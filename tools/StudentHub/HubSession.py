"""学社登录 —— 四种方式，输出同一个 Bearer token。

  1) campus   校园网账号 + 验证码：GET /campus/captcha 取图（base64 dataURL）
              与 jsessionId 绑定，POST /auth/login {loginType:"campus",...}
  2) normal   站内用户名密码：POST /auth/login {loginType:"normal",...}
  3) sms      手机号 + 短信码：POST /sms/send → POST /sms/login
  4) token    浏览器已登录时直接复制 token（localStorage 的 token 字段）

会话落在仓库外 `%LOCALAPPDATA%\\AutoXMYZ\\hub_session.json`
（类 Unix `~/.local/share/AutoXMYZ/`），`AUTOMXYZ_HUB_SESSION` 可覆盖。

campus 验证码两步走（有读图能力时的标准流程）：
    python tools/StudentHub/HubSession.py captcha            # 取图，打印临时文件路径
    # 人/模型看图读码
    python tools/StudentHub/HubSession.py campus -a <账号> -p <密码> --code ab12
验证码的 jsessionId 在第一步落盘（hub_captcha_pending.json），第二步自动取用。
expiresAt（unix 秒）过期则要求重取。

无读图能力可用 --ocr 兜底：复用 591iq/AutoXMYZ 同源的 rapidocr 变体池投票，
失败自动重取新图，默认 6 轮。
"""
import argparse
import json
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.Logcat import Log, setVerbose  # noqa: E402
from StudentHub.HubTransport import (  # noqa: E402
    BASE, SESSION_FILE, CAPTCHA_PENDING_FILE, HubError, HubAuthError,
    HubHttp, saveDataUrl)


def fetchCaptcha(client=None):
    """取验证码：落盘图片 + 暂存 jsessionId。返回 (图片路径, jsessionId, 过期unix)。"""
    c = client or HubHttp()
    d = c.get("/campus/captcha")
    img, jsid, exp = d.get("captchaImage", ""), d.get("jsessionId", ""), d.get("expiresAt")
    out = os.path.join(tempfile.gettempdir(), "hub_captcha_%d.jpg" % int(time.time()))
    saveDataUrl(img, out)
    os.makedirs(os.path.dirname(CAPTCHA_PENDING_FILE), exist_ok=True)
    with open(CAPTCHA_PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump({"jsessionId": jsid, "expiresAt": exp, "image": out}, f)
    return out, jsid, exp


def _pendingJsessionid() -> str:
    if not os.path.exists(CAPTCHA_PENDING_FILE):
        raise HubError(-1, "未取验证码：先执行 HubSession.py captcha")
    with open(CAPTCHA_PENDING_FILE, encoding="utf-8") as f:
        d = json.load(f)
    if d.get("expiresAt") and time.time() > float(d["expiresAt"]):
        raise HubError(-1, "验证码已过期（expiresAt），请重新执行 HubSession.py captcha")
    return d["jsessionId"]


def _persistLogin(d: dict) -> dict:
    """登录响应 data 落盘并验证。data 至少含 token；user/expiresAt 尽力保存。"""
    token = (d or {}).get("token")
    if not token:
        raise HubError(-1, "登录响应缺少 token: %s" % json.dumps(d, ensure_ascii=False)[:200])
    HubHttp.saveSession({"token": token, "user": d.get("user"),
                         "expiresAt": d.get("expiresAt"),
                         "campusInfo": d.get("campusInfo")})
    c = HubHttp()
    try:
        prof = c.getMyProfile()
    except HubError as e:
        raise HubError(-1, "登录后自检失败（token 未生效？）: %s" % e)
    Log.d("HubSession", "登录成功 user=%s" % (prof or {}).get("username"))
    return {"username": (prof or {}).get("username"), "token": token[:8] + "…"}


def loginCampus(account: str, password: str, code: str = None, ocrRounds: int = 0) -> dict:
    """campus 模式。code=None 且 ocrRounds>0 时走 OCR 自动重试。"""
    jsid = _pendingJsessionid() if code else None
    last = None
    for i in range(max(1, ocrRounds) if not code else 1):
        if code:
            captchaCode = code
        else:
            img, jsid, _ = fetchCaptcha()
            captchaCode = _ocrImage(img)
            Log.d("HubSession", "OCR 第%d轮 → %r" % (i + 1, captchaCode))
            if not captchaCode:
                last = "OCR 空结果"
                continue
        c = HubHttp()
        try:
            d = c.post("/auth/login", json={
                "loginType": "campus", "campusAccount": account,
                "campusPassword": password, "captchaCode": captchaCode,
                "jsessionId": jsid})
            return _persistLogin(d)
        except HubError as e:
            last = str(e)
            if code:
                raise
            Log.d("HubSession", "第%d轮失败: %s" % (i + 1, e))
            time.sleep(0.3)
    raise HubError(-1, "campus 登录失败（%d 轮）：%s" % (ocrRounds, last))


def loginNormal(username: str, password: str) -> dict:
    c = HubHttp()
    d = c.post("/auth/login", json={
        "loginType": "normal", "username": username, "password": password})
    return _persistLogin(d)


def loginSms(phone: str, code: str) -> dict:
    c = HubHttp()
    d = c.post("/sms/login", json={"phoneNumber": phone, "code": code})
    return _persistLogin(d)


def loginToken(token: str) -> dict:
    c = HubHttp()
    c.setToken(token)
    try:
        prof = c.getMyProfile()
    except HubError as e:
        raise HubError(-1, "token 无效或已过期: %s" % e)
    HubHttp.saveSession({"token": token, "user": prof})
    return {"username": (prof or {}).get("username"), "token": token[:8] + "…"}


def _ocrImage(path: str) -> str:
    """复用 xmyz 登录的验证码 OCR（同源同参，591iq 实测有效）。"""
    try:
        from Access.LoginSession import ocrCaptcha
    except Exception:
        return ""
    return ocrCaptcha(path)


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="学社（xmyzstudent.com）登录工具",
        epilog="会话文件: %s" % SESSION_FILE)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("captcha", help="取 campus 验证码图（供人/读图模型识别）")
    p.add_argument("--out", default="", help="图片输出路径（默认临时目录）")

    p = sub.add_parser("campus", help="校园网账号登录（配合 captcha 两步走或 --ocr）")
    p.add_argument("-a", "--account", required=True, help="校园网账号")
    p.add_argument("-p", "--password", required=True, help="校园网密码")
    p.add_argument("--code", default="", help="验证码（看过图后填）")
    p.add_argument("--ocr", type=int, default=0, help="OCR 自动重试轮数（无读图能力时）")

    p = sub.add_parser("normal", help="站内用户名密码登录")
    p.add_argument("-u", "--username", required=True)
    p.add_argument("-p", "--password", required=True)

    p = sub.add_parser("sms", help="手机短信登录（先 send）")
    p.add_argument("--phone", required=True)
    p.add_argument("--code", required=True)

    p = sub.add_parser("token", help="直接保存浏览器复制的 token")
    p.add_argument("--token", required=True)

    sub.add_parser("check", help="会话自检（读 hub_session.json 并打 /user/profile）")
    p = sub.add_parser("send-sms", help="发送短信验证码（sms 登录第一步）")
    p.add_argument("--phone", required=True)
    p.add_argument("--purpose", default="login")

    a = ap.parse_args()
    setVerbose(os.environ.get("HUB_DEBUG") == "1")
    try:
        if a.cmd == "captcha":
            img, jsid, exp = fetchCaptcha()
            print("验证码图: %s" % img)
            print("jsessionId 已暂存（过期 unix: %s）——看图后执行:" % exp)
            print("  python tools/StudentHub/HubSession.py campus -a <账号> -p <密码> --code <码>")
        elif a.cmd == "campus":
            print(json.dumps(loginCampus(a.account, a.password,
                                         a.code or None, a.ocr), ensure_ascii=False))
        elif a.cmd == "normal":
            print(json.dumps(loginNormal(a.username, a.password), ensure_ascii=False))
        elif a.cmd == "sms":
            print(json.dumps(loginSms(a.phone, a.code), ensure_ascii=False))
        elif a.cmd == "send-sms":
            c = HubHttp()
            c.post("/sms/send", json={"phoneNumber": a.phone, "purpose": a.purpose})
            print("短信已发送")
        elif a.cmd == "token":
            print(json.dumps(loginToken(a.token), ensure_ascii=False))
        elif a.cmd == "check":
            c = HubHttp()
            prof = c.getMyProfile()
            print(json.dumps({"ok": True, "username": (prof or {}).get("username"),
                              "token": (c.token or "")[:8] + "…"}, ensure_ascii=False))
    except HubError as e:
        print("失败: %s" % e)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())

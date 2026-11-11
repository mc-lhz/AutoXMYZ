"""登录 —— 三种方式，输出同一个 JSESSIONID。

  1) password    账号密码：验证码 OCR 自动重试（有读图能力时优先 VisionLogin）
  2) jsessionid  浏览器已登录时复制会话 id，免验证码
  3) vision      取验证码图并等待人工/读图识别后提交

登录契约：
  GET  /system/system!currentTime.action
  GET  /security/jcaptcha.jpg?_dc=<ms>          验证码与 JSESSIONID 强绑定
  POST /j_spring_security_check                 j_password = sha1(明文)，无盐单次
  POST /account/user!getGrantedMenuTree.action  登录判据：返回非空菜单树

验证码实测特征：4~5 位、只含小写字母、一次性、服务端大小写敏感。
"""
import argparse
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.Logcat import Log, setVerbose  # noqa: E402
from Access.HttpTransport import (  # noqa: E402
    BASE, UA, SESSION_FILE, sha1, XmyzError)

# OCR 变体池：`(阈值, 放大倍数)`，三者强度接近但预处理不同，投票才有效。
# 与 XinYiWo 子技能（原 591iqAutomatic，上游已归档）同源同参——两个系统是同一个门户，实测有效。
CAPTCHA_VARIANTS = [(170, 3), (180, 4), (200, 4)]
DIGIT2LETTER = str.maketrans("0123456789", "olzeasgbgg")


def newSession():
    import requests
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA, "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9",
        "Origin": BASE, "Referer": BASE + "/manager.html",
        "X-Requested-With": "XMLHttpRequest",
    })
    return s


def serverTime(s) -> int:
    """预热/取服务器时间。jcret 非 JSON（404/风控 HTML/503）只是瞬时抖动，
    不该崩掉登录流程——best-effort，取不到返回 0。"""
    try:
        r = s.get(BASE + "/system/system!currentTime.action", timeout=10)
        t = r.text.strip()
        if r.status_code == 200 and t.isdigit():
            return int(t)
        print("[warn] serverTime 返回 HTTP %s 非 JSON（跳过预热）" % r.status_code,
              file=sys.stderr)
    except Exception as e:  # noqa: BLE001 网络抖动一律不致命
        print("[warn] serverTime 探测失败（跳过预热）: %s" % e, file=sys.stderr)
    return 0


def fetchCaptcha(s, out="jcaptcha.jpg") -> str:
    r = s.get(BASE + "/security/jcaptcha.jpg?_dc=%d" % int(time.time() * 1000), timeout=10)
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    # 验证码与 JSESSIONID 强绑定：把取图会话落盘为同名 .sid.txt，供 --code 提交复用。
    with open(out + ".sid.txt", "w", encoding="utf-8") as f:
        f.write(s.cookies.get("JSESSIONID") or "")
    return out


def preprocess(path, out=None, scale=3, threshold=160):
    """红字白底验证码 → 黑字白底 → 放大。"""
    from PIL import Image
    import numpy as np
    im = Image.open(path).convert("L")
    a = np.array(im)
    im2 = Image.fromarray(255 - (a < threshold).astype("uint8") * 255)
    im3 = im2.resize((im2.width * scale, im2.height * scale), Image.LANCZOS)
    out = out or (str(path) + ".prep.png")
    im3.save(out)
    return out


def cleanCode(text: str) -> str:
    """OCR 原始串归一到字符集：数字→形近字母、全转小写、只留 a-z。"""
    t = text.strip().lower().translate(DIGIT2LETTER)
    return "".join(ch for ch in t if "a" <= ch <= "z")


def _ocrOnce(ocr, path):
    res, _ = ocr(path)
    if not res:
        return "", 0.0
    res = sorted(res, key=lambda r: min(p[0] for p in r[0]))
    joined = cleanCode("".join(r[1] for r in res))
    return joined, sum(float(r[2]) for r in res) / len(res)


def ocrCaptcha(path: str) -> str:
    """多预处理变体投票。返回 4~5 位小写字母串，无合法长度候选则返回 ''。"""
    made = []
    for t, s in CAPTCHA_VARIANTS:
        o = "%s.t%d_s%d.png" % (path, t, s)
        made.append(((t, s), preprocess(path, out=o, threshold=t, scale=s)))
    try:
        from rapidocr_onnxruntime import RapidOCR
        ocr = RapidOCR()
    except ModuleNotFoundError as e:
        ocr = None
        print("[ocr] 未安装验证码依赖 %s（pip install %s 可启用自动识别）；"
              "当下请改用 vision 看图登录" % (e.name, e.name),
              file=sys.stderr)
    cands = []
    if ocr:
        for (t, s), f in made:
            code, conf = _ocrOnce(ocr, f)
            Log.d("OCR", "阈值%d×%d → %r conf=%.3f" % (t, s, code, conf))
            if len(code) in (4, 5):
                cands.append((code, conf))
    if not cands:
        return ""
    votes = {}
    for code, conf in cands:
        slot = votes.setdefault(code, [0, 0.0])
        slot[0] += 1
        slot[1] = max(slot[1], conf)
    best = max(votes, key=lambda k: (votes[k][0], votes[k][1]))
    Log.d("OCR", "选定 %r 票数=%s" % (best, {k: v[0] for k, v in votes.items()}))
    return best


def portalLogin(s, username, password, captchaCode) -> bool:
    """Spring Security 表单登录；成功判据是菜单树可取。"""
    r = s.post(BASE + "/j_spring_security_check",
               data={"j_username": username,
                     "j_password": sha1(password),
                     "j_captcha": captchaCode},
               timeout=15, allow_redirects=True)
    if "loginFailure" in r.url or "error=" in r.url:
        print("[login] 被拒:", r.url, file=sys.stderr)
        return False
    try:
        rsp = s.post(BASE + "/account/user!getGrantedMenuTree.action",
                     data={}, timeout=10)
        ctype = rsp.headers.get("Content-Type", "")
        if "json" not in ctype:
            # 服务端瞬时 503/风控 HTML：不是凭据问题，报可读原因。
            print("[login] 菜单树返回非 JSON（HTTP %s，服务端瞬时不可用？请稍后重试）"
                  % rsp.status_code, file=sys.stderr)
            return False
        m = rsp.json()
    except Exception as e:
        print("[login] 菜单树探测异常:", e, file=sys.stderr)
        return False
    if not m:
        print("[login] 菜单树为空", file=sys.stderr)
        return False
    return True


def saveSession(cookies: dict, path: str = SESSION_FILE) -> str:
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        target = path
    except OSError as e:
        import tempfile
        fallback = os.path.join(tempfile.gettempdir(), "AutoXMYZ",
                                os.path.basename(path) or "session.json")
        print("[!] 数据目录不可写（%s），会话降级保存到 %s"
              "（可用 AUTOMXYZ_SESSION 环境变量固定位置）" % (e, fallback), file=sys.stderr)
        os.makedirs(os.path.dirname(fallback), exist_ok=True)
        target = fallback
    with open(target, "w", encoding="utf-8") as f:
        json.dump({"cookies": cookies, "saved_at": time.strftime("%Y-%m-%d %H:%M:%S")},
                  f, ensure_ascii=False, indent=2)
    return target


def loginForSession(username, password, retry=6, captchaFile="jcaptcha.jpg", out=None):
    s = newSession()
    serverTime(s)
    for attempt in range(1, (retry or 6) + 1):
        fetchCaptcha(s, captchaFile)
        code = ocrCaptcha(captchaFile)
        print("[ocr] 第%d次 验证码=%r" % (attempt, code or "(识别失败)"))
        if not code:
            continue
        if portalLogin(s, username, password, code):
            sid = s.cookies.get("JSESSIONID")
            p = saveSession(s.cookies.get_dict(), out or SESSION_FILE)
            print("[login] 成功，JSESSIONID=%s…" % (sid or "")[:8])
            print("[save] 会话 → %s" % p)
            return s
        print("[login] 被拒，换新图")
    raise XmyzError("多次尝试均失败")


def cmdPassword(a) -> int:
    try:
        s = loginForSession(a.username, a.password, retry=a.retry,
                            captchaFile=a.captchaFile, out=getattr(a, "out", None))
    except XmyzError as e:
        print("[x] %s" % e, file=sys.stderr)
        return 3
    d = s.post(BASE + "/account/user!status.action", timeout=10)
    try:
        if "json" not in d.headers.get("Content-Type", ""):
            print("[身份] status 端点非 JSON（HTTP %s，登录已成功，跳过身份显示）"
                  % d.status_code)
        else:
            j = d.json()
            print("[身份] loginName=%s 座位=%s" % (j.get("loginName"), j.get("seatNumber")))
    except Exception as e:  # noqa: BLE001 身份显示已是锦上添花
        print("[身份] 解析异常（登录已成功）: %s" % e)
    return 0


def cmdJsessionid(a) -> int:
    raw = a.jsessionid.strip().strip('"').strip("'")
    if "JSESSIONID=" in raw:
        raw = raw.split("JSESSIONID=", 1)[1].split(";", 1)[0].strip()
    s = newSession()
    s.cookies.set("JSESSIONID", raw, domain="xmyz.xmedu.cn", path="/")
    try:
        d = s.post(BASE + "/account/user!status.action", timeout=10)
        if "json" not in d.headers.get("Content-Type", ""):
            print("[x] status 返回非 JSON（HTTP %s）——服务端可能瞬时不可用，"
                  "请稍后重试而不是重灌会话" % d.status_code, file=sys.stderr)
            return 4
        j = d.json()
    except Exception:
        print("[x] 会话无效（已过期或复制不全），请重新登录", file=sys.stderr)
        return 4
    # 判据用 loginName，不用 loggedIn —— 登录后该字段直接消失（详见 HttpTransport._bindUser）。
    if not j.get("loginName"):
        print("[x] 会话未认证", file=sys.stderr)
        return 4
    p = saveSession(s.cookies.get_dict(), getattr(a, "out", None) or SESSION_FILE)
    print("[ok] 会话可用 → %s" % p)
    print("[身份] loginName=%s" % j.get("loginName"))
    return 0


def cmdVision(a) -> int:
    """取验证码图并等待 --code 提交（供有读图能力的调用方使用）。
    验证码与取图会话强绑定：--code 分支自动复用取图时落盘的 JSESSIONID
    （<captchaFile>.sid.txt），两步走才不是"必定失败"。"""
    if a.code:
        s = newSession()
        sid_file = a.captchaFile + ".sid.txt"
        if os.path.exists(sid_file):
            with open(sid_file, encoding="utf-8") as f:
                sid = f.read().strip()
            if sid:
                s.cookies.set("JSESSIONID", sid, domain="xmyz.xmedu.cn", path="/")
                print("[i] 复用取图会话 JSESSIONID=%s…" % sid[:6])
            else:
                print("[!] 会话暂存为空（%s），验证码很可能已与取图会话失联" % sid_file,
                      file=sys.stderr)
        else:
            print("[!] 未找到取图会话暂存 %s —— 请勿在取图与提交之间运行其他会话操作"
                  "（验证码与 JSESSIONID 强绑定，跨会话提交必被拒 error=2）"
                  % sid_file, file=sys.stderr)
        if not portalLogin(s, a.username, a.password, a.code):
            return 2
        p = saveSession(s.cookies.get_dict(), getattr(a, "out", None) or SESSION_FILE)
        print("[ok] 登录成功 → %s" % p)
        return 0
    s = newSession()
    serverTime(s)
    p = fetchCaptcha(s, a.captchaFile)
    print("验证码图片：%s" % p)
    print("识别后执行：python LoginSession.py vision -u <账号> -p <密码> --code <4~5位>")
    print("（会话已随取图暂存 %s.sid.txt，提交时自动复用）" % p)
    return 0


def cmdCheck(a=None) -> int:
    """无凭据探测各端点可达性。"""
    s = newSession()
    checks = [
        ("serverTime", "GET", "/system/system!currentTime.action"),
        ("captcha", "GET", "/security/jcaptcha.jpg"),
        ("menuTree(未登录)", "POST", "/account/user!getGrantedMenuTree.action"),
        ("userStatus(未登录)", "GET", "/account/user!status.action"),
        ("parameter(未登录)", "GET", "/system/parameter!getParameterValue.action"),
    ]
    for name, method, path in checks:
        try:
            r = s.request(method, BASE + path, timeout=15)
            head = r.content[:60].decode("utf-8", "replace").replace("\n", " ")
            print("  %-22s %s  len=%d  %s" % (name, r.status_code, len(r.content), head))
        except Exception as e:
            print("  %-22s ERR %s" % (name, e))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="method", required=True)

    # 会话默认落在**仓库外**的用户目录（见 HttpTransport.SESSION_FILE），
    # 所以 .gitignore 漏配也不会把活凭据带进提交。--out 可显式改到别处。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--out", default=None,
                        metavar="PATH", help="会话输出路径，默认 %s" % SESSION_FILE)

    p = sub.add_parser("password", parents=[common], help="账号密码 + 验证码 OCR")
    p.add_argument("-u", "--username", required=True)
    p.add_argument("-p", "--password", required=True)
    p.add_argument("--retry", type=int, default=6)
    p.add_argument("--captchaFile", default="jcaptcha.jpg")
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(func=cmdPassword)

    p = sub.add_parser("jsessionid", parents=[common], help="用浏览器会话 id，免验证码")
    p.add_argument("--jsessionid", required=True)
    p.set_defaults(func=cmdJsessionid)

    p = sub.add_parser("vision", parents=[common], help="取验证码图 / 凭 --code 提交")
    p.add_argument("-u", "--username", default="")
    p.add_argument("-p", "--password", default="")
    p.add_argument("--code", default="")
    p.add_argument("--captchaFile", default="jcaptcha.jpg")
    p.set_defaults(func=cmdVision)

    p = sub.add_parser("check", help="无凭据探测端点可达性")
    p.set_defaults(func=cmdCheck)

    a = ap.parse_args()
    setVerbose(getattr(a, "verbose", False))
    sys.exit(a.func(a))


if __name__ == "__main__":
    main()
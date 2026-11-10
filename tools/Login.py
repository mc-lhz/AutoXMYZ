"""统一登录编排：一组学号密码 → 三站会话（0 跨子树 import，全部子进程）。

认证拓扑：
  CampusNet (xmyz.xmedu.cn)      门户直登（自有验证码）→ JSESSIONID
  XinYiWo   (591iq.cn)           同一门户，用该 JSESSIONID 换发 ssoToken
  XmyzStudent (xmyzstudent.com)  学社服务端拿同一凭据回调 CampusNet 校验
                                 （客户端不共享 CampusNet 会话，只共享凭据）

用法：
  python tools/Login.py all -u <学号> -p <密码> [--ocr 6]
  python tools/Login.py campusnet -u <学号> -p <密码> [--ocr 6]
  python tools/Login.py xinyiwo                 # 用现有 CampusNet 会话换 ssoToken
  python tools/Login.py xinyiwo -u <学号> -p <密码>   # 无会话时自行登录门户
  python tools/Login.py xmyzstudent -a <学号> -p <密码> [--code ab12 | --ocr 6]
  python tools/Login.py status                  # 三站会话状态

会话落盘（均在仓库外）：
  %LOCALAPPDATA%\\AutoXMYZ\\session.json      CampusNet JSESSIONID
  %LOCALAPPDATA%\\AutoXMYZ\\iq_token.json     XinYiWo ssoToken
  %LOCALAPPDATA%\\AutoXMYZ\\hub_session.json  XmyzStudent Bearer token
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def _userDataDir():
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "AutoXMYZ")


DATA = _userDataDir()
CAMPUS_SESSION = os.environ.get("AUTOMXYZ_SESSION") or os.path.join(DATA, "session.json")
IQ_TOKEN = os.environ.get("AUTOMXYZ_IQ_TOKEN") or os.path.join(DATA, "iq_token.json")
HUB_SESSION = os.environ.get("AUTOMXYZ_HUB_SESSION") or os.path.join(DATA, "hub_session.json")


def ensureDataDir() -> str:
    """保证会话目录可写；不可写（如 ~/.local/share 归属他人）时降级 %TEMP% 并提示。"""
    global DATA
    global CAMPUS_SESSION, IQ_TOKEN, HUB_SESSION
    try:
        os.makedirs(DATA, exist_ok=True)
        probe = os.path.join(DATA, ".write_test")
        with open(probe, "w", encoding="utf-8") as f:
            f.write("x")
        os.remove(probe)
        return DATA
    except OSError as e:
        import tempfile
        DATA = os.path.join(tempfile.gettempdir(), "AutoXMYZ")
        os.makedirs(DATA, exist_ok=True)
        CAMPUS_SESSION = os.environ.get("AUTOMXYZ_SESSION") or os.path.join(DATA, "session.json")
        IQ_TOKEN = os.environ.get("AUTOMXYZ_IQ_TOKEN") or os.path.join(DATA, "iq_token.json")
        HUB_SESSION = os.environ.get("AUTOMXYZ_HUB_SESSION") or os.path.join(DATA, "hub_session.json")
        print("[!] 数据目录不可写（%s），已降级到 %s" % (e, DATA), file=sys.stderr)
        return DATA

SUBS = {
    "campusnet": os.path.join(ROOT, "references", "CampusNet"),
    "xinyiwo": os.path.join(ROOT, "references", "XinYiWo"),
    "xmyzstudent": os.path.join(ROOT, "references", "XmyzStudent"),
}


def _run(sub, args, capture=False):
    """在子树根跑子进程；capture=False 时实时透传输出。"""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    cwd = SUBS[sub]
    cmd = [PY, "-B"] + args
    if capture:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=600)
        sys.stdout.write(r.stdout or "")
        if r.stderr:
            sys.stdout.write(r.stderr)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    return subprocess.call(cmd, cwd=cwd, env=env), ""


def _campusJsessionid() -> str:
    if not os.path.exists(CAMPUS_SESSION):
        return ""
    try:
        doc = json.load(open(CAMPUS_SESSION, encoding="utf-8"))
        return (doc.get("cookies") or {}).get("JSESSIONID", "")
    except Exception:
        return ""


def loginCampusnet(u, p, ocr=6):
    print("== ① CampusNet 门户登录（xmyz.xmedu.cn）==")
    code, _ = _run("campusnet", ["tools/Access/LoginSession.py", "password",
                                 "-u", u, "-p", p, "--retry", str(ocr)])
    if code != 0:
        print("[!] CampusNet 登录失败（验证码/凭据/网络）", file=sys.stderr)
        return False
    sid = _campusJsessionid()
    print("[ok] CampusNet 会话:", (sid[:8] + "…") if sid else "(未取到 JSESSIONID)")
    return bool(sid)


def loginXinyiwo(u="", p="", ocr=6):
    print("== ② XinYiWo 换发 ssoToken（同一门户）==")
    sid = _campusJsessionid()
    if sid:
        print("[i] 复用 CampusNet JSESSIONID（无需第二次验证码）")
        code, out = _run("xinyiwo", ["tools/Access/LoginToken.py", "jsessionid",
                                     "--jsessionid", sid], capture=True)
    elif u and p:
        print("[i] 无 CampusNet 会话，走门户账号密码（自有验证码）")
        code, out = _run("xinyiwo", ["tools/Access/LoginToken.py", "password",
                                     "-u", u, "-p", p, "--retry", str(ocr)], capture=True)
    else:
        print("[!] 缺 CampusNet 会话，且未给 -u/-p；跳过 XinYiWo", file=sys.stderr)
        return False
    m = re.search(r"ssoToken\s*=\s*([0-9A-Za-z]+)", out or "")
    if code != 0 or not m:
        print("[!] XinYiWo 未取得 ssoToken（门户会话可能失效）", file=sys.stderr)
        return False
    token = m.group(1)
    ensureDataDir()
    with open(IQ_TOKEN, "w", encoding="utf-8") as f:
        json.dump({"token": token, "savedAt": __import__("time").strftime("%Y-%m-%d %H:%M:%S")},
                  f, ensure_ascii=False, indent=1)
    print("[ok] ssoToken 已保存 →", IQ_TOKEN)
    return True


def loginXmyzstudent(account, password, cod="", ocr=0):
    print("== ③ XmyzStudent 学社登录（服务端回调 CampusNet 校验）==")
    args = ["tools/StudentHub/HubSession.py", "campus",
            "-a", account, "-p", password]
    if cod:
        args += ["--code", cod]
    else:
        args += ["--ocr", str(ocr or 6)]
    code, _ = _run("xmyzstudent", args)
    if code != 0:
        print("[!] 学社登录失败（验证码/凭据/网络）", file=sys.stderr)
        return False
    print("[ok] 学社会话 →", HUB_SESSION)
    return True


def status():
    print("== 三站会话状态 ==")
    print("-- CampusNet --")
    _run("campusnet", ["tools/XMYZClient.py", "--health"], capture=False)
    print("-- XinYiWo --")
    tok = ""
    if os.path.exists(IQ_TOKEN):
        try:
            tok = json.load(open(IQ_TOKEN, encoding="utf-8")).get("token", "")
        except Exception:
            tok = ""
    if tok:
        _run("xinyiwo", ["tools/Access/LoginToken.py", "token", tok], capture=True)
    else:
        print("(无 iq_token.json；先跑 Login.py xinyiwo)")
    print("-- XmyzStudent --")
    _run("xmyzstudent", ["tools/StudentHub/HubSession.py", "check"], capture=False)
    print("\n提示：CampusNet 与 XinYiWo 同门户（门户会话失效需一起重登）；"
          "XmyzStudent 是独立 JWT（仅凭据同源）。")


def main():
    ap = argparse.ArgumentParser(
        description="统一登录编排：一组学号密码 → 三站会话（子进程，零跨子树 import）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("all", help="依次登录三站")
    p.add_argument("-u", "--username", required=True)
    p.add_argument("-p", "--password", required=True)
    p.add_argument("--ocr", type=int, default=6, help="OCR 重试轮数")
    p.add_argument("--code-hub", default="", help="学社验证码（看图后填，免 OCR）")

    p = sub.add_parser("campusnet", help="仅登录校内系统（门户）")
    p.add_argument("-u", "--username", required=True)
    p.add_argument("-p", "--password", required=True)
    p.add_argument("--ocr", type=int, default=6)

    p = sub.add_parser("xinyiwo", help="换发/验证 591iq ssoToken")
    p.add_argument("-u", "--username", default="")
    p.add_argument("-p", "--password", default="")
    p.add_argument("--ocr", type=int, default=6)

    p = sub.add_parser("xmyzstudent", help="仅登录学社")
    p.add_argument("-a", "--account", required=True)
    p.add_argument("-p", "--password", required=True)
    p.add_argument("--code", default="", help="学社验证码（看图后填）")
    p.add_argument("--ocr", type=int, default=0, help="OCR 轮数（0=用 --code）")

    sub.add_parser("status", help="三站会话状态")

    a = ap.parse_args()
    if a.cmd == "status":
        status()
        return 0
    if a.cmd == "campusnet":
        return 0 if loginCampusnet(a.username, a.password, a.ocr) else 4
    if a.cmd == "xinyiwo":
        return 0 if loginXinyiwo(a.username, a.password, a.ocr) else 4
    if a.cmd == "xmyzstudent":
        return 0 if loginXmyzstudent(a.account, a.password, a.code, a.ocr) else 4
    # all
    ok1 = loginCampusnet(a.username, a.password, a.ocr)
    ok2 = loginXinyiwo(a.username, a.password, a.ocr) if ok1 else False
    ok3 = loginXmyzstudent(a.username, a.password, a.code_hub, a.ocr)
    print("\n== 结果 ==")
    print("CampusNet   :", "OK" if ok1 else "FAIL")
    print("XinYiWo     :", "OK" if ok2 else "FAIL")
    print("XmyzStudent :", "OK" if ok3 else "FAIL")
    return 0 if (ok1 and ok2 and ok3) else 4


if __name__ == "__main__":
    sys.exit(main())
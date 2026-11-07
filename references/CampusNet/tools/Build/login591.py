#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""复用 591iqAutomatic 的 OCR 与登录契约,登录 xmyz.xmedu.cn 并导出菜单树。

  python login591.py -u <学号> -p <密码> [--retry 6] [--out .]
"""
import argparse, json, os, sys, time

SKILL = os.environ.get(
    "IQ_SKILL",
    os.path.expanduser(r"~/.config/opencode/skills/591iqAutomatic"))
sys.path.insert(0, SKILL)
sys.path.insert(0, os.path.join(SKILL, "tools"))

from tools.Access.LoginToken import (          # noqa: E402
    BASE, sha1, newSession, serverTime, fetchCaptcha,
    ocrCaptcha, portalLogin,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--username", required=True)
    ap.add_argument("-p", "--password", required=True)
    ap.add_argument("--retry", type=int, default=6)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    cap = os.path.join(a.out, "captcha.jpg")
    s = newSession()
    serverTime(s)

    for attempt in range(1, a.retry + 1):
        fetchCaptcha(s, cap)
        code = ocrCaptcha(cap)
        print("[ocr] 第%d次 验证码=%r" % (attempt, code or "(失败)"))
        if not code:
            continue
        if portalLogin(s, a.username, a.password, code):
            break
        print("[login] 被拒，换新图")
    else:
        print("[x] 多次尝试失败", file=sys.stderr)
        return 1

    st = os.path.join(a.out, "session.json")
    with open(st, "w", encoding="utf-8") as f:
        json.dump({"cookies": s.cookies.get_dict()}, f, ensure_ascii=False, indent=2)
    print("[save] 会话 ->", st)

    r = s.post(BASE + "/account/user!getGrantedMenuTree.action", timeout=30)
    mt = os.path.join(a.out, "menu_tree.json")
    with open(mt, "w", encoding="utf-8") as f:
        f.write(r.text)
    print("[save] 菜单树 -> %s  (%d bytes)" % (mt, len(r.text)))

    r2 = s.get(BASE + "/account/user!status.action", timeout=20)
    print("[status]", r2.text[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
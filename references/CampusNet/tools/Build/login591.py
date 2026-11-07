#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""复用 591iqAutomatic 的 OCR 与登录契约,登录 xmyz.xmedu.cn 并导出菜单树。

  python login591.py -u <学号> -p <密码> [--retry 6] [--out .]
"""
import argparse, json, os, sys, time

# 默认指向本仓库的 XinYiWo 子树（references/XinYiWo）；IQ_SKILL 可覆盖
_HERE = os.path.dirname(os.path.abspath(__file__))          # .../CampusNet/tools/Build
_CAMPUS = os.path.dirname(os.path.dirname(_HERE))           # .../CampusNet
_SKILL_ROOT = os.path.dirname(os.path.dirname(_CAMPUS))     # 仓库根（含 references/）
SKILL = os.environ.get(
    "IQ_SKILL",
    os.path.join(_SKILL_ROOT, "references", "XinYiWo"))
# 用「按路径加载」而不是 `from tools.Access...`：
# 子树在聚合仓库内时，`tools` 顶层包名会被 CampusNet 的正规包抢占
# （regular package 优先于 namespace package），跨子树 import 必失败。
import importlib.util as _ilu  # noqa: E402

_LT = os.path.join(SKILL, "tools", "Access", "LoginToken.py")
_spec = _ilu.spec_from_file_location("iq_LoginToken", _LT)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

BASE = _mod.BASE
sha1 = _mod.sha1
newSession = _mod.newSession
serverTime = _mod.serverTime
fetchCaptcha = _mod.fetchCaptcha
ocrCaptcha = _mod.ocrCaptcha
portalLogin = _mod.portalLogin


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
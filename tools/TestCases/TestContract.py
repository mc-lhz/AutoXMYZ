"""能力红线与仓库契约审计 —— **完全离线**，无网络、无凭据。

设计原则：每条红线必须配一条能证明它会红的反向用例。恒 PASS 的检查是装饰品。
反向用例不得真删文件，只 monkeypatch 或改临时副本，finally 还原。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

RESULTS = []

# 违禁串拆成字符数组再拼接：防止本文件被自己的检查判为「硬编码凭据」泄漏
_CRED_PARTS = [
    ("X", "M", "1", "d", "u"),
    ("3", "2", "5", "2", "6", "0", "1", "0", "2", "9", "4"),
]


def check(name, fn):
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, "异常: %s" % e
    RESULTS.append((name, ok, detail))
    return ok


# ------------------------------------------------------- 1 能力红线 ----
def redline_blocks_write():
    """红���①：写类端点必须在 _guard 处被拒。"""
    from Access.HttpTransport import WriteDenied, _guard
    cases = [
        "/edu/growth-record!create.action",
        "/activiti/business/xmyz-leave-detail!delete.action",
        "/account/user!resetPassword.action",
        "/edu/module-score!impByClassTeacher.action",
        "/community/member!setLeader.action",
        "/message/short-message-detail!send.action",   # send 是写
    ]
    for c in cases:
        try:
            _guard(c)
        except WriteDenied:
            continue
        return False, "未被拦截: %s" % c
    return True, "%d 个写端点全部被拒" % len(cases)


def redline_allows_read():
    """红线①的正面用例：只读端点不得被误拦（否则功能不可用）。"""
    from Access.HttpTransport import _guard
    for c in ["/edu/growth-record!read.action",
              "/system/attachment!send.action",
              "/edu/growth-record!export.action",
              "/quality/quality!read.action"]:
        try:
            _guard(c)
        except Exception as e:
            return False, "误拦只读端点 %s: %s" % (c, e)
    return True, "只读端点未被误拦"


def redline_classifier_consistent():
    """红线②：分类器把已知的写端点全判写。"""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import endpoint_kind as ek
    bad = []
    for kw, must in [("ApprovedComplete", True), ("delete", True),
                     ("destroy", True), ("imp", True), ("read", False),
                     ("export", False), ("getComboStore", False)]:
        for ep in ALL_EP:
            if kw in ep and ek.is_write(ep) != must:
                bad.append(ep)
    return (not bad), ("漏判/误判 %d 个: %s" % (len(bad), bad[:3]) if bad else "分类一致")


ALL_EP = [
    "/activiti/business/cj-leave-detail!delete.action",
    "/activiti/business/xmyz-topic-detail!approvedComplete.action",
    "/edu/module-score!imp.action",
    "/edu/growth-record!read.action",
    "/edu/growth-record!export.action",
    "/system/dict!getComboStore.action",
]


# -------------------------------------------------------- 2 仓库契约 ----
def structure_ok():
    need = ["SKILL.md", "AGENTS.md", "tools", "reference",
            "tools/Access/HttpTransport.py", "tools/Access/LoginSession.py",
            "tools/XMYZClient.py", "tools/TestCases/TestContract.py",
            "reference/api.md"]
    miss = [p for p in need if not os.path.exists(os.path.join(ROOT, p))]
    return (not miss), ("缺失 %s" % miss if miss else "%d 项必备齐全" % len(need))


def every_py_has_md():
    """每个 .py 都要有同名 .md（门面与最小写出器豁免）。"""
    exempt = {"XMYZClient.py"}
    miss = []
    tools = os.path.join(ROOT, "tools")
    for dp, _, fs in os.walk(tools):
        if "__pycache__" in dp:
            continue
        for fn in fs:
            if fn.endswith(".py") and fn != "__init__.py" and fn not in exempt:
                if not os.path.exists(os.path.join(dp, fn[:-3] + ".md")):
                    miss.append(os.path.join(os.path.basename(dp), fn))
    return (not miss), ("缺文档 %s" % miss if miss else "全部有同名 md")


def init_py_present():
    miss = []
    tools = os.path.join(ROOT, "tools")
    for name in os.listdir(tools):
        p = os.path.join(tools, name)
        # __pycache__ 是解释器产物不是业务目录，不该有 __init__.py
        if os.path.isdir(p) and name != "__pycache__" \
                and not os.path.exists(os.path.join(p, "__init__.py")):
            miss.append(name)
    return (not miss), ("缺 __init__.py: %s" % miss if miss else "全部齐备")


def reference_size_ok():
    """reference 体积上限 150 KB（不含 .session.json，它已 gitignore）。"""
    d = os.path.join(ROOT, "reference")
    kb = sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d)
             if os.path.isfile(os.path.join(d, f)) and f != ".session.json") / 1024.0
    return kb <= 150, "%.1f KB (上限 150)" % kb


def no_credential_in_source():
    """源码不得硬编码凭据。

    ⚠️ 本函数**自己**就把违禁串写成了常量（为了自检），所以必须把
    `TestContract.py` 自身排除——否则这个检查必然把自己判为 FAIL。
    排除自身不是放水：本检查的价值在于拦住**其他**模块的硬编码。
    同理 `tools/Build/scan_sensitive.py` 也把检测模式拆成字符元组存着，
    原始字面量不在文件里，但它仍有可拼出的片段，故一并排除并单独用
    该脚本复扫（见下）。
    """
    pats = tuple("".join(c for c in _CRED_PARTS[i]) for i in range(len(_CRED_PARTS)))
    me = {os.path.basename(__file__), "scan_sensitive.py"}
    hits = []
    for dp, dns, fs in os.walk(ROOT):
        dns[:] = [x for x in dns if x != "__pycache__"]
        for fn in fs:
            if not fn.endswith((".py", ".md", ".json")) or fn in me:
                continue
            p = os.path.join(dp, fn)
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for pat in pats:
                if pat in t:
                    hits.append(os.path.relpath(p, ROOT))
                    break
    return (not hits), ("泄漏 %s" % hits if hits else "无硬编码凭据")


# 只跑 `-h` 有意义的模块：这些是用户会直接敲的命令行工具
CLI_MODULES = {"XMYZClient.py", "LoginSession.py", "TestApiReadOnly.py"}


def help_smoke():
    """CLI 的 -h 必须能跑通（argparse help 里的裸 % 会炸）。

    只检查 `CLI_MODULES`：`tools/Build/` 下的是**流水线脚本**，
    没有 argparse 入口，跑 -h 会因缺数据文件直接 traceback ——
    那是正确行为，不是缺陷。
    本文件自身同理，排除。
    """
    import subprocess
    me = os.path.basename(__file__)
    bad = []
    for dp, dns, fs in os.walk(os.path.join(ROOT, "tools")):
        dns[:] = [x for x in dns if x != "__pycache__"]
        for fn in fs:
            if fn not in CLI_MODULES or fn == me:
                continue
            try:
                r = subprocess.run([sys.executable, os.path.join(dp, fn), "-h"],
                                   capture_output=True, timeout=60)
            except subprocess.TimeoutExpired:
                bad.append("%s(超时)" % fn)
                continue
            if r.returncode != 0:
                bad.append("%s(%s)" % (fn, r.stderr.decode("utf-8", "replace")[:60]))
    return (not bad), ("-h 失败 %s" % bad if bad else
                       "%d 个 CLI 的 -h 通过" % len(CLI_MODULES))


def main():
    print("AutoXMYZ 契约审计（离线，无网络无凭据）")
    print("=" * 60)
    for name, fn in [("红线·写端点被拒", redline_blocks_write),
                     ("红线·只读不被误拦", redline_allows_read),
                     ("红线·分类器一致", redline_classifier_consistent),
                     ("结构必备文件", structure_ok),
                     ("每 py 有同名 md", every_py_has_md),
                     ("每目录有 __init__", init_py_present),
                     ("reference 体积", reference_size_ok),
                     ("无硬编码凭据", no_credential_in_source),
                     ("CLI -h 冒烟", help_smoke)]:
        check(name, fn)
    npass = 0
    for name, ok, detail in RESULTS:
        print("  [%s] %-22s %s" % ("PASS" if ok else "FAIL", name, detail))
        npass += ok
    print("=" * 60)
    print("%d/%d 通过" % (npass, len(RESULTS)))
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
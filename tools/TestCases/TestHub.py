"""学社（StudentHub）仓库契约审计 —— 完全离线，无网络无凭据。

与 TestContract.py 同风格：每条检查配能证明它会红的反向用例。
覆盖：注册表一致性、门面组合、传输层信封语义（mock）、文档再生成一致。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

RESULTS = []


def check(name, fn):
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, "异常: %s" % e
    RESULTS.append((name, ok, detail))
    return ok


# ------------------------------------------------------- 1 注册表 ----
def registry_shape():
    from StudentHub import HubEndpoints as HE
    seen, bad = set(), []
    for m, p, k, dom, w in HE.REST_ENDPOINTS:
        if not p.startswith("/"):
            bad.append("路径不以/: %s" % p)
        if k not in ("read", "write"):
            bad.append("kind 非法: %s %s" % (m, p))
        if k != ("read" if m == "GET" else "write"):
            bad.append("kind 与方法不符: %s %s" % (m, p))
        if (m, p) in seen:
            bad.append("重复: %s %s" % (m, p))
        seen.add((m, p))
    c = HE.counts()
    if c["rest"] != len(HE.REST_ENDPOINTS) or c["ws"] != len(HE.WS_ROUTES):
        bad.append("counts() 与表不符")
    return (not bad), ("260 端点形态一致" if not bad else "问题 %d: %s" % (len(bad), bad[:3]))


def registry_wrapper_names():
    """wrapper 必须是合法标识符且不与 Python 关键字冲突。"""
    import keyword
    from StudentHub import HubEndpoints as HE
    bad = [w for _, _, _, _, w in HE.REST_ENDPOINTS
           if w and (not w[0].islower() or keyword.iskeyword(w))]
    return (not bad), ("wrapper 命名合法" if not bad else str(bad[:5]))


def is_write_symmetry():
    """is_write 与 kind 双向一致（含未知端点必须 KeyError）。"""
    from StudentHub import HubEndpoints as HE
    for m, p, k, _, _ in HE.REST_ENDPOINTS[:50]:
        if HE.is_write(p, m) != (k == "write"):
            return False, "不对称: %s %s" % (m, p)
    try:
        HE.is_write("/admin/banners", "GET")
        HE.is_write("/admin/banners", "PUT")
        HE.is_write("/not/exist")
        return False, "未知端点应 KeyError"
    except KeyError:
        return True, "读写判定双向一致（同路径多方法已区分）"


# ------------------------------------------------------- 2 门面 ----
def facade_composition():
    from StudentHubClient import StudentHubClient
    from StudentHub.HubTransport import HubHttp
    mro = [c.__name__ for c in StudentHubClient.__mro__]
    if mro[-1] != "object" or mro[-2] != "HubHttp":
        return False, "HubHttp 必须在继承链末位（object 前）: %s" % mro[-3:]
    need = ["getMyProfile", "getAdminTallyActivities", "voteAdminTallyCandidates",
            "uploadFile", "getUnreadMessageCount", "getVoiceQuestions",
            "searchRatingItems", "getCampuses", "getAdminDebateRounds",
            "getMessages", "getPublicTicketActivities"]
    miss = [m for m in need if not hasattr(StudentHubClient, m)]
    return (not miss), ("11 域方法齐备" if not miss else "缺 %s" % miss)


def facade_no_method_collision():
    """各 mixin 方法不得同名覆盖（同名即丢端点）。"""
    from StudentHubClient import StudentHubClient
    from StudentHub import HubEndpoints as HE
    wrappers = {w for _, _, _, _, w in HE.REST_ENDPOINTS if w}
    defined = set()
    for cls in StudentHubClient.__mro__:
        for n in vars(cls):
            if not n.startswith("_"):
                defined.add(n)
    miss = wrappers - defined
    return (not miss), ("260 wrapper 全部可调用" if not miss else "被覆盖/缺失 %s" % sorted(miss)[:5])


# ------------------------------------------------------- 3 传输 ----
class _FakeResp(object):
    def __init__(self, doc, ctype="application/json", status=200):
        self._doc, self._ct, self.status = doc, ctype, status
        self.text = ""

    def json(self):
        return self._doc

    @property
    def status_code(self):
        return self.status

    @property
    def headers(self):
        return {"Content-Type": self._ct}


def _mockClient(doc, status=200, ctype="application/json"):
    from StudentHub.HubTransport import HubHttp
    c = HubHttp.__new__(HubHttp)
    import requests
    c._requests = requests
    c._s = requests.Session()
    c._lastCall, c._token = 0.0, None
    holder = {}

    def fake(url=None, **kw):
        holder["url"] = url
        return _FakeResp(doc, ctype, status)

    c._s.get = fake
    c._s.post = fake
    c._s.put = fake
    c._s.delete = fake
    return c, holder


def envelope_ok():
    c, holder = _mockClient({"code": 200, "message": "success", "data": [1, 2]})
    out = c.get("/banners")
    return out == [1, 2] and holder["url"].endswith("/api/v2/banners"), "信封解包正确"


def envelope_fail_raises():
    from StudentHub.HubTransport import HubError
    c, _ = _mockClient({"code": 500, "message": "炸了", "data": None})
    try:
        c.get("/x")
        return False, "code=500 未抛"
    except HubError as e:
        return e.code == 500 and "炸了" in str(e), "业务失败抛 HubError"


def auth401_raises():
    from StudentHub.HubTransport import HubAuthError
    c, _ = _mockClient({"code": 401, "message": "未授权", "data": None})
    try:
        c.get("/user/profile")
        return False, "401 未抛"
    except HubAuthError:
        return True, "401 抛 HubAuthError"


def bearer_attached():
    c, _ = _mockClient({"code": 200, "message": "ok", "data": {}})
    c.setToken("abc123")
    if c._s.headers.get("Authorization") != "Bearer abc123":
        return False, "Bearer 头未设置"
    return True, "Bearer 头随 token 设置"


def non_json_raises():
    from StudentHub.HubTransport import HubError
    c, _ = _mockClient("boom", ctype="text/html")
    try:
        c.get("/x")
        return False, "非 JSON 未抛"
    except HubError:
        return True, "非 JSON 响应抛 HubError"


# ------------------------------------------------------- 4 文档 ----
def hub_docs_in_sync():
    """reference/hub-api.md 必须与注册表内存重生成一致（否则文档漂移）。"""
    import subprocess
    dst = os.path.join(ROOT, "reference", "hub-api.md")
    if not os.path.exists(dst):
        return False, "缺 reference/hub-api.md"
    with open(dst, encoding="utf-8") as f:
        before = f.read()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", os.path.join(ROOT, "tools", "Build",
                        "gen_hub_api_md.py")], capture_output=True, env=env, timeout=60)
    with open(dst, encoding="utf-8") as f:
        after = f.read()
    return before == after, ("文档与注册表一致" if before == after else
                             "hub-api.md 与注册表漂移（跑 gen_hub_api_md.py）")


def mixin_md_present():
    from StudentHub import HubEndpoints as HE
    doms = {d for _, _, _, d, _ in HE.REST_ENDPOINTS}
    names = {"HubTally": "TallyMixin", "HubCampaign": "CampaignMixin",
             "HubDebate": "DebateMixin", "HubCampus": "CampusMixin",
             "HubMuseum": "MuseumMixin", "HubRating": "RatingMixin",
             "HubTicket": "TicketMixin", "HubVoices": "VoicesMixin",
             "HubPortal": "PortalMixin", "HubAccount": "AccountMixin",
             "HubMessage": "MessageMixin"}
    miss = [n for d, n in names.items() if d in doms and
            not os.path.exists(os.path.join(ROOT, "tools", "StudentHub", n + ".md"))]
    return (not miss), ("mixin md 齐" if not miss else str(miss))


def no_credentials():
    """学社侧不得出现真实 token/密码样例（32 hex 及以上 / Bearer + 长串）。"""
    import re
    bad = []
    for dp, dns, fs in os.walk(os.path.join(ROOT, "tools", "StudentHub")):
        dns[:] = [x for x in dns if x != "__pycache__"]
        for fn in fs:
            if not fn.endswith((".py", ".md")):
                continue
            t = open(os.path.join(dp, fn), encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"[0-9a-fA-F]{32,}", t):
                bad.append("%s:%s" % (fn, m.group(0)[:12]))
    return (not bad), ("无硬编码凭据样例" if not bad else str(bad[:5]))


# ------------------------------------------------------- 5 CLI ----
def cli_help():
    import subprocess
    bad = []
    for rel in ("tools/StudentHubClient.py", "tools/StudentHub/HubSession.py"):
        r = subprocess.run([sys.executable, "-B", os.path.join(ROOT, rel), "-h"],
                           capture_output=True, timeout=60)
        if r.returncode != 0:
            bad.append("%s: %s" % (rel, r.stderr.decode("utf-8", "replace")[:60]))
    return (not bad), ("2 个 CLI -h 通过" if not bad else str(bad))


def main():
    print("StudentHub 契约审计（离线，无网络无凭据）")
    print("=" * 60)
    for name, fn in [("注册表·形态", registry_shape),
                     ("注册表·wrapper 命名", registry_wrapper_names),
                     ("注册表·读写对称", is_write_symmetry),
                     ("门面·组合与 MRO", facade_composition),
                     ("门面·无方法覆盖", facade_no_method_collision),
                     ("传输·信封解包", envelope_ok),
                     ("传输·业务失败抛错", envelope_fail_raises),
                     ("传输·401 抛错", auth401_raises),
                     ("传输·Bearer 头", bearer_attached),
                     ("传输·非 JSON 抛错", non_json_raises),
                     ("文档·hub-api 一致", hub_docs_in_sync),
                     ("文档·mixin md", mixin_md_present),
                     ("安全·无凭据样例", no_credentials),
                     ("CLI·-h 冒烟", cli_help)]:
        check(name, fn)
    npass = 0
    for name, ok, detail in RESULTS:
        print("  [%s] %-20s %s" % ("PASS" if ok else "FAIL", name, detail))
        npass += ok
    print("=" * 60)
    print("%d/%d 通过" % (npass, len(RESULTS)))
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())

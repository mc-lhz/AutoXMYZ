"""传输层：会话建立、调用、登录、身份识别 + XmyzError。

能力政策（2026-10-24 由仓库所有者修订）：
  - 早期版本为「纯只读」，`_guard` 在发请求前强制拦截写语义端点；
  - 现已解除拦截：**读写都放行**，写能力是本工具的需求本身。
    `endpoint_kind.py::is_write` 保留，作为文档/统计口径（api.md 的 kind 列），
    不再作为运行时闸门。实际可写范围由**服务端账号权限**决定——
    无权限的写端点会被服务端拒绝，客户端不越权、不枚举他人数据。
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.Logcat import Log  # noqa: E402

BASE = "https://xmyz.xmedu.cn"
AES_KEY = "Tk8IVNJ8B75nHDgb"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def _userDataDir() -> str:
    """跨平台用户数据目录：仓库**之外**，与会话凭据隔离。"""
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "AutoXMYZ")


_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ⚠️ 会话**默认写在仓库外**。
#
# 曾经默认写 `reference/.session.json`，于是每次登录都会把**活凭据**
# 落进工作区；一旦仓库没配 .gitignore（本仓库刻意没有），
# `git add -A` 就会把一条可直接冒用身份的 JSESSIONID 推上 GitHub。
# 靠 .gitignore 挡是「记得配才行」的方案，靠路径隔离才是「不配也不会漏」。
# 覆盖优先级：AUTOMXYZ_SESSION 环境变量 > 本默认值。
SESSION_FILE = os.environ.get("AUTOMXYZ_SESSION") or os.path.join(_userDataDir(), "session.json")

# 仓库里只保留**占位模板**，仅用于在未登录时给出可读提示。
TEMPLATE_FILE = os.path.join(_REPO, "reference", ".session.json")

# 分类器：tools/endpoint_kind.py（历史 2026-10-24 前）曾用作运行时红线闸门，
# 现在只做**文档/统计口径**（api.md 的 kind 列、合并清单的读写标注）。
# 历史教训仍有效：判定逻辑只有一份，别在任何地方维护第二套名单。
from endpoint_kind import is_write  # noqa: F401  （供文档/统计方复用）


class XmyzError(Exception):
    pass


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def action_of(path: str) -> str:
    m = re.search(r"!([A-Za-z0-9_]+)\.action", path or "")
    return m.group(1) if m else ""


class Http(object):
    """只读传输基类。`_call` 是唯一出口，红线守在这里。"""

    def __init__(self, cookie: dict = None, token: str = None):
        import requests
        self._requests = requests
        self._s = requests.Session()
        self._s.headers.update({
            "User-Agent": UA,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": BASE + "/manager.html",
            "Origin": BASE,
            "X-Requested-With": "XMLHttpRequest",
        })
        self._userId = None
        if token:
            self.login(token)
        else:
            # ⚠️ 踩过的坑：曾经写成 `elif cookie:`，于是 `XMYZClient()` 无参构造
            # （门面最常见的用法）**静默不加载会话文件**，直接以未登录身份跑完全部
            # 方法——而未登录时大部分只读端点照样返回 200，于是「测试全绿」，
            # 实则一条真实数据都没取到。默认路径必须自己读文件。
            ck = cookie if cookie is not None else self.loadCookie()
            if ck:
                self._s.cookies.update(ck)
                self._bindUser()

    # ------------------------------------------------------------ 会话 ----
    @staticmethod
    def loadCookie(path: str = None) -> dict:
        path = path or SESSION_FILE
        if not os.path.exists(path):
            # 回退到仓库模板只为**给出可读提示**，不是拿它当会话用。
            if os.path.exists(TEMPLATE_FILE):
                raise XmyzError(
                    "未登录：用户会话 %s 不存在。\n"
                    "       请先执行：python tools/Access/LoginSession.py password -u <学号> -p <密码>\n"
                    "       （仓库里的 reference/.session.json 只是占位模板，不参与运行）"
                    % path)
            raise XmyzError("未找到会话文件 %s，请先执行 LoginSession.py password" % path)
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        ck = (doc or {}).get("cookies") or {}
        sid = ck.get("JSESSIONID", "")
        # 占位模板里的中文占位符不能当 cookie 发。
        # 不校验的话，requests 会把它塞进 Cookie 头，抛一个
        # `UnicodeEncodeError: 'latin-1' codec can't encode ...` —— 与真实故障毫不相干。
        if not sid:
            raise XmyzError("会话文件缺少 JSESSIONID，请重新执行 LoginSession.py password")
        if not re.fullmatch(r"[0-9A-F]{16,}", sid):
            raise XmyzError(
                "会话文件里的 JSESSIONID 不是有效值（%r），文件可能是占位模板。"
                "请先执行：python tools/Access/LoginSession.py password -u <学号> -p <密码>"
                % (sid[:24] + ("…" if len(sid) > 24 else "")))
        return ck

    def _bindUser(self) -> dict:
        """绑定身份并校验会话有效性。

        ⚠️ 踩过的坑：不能用 `status.action` 的 `loggedIn` 字段判会话。
        未登录时它返回 `{"success":true,"loggedIn":false,"principalSize":N}`；
        登录后该字段**直接消失**，`j.get("loggedIn")` 于是返回 None——
        用 `== False` 判会误报未登录，用 `== True` 判又永远失败。
        可靠判据是 profile 里有没有 `loginName`/`id`。
        """
        d = self._call("/account/user!status.action", method="GET")
        self._userId = d.get("id") or d.get("studentId")
        if not (d.get("loginName") and self._userId):
            raise XmyzError(
                "会话无效或已过期（status 返回 loggedIn 缺失且无 loginName），"
                "请重新执行 LoginSession.py password 或 jsessionid")
        Log.d("Http", "绑定身份 loginName=%s userId=%s"
              % (d.get("loginName"), str(self._userId)[:8]))
        return d

    def login(self, token: str) -> dict:
        """token 即 JSESSIONID 值。"""
        self._s.cookies.set("JSESSIONID", token, domain="xmyz.xmedu.cn", path="/")
        return self._bindUser()

    @property
    def userId(self):
        return self._userId

    # ------------------------------------------------------------ 调用 ----
    def _call(self, path: str, method: str = "GET", params: dict = None, **kw):
        url = path if path.startswith("http") else BASE + "/" + path.lstrip("/")
        fn = self._s.post if method.upper() == "POST" else self._s.get
        Log.d("Http", "%s %s params=%s" % (method.upper(), path, params))
        r = fn(url, data=params if method.upper() == "POST" else None,
               params=params if method.upper() != "POST" else None,
               timeout=kw.pop("timeout", 25), allow_redirects=False, **kw)
        ctype = r.headers.get("Content-Type", "")
        if "json" in ctype:
            try:
                return r.json()
            except Exception:
                pass
        t = r.text.strip()
        if t[:1] in "[{":
            try:
                return json.loads(t)
            except Exception:
                pass
        return {"success": False, "message": t[:200], "_status": r.status_code}

    def get(self, path: str, params: dict = None, **kw):
        return self._call(path, "GET", params, **kw)

    def post(self, path: str, params: dict = None, **kw):
        return self._call(path, "POST", params, **kw)

    # ------------------------------------------------------------ 分页 ----
    def paged(self, path: str, params: dict = None, limit: int = 60,
              maxRows: int = 2000, **kw):
        """桌面端分页契约：start + limit，响应 {total,data,success}。"""
        params = dict(params or {})
        rows, off = [], 0
        while off < maxRows:
            params["start"] = off
            params["limit"] = limit
            d = self.get(path, params, **kw)
            batch = (d or {}).get("data") or []
            if not isinstance(batch, list):
                return rows, d
            rows.extend(batch)
            if len(batch) < limit:
                break
            off += limit
        return rows, {"success": True, "rows": len(rows)}
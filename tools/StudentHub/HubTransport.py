"""学社传输层：Bearer 会话、统一信封解包、限速、multipart 上传、WS 快照订阅。

设计约束：
  - 与 xmyz 的 `Access/HttpTransport.py` **完全独立**：不同源站、不同鉴权
    （xmyz 是 JSESSIONID cookie + Struts2；学社是 Bearer token + JSON API）。
  - 学社端**不设写拦截**：xmyzstudent.com 是学生自建平台，写能力是本技能的需求
    本身（唱票、审核、发布）。端点读写分类保留在 `HubEndpoints.py` 供文档与
    统计使用，语义与 xmyz 的 `endpoint_kind.is_write` 相反——那里 True=拦截。
  - 信封契约：业务失败也是 HTTP 200，靠 `code !== 200` 区分（链路分析报告 §3.1）。
    本层把 code!=200 翻译成异常，调用方拿到的 data 永远是成功数据。
"""
import base64
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.Logcat import Log  # noqa: E402

BASE = "https://api.xmyzstudent.com/api/v2"
WS_BASE = "wss://api.xmyzstudent.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def _userDataDir() -> str:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "AutoXMYZ")


# 会话同样**写在仓库外**（与 xmyz 同目录、不同文件），覆盖优先级：
# AUTOMXYZ_HUB_SESSION 环境变量 > 本默认值。
SESSION_FILE = os.environ.get("AUTOMXYZ_HUB_SESSION") or \
    os.path.join(_userDataDir(), "hub_session.json")

# 登录两步走时，验证码的暂存（jsessionId 与验证码图绑定，非会话凭据）
CAPTCHA_PENDING_FILE = os.path.join(_userDataDir(), "hub_captcha_pending.json")

# 单账号串行限速；0 可关（自建平台压力可控，但默认仍给服务端留喘息）
MIN_INTERVAL_S = float(os.environ.get("AUTOMXYZ_HUB_MIN_INTERVAL_MS", "150")) / 1000.0


class HubError(Exception):
    """业务失败（信封 code != 200）。"""

    def __init__(self, code, message, path=""):
        super().__init__("学社业务失败 code=%s: %s (%s)" % (code, message, path))
        self.code = code
        self.message = message
        self.path = path


class HubAuthError(HubError):
    """401：token 缺失或过期。重新执行 HubSession.py 即可。"""


class HubHttp(object):
    """学社 HTTP 基类。`_request` 是唯一出口。"""

    def __init__(self, token: str = None):
        import requests
        self._requests = requests
        self._s = requests.Session()
        self._s.headers.update({
            "User-Agent": UA,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "https://xmyzstudent.com",
            "Referer": "https://xmyzstudent.com/",
        })
        self._lastCall = 0.0
        self._token = None
        if token:
            self.setToken(token)
        else:
            # 与 xmyz 踩过的坑同理：无参构造必须自己读会话文件，
            # 否则会静默以未登录身份运行（学社端更隐蔽：公开端点 200，
            # 只有本人数据端点 401，一不留神就是「半绿」假象）。
            saved = self.loadSession()
            if saved and saved.get("token"):
                self.setToken(saved["token"])

    # ------------------------------------------------------------ 会话 ----
    @staticmethod
    def loadSession(path: str = None) -> dict:
        path = path or SESSION_FILE
        if not os.path.exists(path):
            return {}
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f) or {}
        except Exception:
            return {}

    @staticmethod
    def saveSession(doc: dict, path: str = None) -> str:
        path = path or SESSION_FILE
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc = dict(doc)
        doc["savedAt"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        return path

    def setToken(self, token: str):
        self._token = token
        self._s.headers["Authorization"] = "Bearer %s" % token

    @property
    def token(self):
        return self._token

    # ------------------------------------------------------------ 调用 ----
    def _throttle(self):
        if MIN_INTERVAL_S <= 0:
            return
        wait = self._lastCall + MIN_INTERVAL_S - time.time()
        if wait > 0:
            time.sleep(wait)
        self._lastCall = time.time()

    def _request(self, method: str, path: str, params: dict = None,
                 json_body: dict = None, files: dict = None, form: dict = None,
                 timeout: int = 25):
        url = path if path.startswith("http") else BASE + path
        self._throttle()
        Log.d("Hub", "%s %s params=%s json=%s"
              % (method, path, params, "<body>" if json_body else None))
        fn = getattr(self._s, method.lower())
        r = fn(url, params=params, json=json_body, files=files, data=form, timeout=timeout)
        ctype = r.headers.get("Content-Type", "")
        if "json" not in ctype:
            raise HubError(r.status_code, "非 JSON 响应: %s" % r.text[:120], path)
        doc = r.json()
        if not isinstance(doc, dict) or "code" not in doc:
            return doc  # 防御：非信封响应原样返回
        code, msg = doc.get("code"), doc.get("message", "")
        if code == 200:
            return doc.get("data")
        if code == 401 or r.status_code == 401:
            raise HubAuthError(401, msg or "未授权", path)
        raise HubError(code, msg, path)

    def get(self, path, params=None, **kw):
        return self._request("GET", path, params=params, **kw)

    def post(self, path, params=None, json=None, **kw):
        return self._request("POST", path, params=params, json_body=json, **kw)

    def put(self, path, params=None, json=None, **kw):
        return self._request("PUT", path, params=params, json_body=json, **kw)

    def delete(self, path, params=None, json=None, **kw):
        return self._request("DELETE", path, params=params, json_body=json, **kw)

    def upload(self, path, filepath: str, businessType: str = None,
               field: str = "file", btField: str = "businessType"):
        """multipart 上传。`field` 是文件字段名；`btField` 是业务类型字段名
        （站点不统一：/files/upload 用 business_type，rating 域用 businessType）。"""
        with open(filepath, "rb") as f:
            files = {field: (os.path.basename(filepath), f)}
            form = {btField: businessType} if businessType else None
            return self._request("POST", path, form=form, files=files)

    # ------------------------------------------------------------ 分页 ----
    def paged(self, path: str, params: dict = None, pageKey: str = "page",
              sizeKey: str = "size", size: int = 20, maxRows: int = 2000, **kw):
        """学社分页契约：page + size（部分端点用 pageSize），响应 data 形如
        {list/records/items, total} 或裸数组——都能吃。"""
        params = dict(params or {})
        rows, page = [], 1
        while len(rows) < maxRows:
            params[pageKey], params[sizeKey] = page, size
            d = self.get(path, params, **kw)
            batch, total = self._pageParts(d)
            if not batch:
                break
            rows.extend(batch)
            if total and len(rows) >= total:
                break
            if len(batch) < size:
                break
            page += 1
        return rows

    @staticmethod
    def _pageParts(d):
        if isinstance(d, list):
            return d, None
        if isinstance(d, dict):
            for k in ("records", "list", "items", "rows", "data"):
                if isinstance(d.get(k), list):
                    return d[k], d.get("total")
        return [], None

    # ------------------------------------------------------------ WS ----
    def wsSnapshots(self, wsPath: str, onFrame, seconds: float = 0, token: str = None):
        """订阅 WS 全量快照（tally 大屏 / debate 场）。

        onFrame(dict) 每帧回调；seconds>0 时到点返回，否则 Ctrl-C 退出。
        源站大屏公开无需鉴权；需要鉴权的路由传 token。
        """
        import websocket
        url = wsPath if wsPath.startswith("ws") else WS_BASE + wsPath
        hdr = ["Authorization: Bearer %s" % (token or self._token)] \
            if (token or self._token) else []
        ws = websocket.create_connection(url, header=hdr, timeout=5)
        deadline = time.time() + seconds if seconds else None
        try:
            while True:
                frame = ws.recv()
                if not frame:
                    continue
                try:
                    onFrame(json.loads(frame))
                except ValueError:
                    Log.d("Hub", "非 JSON 帧: %r" % frame[:60])
                if deadline and time.time() > deadline:
                    return
        finally:
            ws.close()

    # ------------------------------------------------------------ 工具 ----
    @staticmethod
    def saveDataUrl(dataUrl: str, out: str) -> str:
        """兼容别名：主体是模块级 saveDataUrl。"""
        return saveDataUrl(dataUrl, out)


def saveDataUrl(dataUrl: str, out: str) -> str:
    """data:image/jpeg;base64,... → 落盘（campus 验证码图）。"""
    m = re.match(r"data:image/(\w+);base64,(.+)", dataUrl or "", re.S)
    if not m:
        raise HubError(-1, "验证码 dataURL 格式异常")
    raw = base64.b64decode(m.group(2))
    with open(out, "wb") as f:
        f.write(raw)
    return out

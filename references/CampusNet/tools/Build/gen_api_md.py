#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""由 endpoints.json + validation.json 生成 reference/api.md"""
import json, os, io, sys, re
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def _work_dir():
    """建库工作目录：环境变量 AUTOMXYZ_WORK > <仓库>/build_data。

    原始数据（menu_tree.json / endpoints.json / validation.json / js/）落在这里。
    ⚠️ 这些文件含真实姓名、学号、userId，**不入库**；
    需要时用 tools/Build/ 下的脚本重新生成。
    """
    import os as _os
    return _os.environ.get(
        "AUTOMXYZ_WORK",
        _os.path.join(_os.path.dirname(_os.path.dirname(
            _os.path.dirname(_os.path.abspath(__file__)))), "build_data"))


WD = _work_dir()
rows = json.load(open(os.path.join(WD, "endpoints.json"), encoding="utf-8"))
val = json.load(open(os.path.join(WD, "validation.json"), encoding="utf-8"))
vmap = {v["endpoint"]: v for v in val}

SRC_CN = {"desktop": "桌面端", "m2": "m2.html", "m": "m.html"}


def ns_of(ep):
    return ep.lstrip("/").split("/")[0].split("!")[0] or "(根)"


by_ns = defaultdict(lambda: {"read": [], "write": []})
for r in rows:
    by_ns[ns_of(r["endpoint"])][r["kind"]].append(r)

out = []
w = out.append
w("# 厦门一中信息校园综合应用系统 API 清单")
w("")
w("目标站：`https://xmyz.xmedu.cn`（Struts2 后端，三个前端共用同一会话）")
w("")
w("| 前端 | 入口 | 技术栈 | 端点数 | 角色 |")
w("|---|---|---|---|---|")
w("| 桌面管理端 | `manager.html` | ExtJS 3.4，服务端驱动按需加载 | %d | 门户「登录」按钮指向的正式入口 |"
  % sum(1 for r in rows if "desktop" in r["sources"]))
w("| 移动端新版 | `m2.html` | Vue 3 + Vant，hash 路由 | %d | 待办审批 + 4 项委托功能 |"
  % sum(1 for r in rows if "m2" in r["sources"]))
w("| 移动端旧版 | `m.html` | Vue 2 + Vux，hash 路由 | %d | 已被 m2 取代，m2 守卫失败时回落此处登录 |"
  % sum(1 for r in rows if "m" in r["sources"]))
w("")
w("合并去重后 **%d** 个唯一端点：只读 %d / 写类 %d。端点层几乎不重叠（三方共有 0 个），"
  "因为三个前端各写各的 Action 名；功能层互补。"
  % (len(rows), sum(1 for r in rows if r["kind"] == "read"),
     sum(1 for r in rows if r["kind"] == "write")))
w("")
w("## 授权口径")
w("")
w("本文清单由**登录后的菜单树**（`POST /account/user!getGrantedMenuTree.action`）"
  "下发，并按各菜单节点携带的 `action.jsFile` 定向抓取 97 个模块得到，"
  "因此 desktop 一列的 %d 个端点**是当前账号有权访问的**，不是静态猜测。"
  % sum(1 for r in rows if "desktop" in r["sources"]))
w("m2.html 一列来自前端 bundle 静态提取，反映能力面，实际可用性以运行时权限为准。")
w("")

w("## 登录契约")
w("")
w("```")
w("GET  /system/system!currentTime.action                     # 取服务端毫秒时间，顺带分配会话")
w("GET  /security/jcaptcha.jpg?_dc=<ms>                        # 验证码，与 JSESSIONID 强绑定")
w("POST /j_spring_security_check                             # j_username / j_password=sha1(明文) / j_captcha")
w("POST /account/user!getGrantedMenuTree.action              # 登录判据：返回非空菜单树")
w("```")
w("")
w("- 无 token / JWT，认证态就是 `JSESSIONID` Cookie（`Path=/`，同源三端共享）")
w("- `j_password` 为 **无盐单次 SHA-1**（`hashlib.sha1(明文).hexdigest()`）")
w("- 验证码 **4~5 位、只含小写字母、一次性、服务端大小写敏感**")
w("- 桌面端另有 `account/user!qrCodeLogin.action`（扫码登录，需手机端配合）与 "
  "`account/user!sendSmsVerification.action`（短信），本技能不封装")
w("")

w("## 只读探测结果")
w("")
from collections import Counter
c = Counter(v["verdict"] for v in val)
w("对 %d 个只读端点各发一次 GET + POST（`start=0&limit=1`，`id` 一律用不存在的 `-1`），"
  "限速 180ms，结果：" % len(val))
w("")
w("| 判定 | 数量 | 含义 |")
w("|---|---|---|")
w("| ALIVE | %d | 返回 2xx |" % c.get("ALIVE", 0))
w("| FORBIDDEN | %d | 401/403，账号无权 |" % c.get("FORBIDDEN", 0))
w("| GONE | %d | 404，路由不存在 |" % c.get("GONE", 0))
w("| REDIRECT | %d | 302，典型是未绑定的单点登录 |" % c.get("REDIRECT", 0))
w("| ERROR | %d | 连接异常或超时 |" % c.get("ERROR", 0))
w("")
w("`success:false` 且 `message` 是业务提示（如「合同申请或审批任务不存在」）也算 ALIVE——"
  "说明路由存在、鉴权通过，只是没有对应数据。")
w("")

w("## 分页与信封")
w("")
w("桌面端分页参数是 `start` + `limit`（`Config.js` 里 `LIMIT=60`），"
  "不是 m2 的 `page`/`pageSize`。响应根属性固定为：")
w("")
w("```json")
w('{"total": 12, "data": [ ... ], "success": true}')
w("```")
w("")
w("写入类响应则是 `{\"success\": false, \"message\": \"...\"}`。两者都叫 `success`，"
  "取值含义一致，但 `data` 可能缺失。")
w("")

w("## 端点清单")
w("")
w("> 只读端点带实测判定；写类端点仅登记，**本技能不封装任何写操作**。")
w("")
def _isM2Only(r):
    return r["sources"] == ["m2"]


for ns in sorted(by_ns, key=lambda x: -(len(by_ns[x]["read"]) + len(by_ns[x]["write"]))):
    grp = by_ns[ns]
    tot = len(grp["read"]) + len(grp["write"])
    if tot < 1:
        continue
    # m2 专属行（新版 2026-10 新增的大头）走紧凑清单；涉及桌面端的保留全表格
    detail = [r for r in grp["read"] + grp["write"] if not _isM2Only(r)]
    m2only = [r for r in grp["read"] + grp["write"] if _isM2Only(r)]
    w("### `%s`（%d）" % (ns, tot))
    w("")
    if detail:
        dRead = [r for r in detail if r["kind"] == "read"]
        dWrite = [r for r in detail if r["kind"] == "write"]
        if dRead:
            w("**只读 %d**" % len(dRead))
            w("")
            w("| 端点 | 来源 | 实测 | 行数 | 顶层字段 |")
            w("|---|---|---|---|---|")
            for r in sorted(dRead, key=lambda x: x["endpoint"]):
                v = vmap.get(r["endpoint"])
                verdict = v["verdict"] if v else "—"
                rowsn = keys = "—"
                if v:
                    a = (v.get("attempts") or [{}])[0]
                    rowsn = str(a.get("rows")) if a.get("rows") is not None else "—"
                    keys = ", ".join(a.get("keys") or []) or a.get("type", "—")
                src = "+".join(SRC_CN.get(s, s) for s in r["sources"])
                w("| `%s` | %s | %s | %s | %s |" % (r["endpoint"], src, verdict, rowsn, keys))
            w("")
        if dWrite:
            w("**写类 %d**（不封装）" % len(dWrite))
            w("")
            w("| 端点 | 来源 |")
            w("|---|---|")
            for r in sorted(dWrite, key=lambda x: x["endpoint"]):
                src = "+".join(SRC_CN.get(s, s) for s in r["sources"])
                w("| `%s` | %s |" % (r["endpoint"], src))
            w("")
    if m2only:
        # 紧凑：命名空间前缀相同，只列 action 名；写类加 * 号
        w("m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：")
        w("")
        acts = sorted(
            ("%s%s" % (r["endpoint"].split("!")[1][:-len(".action")], "*" if r["kind"] == "write" else ""),
             r["kind"])
            for r in m2only)
        line, lines = "m2: ", []
        for a, _ in acts:
            if len(line) + len(a) + 3 > 96:
                lines.append(line.rstrip(" "))
                line = "    "
            line += "`%s`  " % a
        lines.append(line.rstrip(" "))
        w("```")
        for ln in lines:
            w(ln)
        w("```")
        w("`*` 后缀 = 写类。共 %d 个（读 %d / 写 %d）。"
          % (len(m2only), sum(1 for r in m2only if r["kind"] == "read"),
             sum(1 for r in m2only if r["kind"] == "write")))
        w("")

w("## 机器可读")
w("")
w("- `endpoints.json` — 全部 %d 个端点，含 `sources` / `kind` / `menus` / `files`" % len(rows))
w("- `validation.json` — %d 个只读端点的实测响应结构" % len(val))
w("- `menu_tree.json` — 菜单树原始响应（130 节点）")
w("- `desktop_endpoints.json` — 489 个桌面端端点，含来源 jsFile 与所属菜单名")
w("")

path = os.path.join(WD, "api.md")
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("api.md 已生成: %d 行, %.1f KB" % (len(out), os.path.getsize(path) / 1024))
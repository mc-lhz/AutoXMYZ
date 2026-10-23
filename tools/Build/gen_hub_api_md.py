"""从 HubEndpoints.py 注册表重生成 reference/hub-api.md 与各 Mixin 的同名 .md。

注册表是端点事实的唯一来源；本文档全部派生自它，不手写端点行。
用法：python tools/Build/gen_hub_api_md.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from StudentHub import HubEndpoints as HE  # noqa: E402

MIXIN_TITLE = {
    "HubTally": ("TallyMixin", "实时唱票"),
    "HubCampaign": ("CampaignMixin", "投票征集活动"),
    "HubDebate": ("DebateMixin", "辩论场管理"),
    "HubCampus": ("CampusMixin", "校区 / 楼宇 / 时段 / 用户检索"),
    "HubMuseum": ("MuseumMixin", "校园博物馆（事件/区块/标签/瞬间审核）"),
    "HubRating": ("RatingMixin", "评分社区（浏览/投稿/评分/评论/后台）"),
    "HubTicket": ("TicketMixin", "电子票务（活动/抢票/核销/审核）"),
    "HubVoices": ("VoicesMixin", "声音问答（提问/回答/举报/后台治理）"),
    "HubPortal": ("PortalMixin", "门户（横幅/年级绑定/文件/音乐/QQ音乐）"),
    "HubAccount": ("AccountMixin", "账号与会话（auth/user/sms/permissions）"),
    "HubMessage": ("MessageMixin", "站内消息（收件箱 + 管理端群发/模板）"),
}
DOM_OF = {dom: (mixin, title) for dom, (mixin, title) in {
    "HubTally": MIXIN_TITLE["HubTally"], "HubCampaign": MIXIN_TITLE["HubCampaign"],
    "HubDebate": MIXIN_TITLE["HubDebate"], "HubCampus": MIXIN_TITLE["HubCampus"],
    "HubMuseum": MIXIN_TITLE["HubMuseum"], "HubRating": MIXIN_TITLE["HubRating"],
    "HubTicket": MIXIN_TITLE["HubTicket"], "HubVoices": MIXIN_TITLE["HubVoices"],
    "HubPortal": MIXIN_TITLE["HubPortal"], "HubAccount": MIXIN_TITLE["HubAccount"],
    "HubMessage": MIXIN_TITLE["HubMessage"]}.items()}


def _probeMap():
    """reference/hub-probe.json（probe_hub_readonly.py 产物）→ {path: kind}。
    只标注 GET 行；文件缺失时返回空表（文档无探测列，不报错）。"""
    p = os.path.join(ROOT, "reference", "hub-probe.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        doc = json.load(f)
    return {k.split(" ", 1)[1]: v for k, v in doc.get("results", {}).items()
            if k.startswith("GET ")}


def mixinTable(dom, rows, probe=None):
    mixin, _ = DOM_OF[dom]
    hasProbe = bool(probe)
    head = "| 方法 | 路径 | 类别 | 包装方法 |" + (" 探测 |" if hasProbe else "")
    lines = [head, "|---|---|---|---|" + ("---|" if hasProbe else "")]
    for r in sorted(rows, key=lambda x: (x[1], x[0])):
        line = "| %s | `%s` | %s | `%s` |" % (r[0], r[1], r[2], r[4])
        if hasProbe:
            pk = probe.get(r[1], "")
            line += " %s |" % (PROBE_LABEL.get(pk, pk or "—"))
        lines.append(line)
    return "\n".join(lines) + "\n"


PROBE_LABEL = {
    "public": "公开",
    "auth": "需登录",
    "exists": "存在·需参数",
    "missing": "⚠️未挂载",
    "throttled": "限流未探",
    "net": "网络错误",
}


def main():
    rows = HE.REST_ENDPOINTS
    c = HE.counts()
    byDom = {}
    for r in rows:
        byDom.setdefault(r[3], []).append(r)

    out = ["# 学社 API 端点清单（xmyzstudent.com）",
           "",
           "> 来源：镜像 bundle 接口层（mc-lhz/XMYZStudent assets/）+ 实测探测。",
           "> 事实来源 `tools/StudentHub/HubEndpoints.py`；本文件由",
           "> `tools/Build/gen_hub_api_md.py` 派生，**不要手改端点行**。",
           "",
           "- REST 端点 **%d** 个（read %d / write %d）+ WS **%d** 条" % (
               c["rest"], c["read"], c["write"], c["ws"]),
           "- 基址 `https://api.xmyzstudent.com/api/v2`，Bearer token 鉴权",
           "- 信封 `{code, message, data}`，业务失败也是 HTTP 200，code!=200",
           "- 分页 `page` + `size`（部分端点 `pageSize`）",
           "",
           "## WebSocket",
           "",
           "| 路径 | 说明 |", "|---|---|"]
    for path, note in HE.WS_ROUTES:
        out.append("| `wss://api.xmyzstudent.com%s` | %s |" % (path, note))

    probe = _probeMap()
    if probe:
        from collections import Counter
        pc = Counter(probe.values())
        out.insert(9, "- 免凭据探测（GET %d 个）：公开 %d / 需登录 %d / 存在·需参数 %d"
                   " —— 详见 `reference/hub-probe.json`（probe_hub_readonly.py）"
                   % (sum(pc.values()), pc.get("public", 0), pc.get("auth", 0),
                      pc.get("exists", 0)))

    for dom in ["HubAccount", "HubPortal", "HubMessage", "HubTally", "HubCampaign",
                "HubTicket", "HubMuseum", "HubRating", "HubVoices", "HubCampus",
                "HubDebate"]:
        mixin, title = DOM_OF[dom]
        out += ["", "## %s —— %s" % (dom, title), "",
                mixinTable(dom, byDom.get(dom, []), probe)]

    dst = os.path.join(ROOT, "reference", "hub-api.md")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("reference/hub-api.md: %d bytes" % os.path.getsize(dst))

    # 各 Mixin 的同名 .md（契约：每 py 必须有同名 md；表格与 hub-api.md 同源同列）
    for dom, rowsDom in byDom.items():
        mixin, title = DOM_OF[dom]
        doc = ["# %s — %s" % (mixin, title), "",
               "包装 `%s` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。" % dom,
               "", mixinTable(dom, rowsDom, probe)]
        p = os.path.join(ROOT, "tools", "StudentHub", mixin + ".md")
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(doc))
    print("mixin md × %d" % len(byDom))
    return 0


if __name__ == "__main__":
    sys.exit(main())

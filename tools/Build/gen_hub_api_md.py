"""从 HubEndpoints.py 注册表重生成 reference/hub-api.md 与各 Mixin 的同名 .md。

注册表是端点事实的唯一来源；本文档全部派生自它，不手写端点行。
用法：python tools/Build/gen_hub_api_md.py
"""
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


def mixinTable(dom, rows):
    mixin, _ = DOM_OF[dom]
    lines = ["| 方法 | 路径 | 类别 | 包装方法 |", "|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (x[1], x[0])):
        lines.append("| %s | `%s` | %s | `%s` |" % (r[0], r[1], r[2], r[4]))
    return "\n".join(lines) + "\n"


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

    for dom in ["HubAccount", "HubPortal", "HubMessage", "HubTally", "HubCampaign",
                "HubTicket", "HubMuseum", "HubRating", "HubVoices", "HubCampus",
                "HubDebate"]:
        mixin, title = DOM_OF[dom]
        out += ["", "## %s —— %s" % (dom, title), "",
                mixinTable(dom, byDom.get(dom, []))]

    dst = os.path.join(ROOT, "reference", "hub-api.md")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("reference/hub-api.md: %d bytes" % os.path.getsize(dst))

    # 各 Mixin 的同名 .md（契约：每 py 必须有同名 md）
    for dom, rowsDom in byDom.items():
        mixin, title = DOM_OF[dom]
        doc = ["# %s — %s" % (mixin, title), "",
               "包装 `%s` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。" % dom,
               "", mixinTable(dom, rowsDom)]
        p = os.path.join(ROOT, "tools", "StudentHub", mixin + ".md")
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(doc))
    print("mixin md × %d" % len(byDom))
    return 0


if __name__ == "__main__":
    sys.exit(main())

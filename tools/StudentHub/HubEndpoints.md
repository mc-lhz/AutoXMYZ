# HubEndpoints — 学社端点注册表

端点事实的**唯一来源**：`REST_ENDPOINTS`（method, path, kind, domain, wrapper）+
`WS_ROUTES`。`reference/hub-api.md` 与各 Mixin 的 `.md` 表格全部由
`Build/gen_hub_api_md.py` 从本表派生。

## 约定

- 路径中 `{}` 为路径参数（调用时 `.format(id)`）
- `kind`: `read`=GET / `write`=其余。**语义与 xmyz 的 `endpoint_kind.is_write` 相反**：
  这里只是文档/统计标注，不做任何拦截（学社写能力是需求本身）
- `wrapper` 对应 `StudentHubClient` 上的方法名，命名保持站点前端接口层的
  语义导出名（`getAdminTallyActivities` 等），未包装端点可直接走 `c.get/post/...`
- 改端点契约的流程：改本表 → 跑 `Build/gen_hub_api_md.py` → 跑 `TestCases/TestHub.py`

## 统计

284 REST（read 114 / write 170）+ 2 WS，跨 12 个域（2026-10-24 对线上新版前端
index-D2vbWxba.js 重新对账：+24 admission/debate 操作员域，0 移除）：

HubAccount(29) HubAdmission(13) HubPortal(17) HubMessage(15) HubTally(11)
HubCampaign(19) HubTicket(20) HubMuseum(26) HubRating(74) HubVoices(21)
HubCampus(19) HubDebate(20)

## 清单来源

镜像仓库 `mc-lhz/XMYZStudent` 的 assets 接口层 chunk（tally/campaign/debate/dorm/
file/grade/museum/rating/ticket/voices + index 主 bundle + 5 个页面 chunk），
2026-10 提取；`GET /campus/captcha`、`/banners`、`/voices/status` 已在线实测。

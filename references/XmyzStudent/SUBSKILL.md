---
name: XmyzStudent
description: 厦门一中学生社区（xmyzstudent.com / api.xmyzstudent.com，学社）工具集。Use when the user mentions 学社、xmyzstudent、学生社区、唱票、实时唱票、抢票、票务、评分社区、声音问答、校园博物馆、辩论场、投票活动、纳新、admission，或要查/管理唱票活动、审核投稿、群发站内消息、管理博物馆与票务、给校园事物评分、发声音问答。
---

# XmyzStudent — 学社（xmyzstudent.com）

> **路径基准**：本文件位于 `references/XmyzStudent/`，下文 `tools/...`、`reference/...`
> 均相对本目录。从技能根执行时写完整前缀 `references/XmyzStudent/tools/...`。

> **能力定位**：站点是学生自建平台，**功能完备含写**（唱票/审核/发布是需求本身）。
> 删除类方法名显式含 `delete`，批量操作先自查 id。
> 纪律：未成年人个人信息（token/手机号/他人主页）不落仓库；会话文件在用户目录。

端点：**284 REST + 2 WS**（2026-10-24 对线上新前端 index-D2vbWxba 对账）。
事实唯一来源 `tools/StudentHub/HubEndpoints.py`；`reference/hub-api.md` 由
`tools/Build/gen_hub_api_md.py` 派生（改注册表必须重跑，TestHub 会查漂移）。

## 认证拓扑（凭据与 CampusNet/XinYiWo 同源）

学社登录的 `loginType:"campus"` 是**学社服务端拿着同一组学号密码回调 CampusNet 校验**；
客户端不需要 CampusNet 会话，只需同一凭据 + 学社**自己的验证码**（`GET /campus/captcha`）。

```bash
python tools/StudentHub/HubSession.py captcha                       # ① 学社验证码图（jsessionId 暂存）
python tools/StudentHub/HubSession.py campus -a <学号> -p <密码> --code ab12
python tools/StudentHub/HubSession.py campus -a <学号> -p <密码> --ocr 6   # OCR 兜底
python tools/StudentHub/HubSession.py normal|sms|token ...          # 其它方式
python tools/StudentHub/HubSession.py check
```

> ⚠️ 安全提示：学社登录会把密码发给学社服务器并由其转发 CampusNet
> （站点设计如此）——不要在不可信网络下使用学社登录态。

会话在 `%LOCALAPPDATA%\AutoXMYZ\hub_session.json`。

## 使用

```python
import sys; sys.path.insert(0, "tools")     # 从 references/XmyzStudent 起
from StudentHubClient import StudentHubClient
c = StudentHubClient()
c.healthCheck(); c.summary()
c.getMyProfile(); c.getUnreadMessageCount(); c.getMyPermissions()

# 唱票（管理需 tally.manage 权限）/ 大屏 WS
c.getAdminTallyActivities(); c.voteAdminTallyCandidates(candidateId, 10)
c.wsSnapshots("/ws/tally/activity/%d" % activityId, print, seconds=10)

# 评分社区 / 声音问答 / 票务 / 纳新 / 辩论
c.searchRatingItems("沙茶面"); c.getRatingCommunityRatingItemsById(id)
c.getVoiceQuestions(); c.createVoicesQuestionsAnswers(questionId, "内容")
c.getPublicTicketActivities(); c.getTicketsMy()
c.getAdmissionStatus()
```

## 契约要点

- 信封 `{code,message,data}`；**业务失败也是 HTTP 200**，`code!=200` 抛 `HubError`
  （401 → `HubAuthError`，重登，不要换参重试）
- 分页 `page` + `size`（部分 `pageSize`）
- 每 py 同名 md；生成方法带 payload 参数时必须真发 body（TestHub 有防回归闸）
- 端点事实只改 `HubEndpoints.py` → 重跑 `tools/Build/gen_hub_api_md.py` → `tools/TestCases/TestHub.py`

## 命令速查

```bash
python tools/TestCases/TestHub.py            # 离线契约 15 项（含文档反漂移/防回归）
python tools/TestCases/TestHubSmoke.py       # 具名方法冒烟（GET+无必填，46 法）
python tools/Build/probe_hub_readonly.py     # 只读端点全量探测（二遍慢速重探）
python tools/Build/gen_hub_api_md.py         # 重生成 reference/hub-api.md 与各 Mixin.md
```

## 注意事项

- 管理端点（tally/museum/banner/messages 等）需要对应 `*.manage` 权限，否则服务端 403
- 限速默认 150ms；批量请求后网关会 502 限流——探测需慢速重探，别把 502 当 404
- `reference/` 体积上限 150KB（当前 ≈32KB）
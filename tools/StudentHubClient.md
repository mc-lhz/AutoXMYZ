# StudentHubClient — 学社门面

`xmyzstudent.com`（厦门一中学生社区）客户端。多源站聚合架构的第二块拼图：

| 门面 | 源站 | 能力 |
|---|---|---|
| `XMYZClient` | xmyz.xmedu.cn | 纯只读（`_guard` 强制） |
| `StudentHubClient` | xmyzstudent.com | **功能完备**（学生自建平台，写操作是需求本身） |

## 用法

```python
import sys; sys.path.insert(0, "tools")
from StudentHubClient import StudentHubClient

c = StudentHubClient()               # 自动读 %LOCALAPPDATA%\AutoXMYZ\hub_session.json
c = StudentHubClient(token="<Bearer>")
c.healthCheck()                      # /user/profile 有 username 即有效
c.summary()                          # 跨域摘要（本人/未读/权限/声音/横幅/校区/唱票）

# 高频示例
c.voteAdminTallyCandidates(candidateId, delta=10)   # 唱票 +10
c.getAdminTallyActivitiesRecords(activityId)        # 唱票操作流水
c.getMyTickets()                                    # 我的票
c.searchRatingItems(keyword="食堂")                  # 评分社区搜索
c.post(c.BASE + "/任意未包装端点", json={...})        # 未包装端点直接走传输层
```

## 组合结构

12 个业务 mixin（Account/Admission/Portal/Message/Tally/Campaign/Ticket/Museum/
Rating/Voices/Campus/Debate）+ `HubHttp`（末位基类）。方法名 = 站点前端接口层语义导出名，
共 284 个（见 `StudentHub/HubEndpoints.py` 与 `reference/hub-api.md`）。

## 红线与纪律

- 写操作虽不被拦截，但**删除类方法名显式含 delete**；批量删除（`batch`）调用前
  自查 id 列表
- 未成年人个人信息（token、手机号、他人主页）不落仓库；会话/token 同 xmyz 规则
  存用户目录
- 遇 `HubAuthError`（401）重新登录，不要换参数重试
- 限速默认 150ms，批量脚本勿调 0

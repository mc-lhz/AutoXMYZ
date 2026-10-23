# DebateMixin — 辩论场管理

包装 `HubDebate` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/debate/rounds` | read | `getAdminDebateRounds` | 需登录 |
| POST | `/admin/debate/rounds` | write | `createAdminDebateRounds` | 需登录 |
| DELETE | `/admin/debate/rounds/{}` | write | `deleteAdminDebateRounds` | — |
| PUT | `/admin/debate/rounds/{}` | write | `updateAdminDebateRounds` | — |
| PUT | `/admin/debate/rounds/{}/active` | write | `updateAdminDebateRoundsActive` | — |
| PUT | `/admin/debate/rounds/{}/lock` | write | `lockAdminDebateRounds` | — |
| PUT | `/admin/debate/rounds/{}/regenerate-password` | write | `regeneratePasswordAdminDebateRounds` | — |
| PUT | `/admin/debate/rounds/{}/reset` | write | `resetAdminDebateRounds` | — |
| PUT | `/admin/debate/rounds/{}/unlock` | write | `unlockAdminDebateRounds` | — |
| GET | `/debate/active` | read | `getActiveDebateRounds` | 公开 |
| GET | `/debate/me` | read | `getMyDebateIdentity` | 公开 |
| PUT | `/debate/operator/rounds/{}` | write | `updateDebateOperatorRound` | — |
| PUT | `/debate/operator/rounds/{}/active` | write | `activateDebateOperatorRound` | — |
| PUT | `/debate/operator/rounds/{}/lock` | write | `lockDebateOperatorRound` | — |
| PUT | `/debate/operator/rounds/{}/reset` | write | `resetDebateOperatorRound` | — |
| POST | `/debate/operator/verify` | write | `verifyDebateOperator` | — |
| GET | `/debate/results/{}` | read | `getDebateResultsById` | 存在·需参数 |
| GET | `/debate/round/{}` | read | `getDebateRoundById` | 存在·需参数 |
| POST | `/debate/vote` | write | `submitDebateVote` | — |
| GET | `/debate/wechat/login` | read | `debateWechatLoginUrl` | 存在·需参数 |

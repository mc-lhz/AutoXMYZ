# MessageMixin — 站内消息（收件箱 + 管理端群发/模板）

包装 `HubMessage` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/messages` | read | `getAdminMessages` | 需登录 |
| DELETE | `/admin/messages/batch` | write | `deleteAdminMessagesBatch` | — |
| POST | `/admin/messages/broadcast` | write | `broadcastAdminMessage` | — |
| POST | `/admin/messages/send` | write | `sendAdminMessage` | — |
| GET | `/admin/messages/stats` | read | `getAdminMessageStats` | 需登录 |
| GET | `/admin/messages/templates` | read | `getAdminMessageTemplates` | 需登录 |
| POST | `/admin/messages/templates` | write | `createAdminMessageTemplate` | 需登录 |
| DELETE | `/admin/messages/templates/{}` | write | `deleteAdminMessageTemplate` | — |
| PUT | `/admin/messages/templates/{}` | write | `updateAdminMessageTemplate` | — |
| DELETE | `/admin/messages/{}` | write | `deleteAdminMessage` | — |
| GET | `/messages` | read | `getMessages` | 需登录 |
| PUT | `/messages/read-all` | write | `markAllMessagesRead` | — |
| GET | `/messages/unread-count` | read | `getUnreadMessageCount` | 需登录 |
| DELETE | `/messages/{}` | write | `deleteMessage` | — |
| PUT | `/messages/{}/read` | write | `markMessageRead` | — |

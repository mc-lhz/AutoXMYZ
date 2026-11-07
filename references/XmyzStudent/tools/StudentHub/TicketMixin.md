# TicketMixin — 电子票务（活动/抢票/核销/审核）

包装 `HubTicket` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/ticket/activities` | read | `getAdminTicketActivities` | 需登录 |
| POST | `/admin/ticket/activities` | write | `createAdminTicketActivities` | 需登录 |
| DELETE | `/admin/ticket/activities/{}` | write | `deleteAdminTicketActivities` | 需登录 |
| GET | `/admin/ticket/activities/{}` | read | `getAdminTicketActivitiesById` | 需登录 |
| PUT | `/admin/ticket/activities/{}` | write | `updateAdminTicketActivities` | 需登录 |
| GET | `/admin/ticket/activities/{}/review` | read | `getAdminTicketReview` | 需登录 |
| POST | `/admin/ticket/activities/{}/sessions` | write | `createAdminTicketActivitiesSessions` | — |
| GET | `/admin/ticket/activities/{}/stats` | read | `getAdminTicketActivitiesStats` | 需登录 |
| POST | `/admin/ticket/activities/{}/status` | write | `createAdminTicketActivitiesStatus` | — |
| DELETE | `/admin/ticket/sessions/{}` | write | `deleteAdminTicketSessions` | — |
| PUT | `/admin/ticket/sessions/{}` | write | `updateAdminTicketSessions` | — |
| POST | `/admin/ticket/tickets/batch-review` | write | `batchReviewAdminTicketTickets` | — |
| POST | `/admin/ticket/tickets/{}/review` | write | `reviewAdminTicketTickets` | — |
| GET | `/admin/ticket/verify` | read | `getTicketByCode` | 需登录 |
| POST | `/admin/ticket/verify/use` | write | `useAdminTicketVerify` | — |
| GET | `/ticket-activities` | read | `getPublicTicketActivities` | 需登录 |
| GET | `/ticket-activities/{}` | read | `getTicketActivitiesById` | 需登录 |
| POST | `/tickets/grab` | write | `grabTickets` | — |
| GET | `/tickets/my` | read | `getTicketsMy` | 需登录 |
| GET | `/tickets/my/activity/{}` | read | `getTicketsMyActivityById` | 需登录 |

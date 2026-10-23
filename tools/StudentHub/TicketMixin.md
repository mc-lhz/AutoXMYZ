# TicketMixin — 电子票务（活动/抢票/核销/审核）

包装 `HubTicket` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/ticket/activities` | read | `getAdminTicketActivities` |
| POST | `/admin/ticket/activities` | write | `createAdminTicketActivities` |
| DELETE | `/admin/ticket/activities/{}` | write | `deleteAdminTicketActivities` |
| GET | `/admin/ticket/activities/{}` | read | `getAdminTicketActivitiesById` |
| PUT | `/admin/ticket/activities/{}` | write | `updateAdminTicketActivities` |
| GET | `/admin/ticket/activities/{}/review` | read | `getAdminTicketReview` |
| POST | `/admin/ticket/activities/{}/sessions` | write | `createAdminTicketActivitiesSessions` |
| GET | `/admin/ticket/activities/{}/stats` | read | `getAdminTicketActivitiesStats` |
| POST | `/admin/ticket/activities/{}/status` | write | `createAdminTicketActivitiesStatus` |
| DELETE | `/admin/ticket/sessions/{}` | write | `deleteAdminTicketSessions` |
| PUT | `/admin/ticket/sessions/{}` | write | `updateAdminTicketSessions` |
| POST | `/admin/ticket/tickets/batch-review` | write | `batchReviewAdminTicketTickets` |
| POST | `/admin/ticket/tickets/{}/review` | write | `reviewAdminTicketTickets` |
| GET | `/admin/ticket/verify` | read | `getTicketByCode` |
| POST | `/admin/ticket/verify/use` | write | `useAdminTicketVerify` |
| GET | `/ticket-activities` | read | `getPublicTicketActivities` |
| GET | `/ticket-activities/{}` | read | `getTicketActivitiesById` |
| POST | `/tickets/grab` | write | `grabTickets` |
| GET | `/tickets/my` | read | `getTicketsMy` |
| GET | `/tickets/my/activity/{}` | read | `getTicketsMyActivityById` |

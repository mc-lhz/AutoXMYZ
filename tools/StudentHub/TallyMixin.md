# TallyMixin — 实时唱票

包装 `HubTally` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/tally/activities` | read | `getAdminTallyActivities` |
| POST | `/admin/tally/activities` | write | `createAdminTallyActivities` |
| DELETE | `/admin/tally/activities/{}` | write | `deleteAdminTallyActivities` |
| GET | `/admin/tally/activities/{}` | read | `getAdminTallyActivitiesById` |
| PUT | `/admin/tally/activities/{}` | write | `updateAdminTallyActivities` |
| POST | `/admin/tally/activities/{}/candidates` | write | `createAdminTallyActivitiesCandidates` |
| GET | `/admin/tally/activities/{}/records` | read | `getAdminTallyActivitiesRecords` |
| POST | `/admin/tally/activities/{}/undo` | write | `undoAdminTallyActivities` |
| DELETE | `/admin/tally/candidates/{}` | write | `deleteAdminTallyCandidates` |
| PUT | `/admin/tally/candidates/{}` | write | `updateAdminTallyCandidates` |
| POST | `/admin/tally/candidates/{}/vote` | write | `voteAdminTallyCandidates` |

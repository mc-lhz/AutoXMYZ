# CampusMixin — 校区 / 楼宇 / 时段 / 用户检索

包装 `HubCampus` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| POST | `/admin/buildings` | write | `createAdminBuildings` |
| DELETE | `/admin/buildings/time-periods` | write | `deleteAdminBuildingsTimePeriods` |
| POST | `/admin/buildings/time-periods` | write | `createAdminBuildingsTimePeriods` |
| DELETE | `/admin/buildings/{}` | write | `deleteAdminBuildings` |
| PUT | `/admin/buildings/{}` | write | `updateAdminBuildings` |
| POST | `/admin/campuses` | write | `createAdminCampuses` |
| DELETE | `/admin/campuses/{}` | write | `deleteAdminCampuses` |
| PUT | `/admin/campuses/{}` | write | `updateAdminCampuses` |
| POST | `/admin/time-periods` | write | `createAdminResourceTimePeriods` |
| DELETE | `/admin/time-periods/{}` | write | `deleteAdminResourceTimePeriods` |
| PUT | `/admin/time-periods/{}` | write | `updateAdminResourceTimePeriods` |
| GET | `/admin/users/search/by-campus-account` | read | `searchUsersByCampusAccount` |
| GET | `/admin/users/search/by-campus-name` | read | `searchUsersByCampusName` |
| GET | `/admin/users/search/by-user` | read | `searchUsersByUser` |
| GET | `/buildings` | read | `getBuildings` |
| GET | `/buildings/{}/time-periods` | read | `getBuildingsTimePeriods` |
| GET | `/campuses` | read | `getCampuses` |
| GET | `/campuses/{}/buildings` | read | `getCampusesBuildingsById` |
| GET | `/time-periods` | read | `getResourceTimePeriods` |

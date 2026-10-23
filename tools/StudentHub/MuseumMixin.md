# MuseumMixin — 校园博物馆（事件/区块/标签/瞬间审核）

包装 `HubMuseum` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/museum/events` | read | `getAdminMuseumEvents` |
| POST | `/admin/museum/events` | write | `createAdminMuseumEvents` |
| POST | `/admin/museum/events/batch` | write | `batchAdminMuseumEvents` |
| DELETE | `/admin/museum/events/{}` | write | `deleteAdminMuseumEvents` |
| GET | `/admin/museum/events/{}` | read | `getAdminMuseumEventsById` |
| PUT | `/admin/museum/events/{}` | write | `updateAdminMuseumEvents` |
| GET | `/admin/museum/events/{}/blocks` | read | `getAdminMuseumEventsBlocks` |
| POST | `/admin/museum/events/{}/blocks` | write | `createAdminMuseumEventsBlocks` |
| POST | `/admin/museum/events/{}/blocks/sort` | write | `sortAdminMuseumEventsBlocks` |
| DELETE | `/admin/museum/events/{}/blocks/{}` | write | `deleteAdminMuseumEventsBlocks` |
| PUT | `/admin/museum/events/{}/blocks/{}` | write | `updateAdminMuseumEventsBlocks` |
| POST | `/admin/museum/events/{}/feature` | write | `featureAdminMuseumEvents` |
| POST | `/admin/museum/events/{}/publish` | write | `publishAdminMuseumEvents` |
| POST | `/admin/museum/events/{}/unfeature` | write | `unfeatureAdminMuseumEvents` |
| POST | `/admin/museum/events/{}/unpublish` | write | `unpublishAdminMuseumEvents` |
| GET | `/admin/museum/moments` | read | `getAdminMuseumMoments` |
| POST | `/admin/museum/moments/batch` | write | `batchAdminMuseumMoments` |
| DELETE | `/admin/museum/moments/{}` | write | `deleteAdminMuseumMoments` |
| POST | `/admin/museum/moments/{}/approve` | write | `approveAdminMuseumMoments` |
| POST | `/admin/museum/moments/{}/reject` | write | `rejectAdminMuseumMoments` |
| POST | `/admin/museum/moments/{}/takedown` | write | `takedownAdminMuseumMoments` |
| GET | `/admin/museum/tags` | read | `getAdminMuseumTags` |
| POST | `/admin/museum/tags` | write | `createAdminMuseumTags` |
| DELETE | `/admin/museum/tags/{}` | write | `deleteAdminMuseumTags` |
| PUT | `/admin/museum/tags/{}` | write | `updateAdminMuseumTags` |
| POST | `/admin/museum/tags/{}/toggle-status` | write | `toggleStatusAdminMuseumTags` |

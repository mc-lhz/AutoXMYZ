# VoicesMixin — 声音问答（提问/回答/举报/后台治理）

包装 `HubVoices` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/voices/answers` | read | `getAdminVoicesAnswers` | 需登录 |
| PUT | `/admin/voices/answers/{}/restore` | write | `restoreAdminVoicesAnswers` | — |
| PUT | `/admin/voices/answers/{}/takedown` | write | `takedownAdminVoicesAnswers` | — |
| GET | `/admin/voices/questions` | read | `getAdminVoicesQuestions` | 需登录 |
| PUT | `/admin/voices/questions/{}/restore` | write | `restoreAdminVoicesQuestions` | — |
| PUT | `/admin/voices/questions/{}/takedown` | write | `takedownAdminVoicesQuestions` | — |
| GET | `/admin/voices/reports` | read | `getAdminVoicesReports` | 需登录 |
| PUT | `/admin/voices/reports/{}/handle` | write | `handleAdminVoicesReports` | — |
| GET | `/admin/voices/stats` | read | `getAdminVoicesStats` | 需登录 |
| POST | `/voices/answers/{}/like` | write | `likeVoicesAnswers` | — |
| POST | `/voices/identity` | write | `createVoicesIdentity` | — |
| GET | `/voices/mine/answers` | read | `getMyAnswers` | 需登录 |
| GET | `/voices/mine/favorites` | read | `getMyFavorites` | 需登录 |
| GET | `/voices/mine/questions` | read | `getMyQuestions` | 需登录 |
| GET | `/voices/questions` | read | `getVoiceQuestions` | 公开 |
| POST | `/voices/questions` | write | `createVoicesQuestions` | 公开 |
| GET | `/voices/questions/{}` | read | `getVoicesQuestions2` | 存在·需参数 |
| POST | `/voices/questions/{}/answers` | write | `createVoicesQuestionsAnswers` | — |
| POST | `/voices/questions/{}/favorite` | write | `favoriteVoicesQuestions` | — |
| POST | `/voices/report` | write | `reportVoices` | — |
| GET | `/voices/status` | read | `getVoicesStatus` | 公开 |

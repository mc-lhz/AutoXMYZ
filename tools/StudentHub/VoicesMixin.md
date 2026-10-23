# VoicesMixin — 声音问答（提问/回答/举报/后台治理）

包装 `HubVoices` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/voices/answers` | read | `getAdminVoicesAnswers` |
| PUT | `/admin/voices/answers/{}/restore` | write | `restoreAdminVoicesAnswers` |
| PUT | `/admin/voices/answers/{}/takedown` | write | `takedownAdminVoicesAnswers` |
| GET | `/admin/voices/questions` | read | `getAdminVoicesQuestions` |
| PUT | `/admin/voices/questions/{}/restore` | write | `restoreAdminVoicesQuestions` |
| PUT | `/admin/voices/questions/{}/takedown` | write | `takedownAdminVoicesQuestions` |
| GET | `/admin/voices/reports` | read | `getAdminVoicesReports` |
| PUT | `/admin/voices/reports/{}/handle` | write | `handleAdminVoicesReports` |
| GET | `/admin/voices/stats` | read | `getAdminVoicesStats` |
| POST | `/voices/answers/{}/like` | write | `likeVoicesAnswers` |
| POST | `/voices/identity` | write | `createVoicesIdentity` |
| GET | `/voices/mine/answers` | read | `getMyAnswers` |
| GET | `/voices/mine/favorites` | read | `getMyFavorites` |
| GET | `/voices/mine/questions` | read | `getMyQuestions` |
| GET | `/voices/questions` | read | `getVoiceQuestions` |
| POST | `/voices/questions` | write | `createVoicesQuestions` |
| GET | `/voices/questions/{}` | read | `getVoicesQuestions2` |
| POST | `/voices/questions/{}/answers` | write | `createVoicesQuestionsAnswers` |
| POST | `/voices/questions/{}/favorite` | write | `favoriteVoicesQuestions` |
| POST | `/voices/report` | write | `reportVoices` |
| GET | `/voices/status` | read | `getVoicesStatus` |

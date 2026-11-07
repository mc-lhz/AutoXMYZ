# 学社 API 端点清单（xmyzstudent.com）

> 来源：镜像 bundle 接口层（mc-lhz/XMYZStudent assets/）+ 实测探测。
> 事实来源 `tools/StudentHub/HubEndpoints.py`；本文件由
> `tools/Build/gen_hub_api_md.py` 派生，**不要手改端点行**。

- REST 端点 **284** 个（read 114 / write 170）+ WS **2** 条
- 基址 `https://api.xmyzstudent.com/api/v2`，Bearer token 鉴权
- 信封 `{code, message, data}`，业务失败也是 HTTP 200，code!=200
- 免凭据探测（GET 114 个）：公开 14 / 需登录 83 / 存在·需参数 17 —— 详见 `reference/hub-probe.json`（probe_hub_readonly.py）
- 分页 `page` + `size`（部分端点 `pageSize`）

## WebSocket

| 路径 | 说明 |
|---|---|
| `wss://api.xmyzstudent.com/ws/tally/activity/{id}` | 唱票大屏快照（全量推送，单向） |
| `wss://api.xmyzstudent.com/ws/debate/round/{id}` | 辩论场实时消息 |

## HubAccount —— 账号与会话（auth/user/sms/permissions）

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| POST | `/auth/login` | write | `login` | — |
| POST | `/auth/qq-bind` | write | `qqBind` | — |
| POST | `/auth/qq-login` | write | `qqLogin` | — |
| POST | `/auth/qq-register` | write | `qqRegister` | — |
| GET | `/auth/qq/authorize-url` | read | `getQQAuthorizeUrl` | 公开 |
| POST | `/auth/register` | write | `register` | — |
| GET | `/permissions/my` | read | `getMyPermissions` | 需登录 |
| POST | `/sms/bind` | write | `bindSms` | — |
| GET | `/sms/binding` | read | `getSmsBinding` | 需登录 |
| POST | `/sms/login` | write | `smsLogin` | — |
| POST | `/sms/send` | write | `sendSmsCode` | — |
| DELETE | `/sms/unbind` | write | `unbindSms` | — |
| POST | `/user/avatar` | write | `uploadMyAvatar` | — |
| POST | `/user/bind-campus` | write | `bindCampus` | — |
| POST | `/user/bind-qq` | write | `bindQQ` | — |
| GET | `/user/campus-binding` | read | `getCampusBinding` | 需登录 |
| GET | `/user/has-password` | read | `getHasPassword` | 需登录 |
| PUT | `/user/password` | write | `updatePassword` | — |
| GET | `/user/privacy-settings` | read | `getPrivacySettings` | 需登录 |
| PUT | `/user/privacy-settings` | write | `updatePrivacySettings` | 需登录 |
| GET | `/user/profile` | read | `getMyProfile` | 需登录 |
| PUT | `/user/profile` | write | `updateMyProfile` | 需登录 |
| GET | `/user/qq-binding` | read | `getQQBinding` | 需登录 |
| GET | `/user/qq/authorize-url` | read | `getUserQQAuthorizeUrl` | 需登录 |
| POST | `/user/rebind-campus` | write | `rebindCampus` | — |
| DELETE | `/user/unbind-campus` | write | `unbindCampus` | — |
| DELETE | `/user/unbind-qq` | write | `unbindQQ` | — |
| GET | `/user/users/{}/avatar` | read | `getUserAvatar` | 存在·需参数 |
| GET | `/user/users/{}/profile` | read | `getUserProfile` | 存在·需参数 |


## HubAdmission —— 纳新/准入（分组/成员/豁免/扫码 + 用户验证）

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| POST | `/admin/admission/exempt` | write | `exemptAdminAdmission` | — |
| GET | `/admin/admission/groups` | read | `getAdminAdmissionGroups` | 需登录 |
| POST | `/admin/admission/kick` | write | `kickAdminAdmission` | — |
| GET | `/admin/admission/members` | read | `getAdminAdmissionMembers` | 需登录 |
| POST | `/admin/admission/resend` | write | `resendAdminAdmission` | — |
| POST | `/admin/admission/revoke-exempt` | write | `revokeExemptAdminAdmission` | — |
| GET | `/admin/admission/scan` | read | `scanAdminAdmission` | 需登录 |
| POST | `/admin/admission/scan-fix` | write | `fixAdminAdmissionScan` | — |
| POST | `/admission/confirm` | write | `confirmAdmission` | — |
| GET | `/admission/qq-profile` | read | `getAdmissionQQProfile` | 存在·需参数 |
| GET | `/admission/status` | read | `getAdmissionStatus` | 公开 |
| GET | `/admission/token/{}` | read | `getAdmissionTokenByQQ` | 存在·需参数 |
| POST | `/admission/verify` | write | `verifyAdmission` | — |


## HubPortal —— 门户（横幅/年级绑定/文件/音乐/QQ音乐）

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/banners` | read | `getAdminBanners` | 需登录 |
| POST | `/admin/banners` | write | `createAdminBanner` | 需登录 |
| DELETE | `/admin/banners/{}` | write | `deleteAdminBanner` | — |
| PUT | `/admin/banners/{}` | write | `updateAdminBanner` | — |
| POST | `/admin/banners/{}/toggle-status` | write | `toggleAdminBannerStatus` | — |
| GET | `/banners` | read | `getPublicBanners` | 公开 |
| GET | `/campus/captcha` | read | `getCampusCaptcha` | 公开 |
| POST | `/files/upload` | write | `uploadFile` | — |
| POST | `/grade/bind` | write | `bindGrade` | — |
| GET | `/grade/exams` | read | `getGradeExams` | 需登录 |
| GET | `/grade/exams/{}` | read | `getGradeExamsById` | 需登录 |
| GET | `/grade/status` | read | `getGradeStatus` | 需登录 |
| DELETE | `/grade/unbind` | write | `unbindGrade` | — |
| GET | `/qqmusic/auth/qrcode` | read | `getQQMusicQrCode` | 公开 |
| GET | `/qqmusic/auth/qrcode/status` | read | `getQQMusicQrStatus` | 存在·需参数 |
| GET | `/qqmusic/auth/status` | read | `getQQMusicAuthStatus` | 公开 |
| GET | `/qqmusic/qualities` | read | `getQQMusicQualities` | 公开 |


## HubMessage —— 站内消息（收件箱 + 管理端群发/模板）

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


## HubTally —— 实时唱票

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/tally/activities` | read | `getAdminTallyActivities` | 需登录 |
| POST | `/admin/tally/activities` | write | `createAdminTallyActivities` | 需登录 |
| DELETE | `/admin/tally/activities/{}` | write | `deleteAdminTallyActivities` | 需登录 |
| GET | `/admin/tally/activities/{}` | read | `getAdminTallyActivitiesById` | 需登录 |
| PUT | `/admin/tally/activities/{}` | write | `updateAdminTallyActivities` | 需登录 |
| POST | `/admin/tally/activities/{}/candidates` | write | `createAdminTallyActivitiesCandidates` | — |
| GET | `/admin/tally/activities/{}/records` | read | `getAdminTallyActivitiesRecords` | 需登录 |
| POST | `/admin/tally/activities/{}/undo` | write | `undoAdminTallyActivities` | — |
| DELETE | `/admin/tally/candidates/{}` | write | `deleteAdminTallyCandidates` | — |
| PUT | `/admin/tally/candidates/{}` | write | `updateAdminTallyCandidates` | — |
| POST | `/admin/tally/candidates/{}/vote` | write | `voteAdminTallyCandidates` | — |


## HubCampaign —— 投票征集活动

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| POST | `/admin/campaigns` | write | `createAdminCampaigns` | — |
| PUT | `/admin/campaigns/{}` | write | `updateAdminCampaigns` | — |
| POST | `/admin/campaigns/{}/activate` | write | `activateAdminCampaigns` | — |
| POST | `/admin/campaigns/{}/close` | write | `closeAdminCampaigns` | — |
| POST | `/admin/campaigns/{}/stage-operation` | write | `stageOperationAdminCampaigns` | — |
| GET | `/admin/review/campaigns/{}/submissions` | read | `getAdminReviewCampaignsSubmissions` | 需登录 |
| DELETE | `/admin/review/submissions` | write | `deleteAdminReviewSubmissions` | — |
| GET | `/admin/voting/campaigns/{}/results` | read | `getAdminVotingCampaignsResults` | 需登录 |
| GET | `/campaigns` | read | `getCampaigns` | 需登录 |
| GET | `/campaigns/{}` | read | `getCampaignsById` | 需登录 |
| GET | `/music/detail` | read | `getMusicDetail` | 需登录 |
| GET | `/music/search` | read | `searchMusic` | 需登录 |
| GET | `/music/url` | read | `getMusicUrl` | 需登录 |
| POST | `/submissions` | write | `createResourceSubmissions` | — |
| GET | `/submissions/campaigns/{}` | read | `getSubmissionsCampaignsById` | 需登录 |
| GET | `/voting/campaigns/{}/config` | read | `getVotingCampaignsConfig` | 需登录 |
| GET | `/voting/campaigns/{}/my-votes` | read | `getVotingCampaignsMyVotes` | 需登录 |
| GET | `/voting/campaigns/{}/options` | read | `getVotingOptions` | 需登录 |
| POST | `/voting/vote` | write | `voteVoting` | — |


## HubTicket —— 电子票务（活动/抢票/核销/审核）

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


## HubMuseum —— 校园博物馆（事件/区块/标签/瞬间审核）

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/museum/events` | read | `getAdminMuseumEvents` | 需登录 |
| POST | `/admin/museum/events` | write | `createAdminMuseumEvents` | 需登录 |
| POST | `/admin/museum/events/batch` | write | `batchAdminMuseumEvents` | — |
| DELETE | `/admin/museum/events/{}` | write | `deleteAdminMuseumEvents` | 需登录 |
| GET | `/admin/museum/events/{}` | read | `getAdminMuseumEventsById` | 需登录 |
| PUT | `/admin/museum/events/{}` | write | `updateAdminMuseumEvents` | 需登录 |
| GET | `/admin/museum/events/{}/blocks` | read | `getAdminMuseumEventsBlocks` | 需登录 |
| POST | `/admin/museum/events/{}/blocks` | write | `createAdminMuseumEventsBlocks` | 需登录 |
| POST | `/admin/museum/events/{}/blocks/sort` | write | `sortAdminMuseumEventsBlocks` | — |
| DELETE | `/admin/museum/events/{}/blocks/{}` | write | `deleteAdminMuseumEventsBlocks` | — |
| PUT | `/admin/museum/events/{}/blocks/{}` | write | `updateAdminMuseumEventsBlocks` | — |
| POST | `/admin/museum/events/{}/feature` | write | `featureAdminMuseumEvents` | — |
| POST | `/admin/museum/events/{}/publish` | write | `publishAdminMuseumEvents` | — |
| POST | `/admin/museum/events/{}/unfeature` | write | `unfeatureAdminMuseumEvents` | — |
| POST | `/admin/museum/events/{}/unpublish` | write | `unpublishAdminMuseumEvents` | — |
| GET | `/admin/museum/moments` | read | `getAdminMuseumMoments` | 需登录 |
| POST | `/admin/museum/moments/batch` | write | `batchAdminMuseumMoments` | — |
| DELETE | `/admin/museum/moments/{}` | write | `deleteAdminMuseumMoments` | — |
| POST | `/admin/museum/moments/{}/approve` | write | `approveAdminMuseumMoments` | — |
| POST | `/admin/museum/moments/{}/reject` | write | `rejectAdminMuseumMoments` | — |
| POST | `/admin/museum/moments/{}/takedown` | write | `takedownAdminMuseumMoments` | — |
| GET | `/admin/museum/tags` | read | `getAdminMuseumTags` | 需登录 |
| POST | `/admin/museum/tags` | write | `createAdminMuseumTags` | 需登录 |
| DELETE | `/admin/museum/tags/{}` | write | `deleteAdminMuseumTags` | — |
| PUT | `/admin/museum/tags/{}` | write | `updateAdminMuseumTags` | — |
| POST | `/admin/museum/tags/{}/toggle-status` | write | `toggleStatusAdminMuseumTags` | — |


## HubRating —— 评分社区（浏览/投稿/评分/评论/后台）

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| GET | `/admin/rating-community/categories` | read | `getCategoriesById2` | 需登录 |
| POST | `/admin/rating-community/categories` | write | `createCategories` | 需登录 |
| DELETE | `/admin/rating-community/categories/{}` | write | `deleteCategories` | 需登录 |
| GET | `/admin/rating-community/categories/{}` | read | `getCategoriesById` | 需登录 |
| PUT | `/admin/rating-community/categories/{}` | write | `updateCategories` | 需登录 |
| DELETE | `/admin/rating-community/categories/{}/image` | write | `deleteCategoriesImage` | — |
| PUT | `/admin/rating-community/categories/{}/status` | write | `updateCategoriesStatus` | — |
| GET | `/admin/rating-community/collections` | read | `getCollectionsById` | 需登录 |
| POST | `/admin/rating-community/collections` | write | `createCollections` | 需登录 |
| DELETE | `/admin/rating-community/collections/{}` | write | `deleteCollections` | 需登录 |
| GET | `/admin/rating-community/collections/{}` | read | `getCollectionsById2` | 需登录 |
| PUT | `/admin/rating-community/collections/{}` | write | `updateCollections` | 需登录 |
| DELETE | `/admin/rating-community/collections/{}/image` | write | `deleteCollectionsImage` | — |
| GET | `/admin/rating-community/collections/{}/items` | read | `getCollectionsItemsById` | 需登录 |
| POST | `/admin/rating-community/collections/{}/items` | write | `createCollectionsItems` | 需登录 |
| DELETE | `/admin/rating-community/collections/{}/items/{}` | write | `deleteCollectionsItems` | — |
| PUT | `/admin/rating-community/collections/{}/items/{}/sort` | write | `sortCollectionsItems` | — |
| PUT | `/admin/rating-community/collections/{}/status` | write | `updateCollectionsStatus` | — |
| GET | `/admin/rating-community/comments` | read | `getCommentsById` | 需登录 |
| DELETE | `/admin/rating-community/comments/batch` | write | `batchComments` | — |
| DELETE | `/admin/rating-community/comments/{}` | write | `deleteComments` | — |
| GET | `/admin/rating-community/contributions` | read | `getContributionsById` | 需登录 |
| GET | `/admin/rating-community/contributions/pending-count` | read | `getContributionsPendingCount` | 需登录 |
| POST | `/admin/rating-community/contributions/{}/review` | write | `reviewContributions` | — |
| GET | `/admin/rating-community/major-sections` | read | `getMajorSectionsById` | 需登录 |
| POST | `/admin/rating-community/major-sections` | write | `createMajorSections` | 需登录 |
| DELETE | `/admin/rating-community/major-sections/{}` | write | `deleteMajorSections` | 需登录 |
| GET | `/admin/rating-community/major-sections/{}` | read | `getMajorSectionsById2` | 需登录 |
| PUT | `/admin/rating-community/major-sections/{}` | write | `updateMajorSections` | 需登录 |
| DELETE | `/admin/rating-community/major-sections/{}/image` | write | `deleteMajorSectionsImage` | — |
| PUT | `/admin/rating-community/major-sections/{}/status` | write | `updateMajorSectionsStatus` | — |
| GET | `/admin/rating-community/minor-sections` | read | `getMinorSectionsById` | 需登录 |
| POST | `/admin/rating-community/minor-sections` | write | `createMinorSections` | 需登录 |
| DELETE | `/admin/rating-community/minor-sections/{}` | write | `deleteMinorSections` | — |
| PUT | `/admin/rating-community/minor-sections/{}` | write | `updateMinorSections` | — |
| DELETE | `/admin/rating-community/minor-sections/{}/image` | write | `deleteMinorSectionsImage` | — |
| PUT | `/admin/rating-community/minor-sections/{}/status` | write | `updateMinorSectionsStatus` | — |
| GET | `/admin/rating-community/rating-items` | read | `getRatingItemsById` | 需登录 |
| POST | `/admin/rating-community/rating-items` | write | `createRatingItems` | 需登录 |
| DELETE | `/admin/rating-community/rating-items/{}` | write | `deleteRatingItems` | 需登录 |
| GET | `/admin/rating-community/rating-items/{}` | read | `getRatingItemsById2` | 需登录 |
| PUT | `/admin/rating-community/rating-items/{}` | write | `updateRatingItems` | 需登录 |
| DELETE | `/admin/rating-community/rating-items/{}/image` | write | `deleteRatingItemsImage` | — |
| PUT | `/admin/rating-community/rating-items/{}/status` | write | `updateRatingItemsStatus` | — |
| GET | `/admin/rating-community/ratings` | read | `getRatingsById` | 需登录 |
| DELETE | `/admin/rating-community/ratings/batch` | write | `batchRatings` | — |
| DELETE | `/admin/rating-community/ratings/{}` | write | `deleteRatings` | — |
| GET | `/admin/rating-community/schools` | read | `getSchoolsById2` | 需登录 |
| POST | `/admin/rating-community/schools` | write | `createSchools` | 需登录 |
| DELETE | `/admin/rating-community/schools/{}` | write | `deleteSchools` | 需登录 |
| GET | `/admin/rating-community/schools/{}` | read | `getSchoolsById` | 需登录 |
| PUT | `/admin/rating-community/schools/{}` | write | `updateSchools` | 需登录 |
| PUT | `/admin/rating-community/schools/{}/status` | write | `updateSchoolsStatus` | — |
| GET | `/admin/rating-community/statistics/daily-ratings` | read | `getStatisticsDailyRatings` | 需登录 |
| GET | `/admin/rating-community/statistics/overview` | read | `getStatisticsOverview` | 需登录 |
| GET | `/rating-community/categories/{}` | read | `getRatingCommunityCategoriesById` | 存在·需参数 |
| GET | `/rating-community/collections` | read | `getRatingCommunityCollections` | 公开 |
| GET | `/rating-community/collections/{}` | read | `getRatingCommunityCollectionsById` | 存在·需参数 |
| POST | `/rating-community/comments` | write | `createRatingCommunityComments` | — |
| DELETE | `/rating-community/comments/{}` | write | `deleteRatingCommunityComments` | — |
| POST | `/rating-community/contributions` | write | `createRatingCommunityContributions` | — |
| POST | `/rating-community/contributions/batch-rating-items` | write | `batchRatingItemsRatingCommunityContributions` | — |
| GET | `/rating-community/contributions/history` | read | `getContributionHistory` | 存在·需参数 |
| GET | `/rating-community/contributions/my` | read | `getRatingCommunityContributionsMy` | 需登录 |
| POST | `/rating-community/contributions/upload-image` | write | `uploadContributionImage` | — |
| GET | `/rating-community/hot-items` | read | `getHotRatingItems` | 公开 |
| POST | `/rating-community/likes` | write | `createRatingCommunityLikes` | — |
| GET | `/rating-community/major-sections/{}/minor-sections` | read | `getRatingCommunityMajorSectionsMinorSectionsById` | 存在·需参数 |
| GET | `/rating-community/minor-sections/{}/rating-items` | read | `getRatingCommunityMinorSectionsRatingItemsById` | 存在·需参数 |
| GET | `/rating-community/random-items` | read | `getRandomRatingItems` | 公开 |
| GET | `/rating-community/rating-items/{}` | read | `getRatingCommunityRatingItemsById` | 存在·需参数 |
| POST | `/rating-community/ratings` | write | `createRatingCommunityRatings` | — |
| GET | `/rating-community/schools/{}/categories` | read | `getRatingCommunitySchoolsCategoriesById` | 存在·需参数 |
| GET | `/rating-community/search` | read | `searchRatingItems` | 存在·需参数 |


## HubVoices —— 声音问答（提问/回答/举报/后台治理）

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


## HubCampus —— 校区 / 楼宇 / 时段 / 用户检索

| 方法 | 路径 | 类别 | 包装方法 | 探测 |
|---|---|---|---|---|
| POST | `/admin/buildings` | write | `createAdminBuildings` | — |
| DELETE | `/admin/buildings/time-periods` | write | `deleteAdminBuildingsTimePeriods` | — |
| POST | `/admin/buildings/time-periods` | write | `createAdminBuildingsTimePeriods` | — |
| DELETE | `/admin/buildings/{}` | write | `deleteAdminBuildings` | — |
| PUT | `/admin/buildings/{}` | write | `updateAdminBuildings` | — |
| POST | `/admin/campuses` | write | `createAdminCampuses` | — |
| DELETE | `/admin/campuses/{}` | write | `deleteAdminCampuses` | — |
| PUT | `/admin/campuses/{}` | write | `updateAdminCampuses` | — |
| POST | `/admin/time-periods` | write | `createAdminResourceTimePeriods` | — |
| DELETE | `/admin/time-periods/{}` | write | `deleteAdminResourceTimePeriods` | — |
| PUT | `/admin/time-periods/{}` | write | `updateAdminResourceTimePeriods` | — |
| GET | `/admin/users/search/by-campus-account` | read | `searchUsersByCampusAccount` | 需登录 |
| GET | `/admin/users/search/by-campus-name` | read | `searchUsersByCampusName` | 需登录 |
| GET | `/admin/users/search/by-user` | read | `searchUsersByUser` | 需登录 |
| GET | `/buildings` | read | `getBuildings` | 需登录 |
| GET | `/buildings/{}/time-periods` | read | `getBuildingsTimePeriods` | 需登录 |
| GET | `/campuses` | read | `getCampuses` | 需登录 |
| GET | `/campuses/{}/buildings` | read | `getCampusesBuildingsById` | 需登录 |
| GET | `/time-periods` | read | `getResourceTimePeriods` | 需登录 |


## HubDebate —— 辩论场管理

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

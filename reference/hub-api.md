# 学社 API 端点清单（xmyzstudent.com）

> 来源：镜像 bundle 接口层（mc-lhz/XMYZStudent assets/）+ 实测探测。
> 事实来源 `tools/StudentHub/HubEndpoints.py`；本文件由
> `tools/Build/gen_hub_api_md.py` 派生，**不要手改端点行**。

- REST 端点 **260** 个（read 103 / write 157）+ WS **2** 条
- 基址 `https://api.xmyzstudent.com/api/v2`，Bearer token 鉴权
- 信封 `{code, message, data}`，业务失败也是 HTTP 200，code!=200
- 分页 `page` + `size`（部分端点 `pageSize`）

## WebSocket

| 路径 | 说明 |
|---|---|
| `wss://api.xmyzstudent.com/ws/tally/activity/{id}` | 唱票大屏快照（全量推送，单向） |
| `wss://api.xmyzstudent.com/ws/debate/round/{id}` | 辩论场实时消息 |

## HubAccount —— 账号与会话（auth/user/sms/permissions）

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| POST | `/auth/login` | write | `login` |
| POST | `/auth/qq-bind` | write | `qqBind` |
| POST | `/auth/qq-login` | write | `qqLogin` |
| POST | `/auth/qq-register` | write | `qqRegister` |
| GET | `/auth/qq/authorize-url` | read | `getQQAuthorizeUrl` |
| POST | `/auth/register` | write | `register` |
| GET | `/permissions/my` | read | `getMyPermissions` |
| POST | `/sms/bind` | write | `bindSms` |
| GET | `/sms/binding` | read | `getSmsBinding` |
| POST | `/sms/login` | write | `smsLogin` |
| POST | `/sms/send` | write | `sendSmsCode` |
| DELETE | `/sms/unbind` | write | `unbindSms` |
| POST | `/user/avatar` | write | `uploadMyAvatar` |
| POST | `/user/bind-campus` | write | `bindCampus` |
| POST | `/user/bind-qq` | write | `bindQQ` |
| GET | `/user/campus-binding` | read | `getCampusBinding` |
| GET | `/user/has-password` | read | `getHasPassword` |
| PUT | `/user/password` | write | `updatePassword` |
| GET | `/user/privacy-settings` | read | `getPrivacySettings` |
| PUT | `/user/privacy-settings` | write | `updatePrivacySettings` |
| GET | `/user/profile` | read | `getMyProfile` |
| PUT | `/user/profile` | write | `updateMyProfile` |
| GET | `/user/qq-binding` | read | `getQQBinding` |
| GET | `/user/qq/authorize-url` | read | `getUserQQAuthorizeUrl` |
| POST | `/user/rebind-campus` | write | `rebindCampus` |
| DELETE | `/user/unbind-campus` | write | `unbindCampus` |
| DELETE | `/user/unbind-qq` | write | `unbindQQ` |
| GET | `/user/users/{}/avatar` | read | `getUserAvatar` |
| GET | `/user/users/{}/profile` | read | `getUserProfile` |


## HubPortal —— 门户（横幅/年级绑定/文件/音乐/QQ音乐）

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/banners` | read | `getAdminBanners` |
| POST | `/admin/banners` | write | `createAdminBanner` |
| DELETE | `/admin/banners/{}` | write | `deleteAdminBanner` |
| PUT | `/admin/banners/{}` | write | `updateAdminBanner` |
| POST | `/admin/banners/{}/toggle-status` | write | `toggleAdminBannerStatus` |
| GET | `/banners` | read | `getPublicBanners` |
| GET | `/campus/captcha` | read | `getCampusCaptcha` |
| POST | `/files/upload` | write | `uploadFile` |
| POST | `/grade/bind` | write | `bindGrade` |
| GET | `/grade/exams` | read | `getGradeExams` |
| GET | `/grade/exams/{}` | read | `getGradeExamsById` |
| GET | `/grade/status` | read | `getGradeStatus` |
| DELETE | `/grade/unbind` | write | `unbindGrade` |
| GET | `/qqmusic/auth/qrcode` | read | `getQQMusicQrCode` |
| GET | `/qqmusic/auth/qrcode/status` | read | `getQQMusicQrStatus` |
| GET | `/qqmusic/auth/status` | read | `getQQMusicAuthStatus` |
| GET | `/qqmusic/qualities` | read | `getQQMusicQualities` |


## HubMessage —— 站内消息（收件箱 + 管理端群发/模板）

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/messages` | read | `getAdminMessages` |
| DELETE | `/admin/messages/batch` | write | `deleteAdminMessagesBatch` |
| POST | `/admin/messages/broadcast` | write | `broadcastAdminMessage` |
| POST | `/admin/messages/send` | write | `sendAdminMessage` |
| GET | `/admin/messages/stats` | read | `getAdminMessageStats` |
| GET | `/admin/messages/templates` | read | `getAdminMessageTemplates` |
| POST | `/admin/messages/templates` | write | `createAdminMessageTemplate` |
| DELETE | `/admin/messages/templates/{}` | write | `deleteAdminMessageTemplate` |
| PUT | `/admin/messages/templates/{}` | write | `updateAdminMessageTemplate` |
| DELETE | `/admin/messages/{}` | write | `deleteAdminMessage` |
| GET | `/messages` | read | `getMessages` |
| PUT | `/messages/read-all` | write | `markAllMessagesRead` |
| GET | `/messages/unread-count` | read | `getUnreadMessageCount` |
| DELETE | `/messages/{}` | write | `deleteMessage` |
| PUT | `/messages/{}/read` | write | `markMessageRead` |


## HubTally —— 实时唱票

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


## HubCampaign —— 投票征集活动

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| POST | `/admin/campaigns` | write | `createAdminCampaigns` |
| PUT | `/admin/campaigns/{}` | write | `updateAdminCampaigns` |
| POST | `/admin/campaigns/{}/activate` | write | `activateAdminCampaigns` |
| POST | `/admin/campaigns/{}/close` | write | `closeAdminCampaigns` |
| POST | `/admin/campaigns/{}/stage-operation` | write | `stageOperationAdminCampaigns` |
| GET | `/admin/review/campaigns/{}/submissions` | read | `getAdminReviewCampaignsSubmissions` |
| DELETE | `/admin/review/submissions` | write | `deleteAdminReviewSubmissions` |
| GET | `/admin/voting/campaigns/{}/results` | read | `getAdminVotingCampaignsResults` |
| GET | `/campaigns` | read | `getCampaigns` |
| GET | `/campaigns/{}` | read | `getCampaignsById` |
| GET | `/music/detail` | read | `getMusicDetail` |
| GET | `/music/search` | read | `searchMusic` |
| GET | `/music/url` | read | `getMusicUrl` |
| POST | `/submissions` | write | `createResourceSubmissions` |
| GET | `/submissions/campaigns/{}` | read | `getSubmissionsCampaignsById` |
| GET | `/voting/campaigns/{}/config` | read | `getVotingCampaignsConfig` |
| GET | `/voting/campaigns/{}/my-votes` | read | `getVotingCampaignsMyVotes` |
| GET | `/voting/campaigns/{}/options` | read | `getVotingOptions` |
| POST | `/voting/vote` | write | `voteVoting` |


## HubTicket —— 电子票务（活动/抢票/核销/审核）

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


## HubMuseum —— 校园博物馆（事件/区块/标签/瞬间审核）

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


## HubRating —— 评分社区（浏览/投稿/评分/评论/后台）

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/rating-community/categories` | read | `getCategoriesById2` |
| POST | `/admin/rating-community/categories` | write | `createCategories` |
| DELETE | `/admin/rating-community/categories/{}` | write | `deleteCategories` |
| GET | `/admin/rating-community/categories/{}` | read | `getCategoriesById` |
| PUT | `/admin/rating-community/categories/{}` | write | `updateCategories` |
| DELETE | `/admin/rating-community/categories/{}/image` | write | `deleteCategoriesImage` |
| PUT | `/admin/rating-community/categories/{}/status` | write | `updateCategoriesStatus` |
| GET | `/admin/rating-community/collections` | read | `getCollectionsById` |
| POST | `/admin/rating-community/collections` | write | `createCollections` |
| DELETE | `/admin/rating-community/collections/{}` | write | `deleteCollections` |
| GET | `/admin/rating-community/collections/{}` | read | `getCollectionsById2` |
| PUT | `/admin/rating-community/collections/{}` | write | `updateCollections` |
| DELETE | `/admin/rating-community/collections/{}/image` | write | `deleteCollectionsImage` |
| GET | `/admin/rating-community/collections/{}/items` | read | `getCollectionsItemsById` |
| POST | `/admin/rating-community/collections/{}/items` | write | `createCollectionsItems` |
| DELETE | `/admin/rating-community/collections/{}/items/{}` | write | `deleteCollectionsItems` |
| PUT | `/admin/rating-community/collections/{}/items/{}/sort` | write | `sortCollectionsItems` |
| PUT | `/admin/rating-community/collections/{}/status` | write | `updateCollectionsStatus` |
| GET | `/admin/rating-community/comments` | read | `getCommentsById` |
| DELETE | `/admin/rating-community/comments/batch` | write | `batchComments` |
| DELETE | `/admin/rating-community/comments/{}` | write | `deleteComments` |
| GET | `/admin/rating-community/contributions` | read | `getContributionsById` |
| GET | `/admin/rating-community/contributions/pending-count` | read | `getContributionsPendingCount` |
| POST | `/admin/rating-community/contributions/{}/review` | write | `reviewContributions` |
| GET | `/admin/rating-community/major-sections` | read | `getMajorSectionsById` |
| POST | `/admin/rating-community/major-sections` | write | `createMajorSections` |
| DELETE | `/admin/rating-community/major-sections/{}` | write | `deleteMajorSections` |
| GET | `/admin/rating-community/major-sections/{}` | read | `getMajorSectionsById2` |
| PUT | `/admin/rating-community/major-sections/{}` | write | `updateMajorSections` |
| DELETE | `/admin/rating-community/major-sections/{}/image` | write | `deleteMajorSectionsImage` |
| PUT | `/admin/rating-community/major-sections/{}/status` | write | `updateMajorSectionsStatus` |
| GET | `/admin/rating-community/minor-sections` | read | `getMinorSectionsById` |
| POST | `/admin/rating-community/minor-sections` | write | `createMinorSections` |
| DELETE | `/admin/rating-community/minor-sections/{}` | write | `deleteMinorSections` |
| PUT | `/admin/rating-community/minor-sections/{}` | write | `updateMinorSections` |
| DELETE | `/admin/rating-community/minor-sections/{}/image` | write | `deleteMinorSectionsImage` |
| PUT | `/admin/rating-community/minor-sections/{}/status` | write | `updateMinorSectionsStatus` |
| GET | `/admin/rating-community/rating-items` | read | `getRatingItemsById` |
| POST | `/admin/rating-community/rating-items` | write | `createRatingItems` |
| DELETE | `/admin/rating-community/rating-items/{}` | write | `deleteRatingItems` |
| GET | `/admin/rating-community/rating-items/{}` | read | `getRatingItemsById2` |
| PUT | `/admin/rating-community/rating-items/{}` | write | `updateRatingItems` |
| DELETE | `/admin/rating-community/rating-items/{}/image` | write | `deleteRatingItemsImage` |
| PUT | `/admin/rating-community/rating-items/{}/status` | write | `updateRatingItemsStatus` |
| GET | `/admin/rating-community/ratings` | read | `getRatingsById` |
| DELETE | `/admin/rating-community/ratings/batch` | write | `batchRatings` |
| DELETE | `/admin/rating-community/ratings/{}` | write | `deleteRatings` |
| GET | `/admin/rating-community/schools` | read | `getSchoolsById2` |
| POST | `/admin/rating-community/schools` | write | `createSchools` |
| DELETE | `/admin/rating-community/schools/{}` | write | `deleteSchools` |
| GET | `/admin/rating-community/schools/{}` | read | `getSchoolsById` |
| PUT | `/admin/rating-community/schools/{}` | write | `updateSchools` |
| PUT | `/admin/rating-community/schools/{}/status` | write | `updateSchoolsStatus` |
| GET | `/admin/rating-community/statistics/daily-ratings` | read | `getStatisticsDailyRatings` |
| GET | `/admin/rating-community/statistics/overview` | read | `getStatisticsOverview` |
| GET | `/rating-community/categories/{}` | read | `getRatingCommunityCategoriesById` |
| GET | `/rating-community/collections` | read | `getRatingCommunityCollections` |
| GET | `/rating-community/collections/{}` | read | `getRatingCommunityCollectionsById` |
| POST | `/rating-community/comments` | write | `createRatingCommunityComments` |
| DELETE | `/rating-community/comments/{}` | write | `deleteRatingCommunityComments` |
| POST | `/rating-community/contributions` | write | `createRatingCommunityContributions` |
| POST | `/rating-community/contributions/batch-rating-items` | write | `batchRatingItemsRatingCommunityContributions` |
| GET | `/rating-community/contributions/history` | read | `getContributionHistory` |
| GET | `/rating-community/contributions/my` | read | `getRatingCommunityContributionsMy` |
| POST | `/rating-community/contributions/upload-image` | write | `uploadContributionImage` |
| GET | `/rating-community/hot-items` | read | `getHotRatingItems` |
| POST | `/rating-community/likes` | write | `createRatingCommunityLikes` |
| GET | `/rating-community/major-sections/{}/minor-sections` | read | `getRatingCommunityMajorSectionsMinorSectionsById` |
| GET | `/rating-community/minor-sections/{}/rating-items` | read | `getRatingCommunityMinorSectionsRatingItemsById` |
| GET | `/rating-community/random-items` | read | `getRandomRatingItems` |
| GET | `/rating-community/rating-items/{}` | read | `getRatingCommunityRatingItemsById` |
| POST | `/rating-community/ratings` | write | `createRatingCommunityRatings` |
| GET | `/rating-community/schools/{}/categories` | read | `getRatingCommunitySchoolsCategoriesById` |
| GET | `/rating-community/search` | read | `searchRatingItems` |


## HubVoices —— 声音问答（提问/回答/举报/后台治理）

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


## HubCampus —— 校区 / 楼宇 / 时段 / 用户检索

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


## HubDebate —— 辩论场管理

| 方法 | 路径 | 类别 | 包装方法 |
|---|---|---|---|
| GET | `/admin/debate/rounds` | read | `getAdminDebateRounds` |
| POST | `/admin/debate/rounds` | write | `createAdminDebateRounds` |
| DELETE | `/admin/debate/rounds/{}` | write | `deleteAdminDebateRounds` |
| PUT | `/admin/debate/rounds/{}` | write | `updateAdminDebateRounds` |
| PUT | `/admin/debate/rounds/{}/active` | write | `updateAdminDebateRoundsActive` |
| PUT | `/admin/debate/rounds/{}/lock` | write | `lockAdminDebateRounds` |
| PUT | `/admin/debate/rounds/{}/regenerate-password` | write | `regeneratePasswordAdminDebateRounds` |
| PUT | `/admin/debate/rounds/{}/reset` | write | `resetAdminDebateRounds` |
| PUT | `/admin/debate/rounds/{}/unlock` | write | `unlockAdminDebateRounds` |

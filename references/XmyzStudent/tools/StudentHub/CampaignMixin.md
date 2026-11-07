# CampaignMixin — 投票征集活动

包装 `HubCampaign` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

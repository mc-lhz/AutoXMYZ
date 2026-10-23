# CampaignMixin — 投票征集活动

包装 `HubCampaign` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

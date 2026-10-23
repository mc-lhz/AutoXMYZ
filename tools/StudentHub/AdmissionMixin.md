# AdmissionMixin — 纳新/准入（分组/成员/豁免/扫码 + 用户验证）

包装 `HubAdmission` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

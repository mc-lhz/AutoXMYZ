# AccountMixin — 账号与会话（auth/user/sms/permissions）

包装 `HubAccount` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

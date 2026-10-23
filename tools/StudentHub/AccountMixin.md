# AccountMixin — 账号与会话（auth/user/sms/permissions）

包装 `HubAccount` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

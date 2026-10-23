# PortalMixin — 门户（横幅/年级绑定/文件/音乐/QQ音乐）

包装 `HubPortal` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

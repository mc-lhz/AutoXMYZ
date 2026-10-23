# PortalMixin — 门户（横幅/年级绑定/文件/音乐/QQ音乐）

包装 `HubPortal` 域端点；方法签名按镜像接口层还原，命名保持站点语义导出名。

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

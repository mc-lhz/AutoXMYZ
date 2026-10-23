# HubSession — 学社登录与会话

四种登录方式，输出同一个 Bearer token，落盘仓库外 `hub_session.json`。

## 登录契约（实测）

| 方式 | 流程 |
|---|---|
| `campus` | `GET /campus/captcha` → `{captchaImage(dataURL), jsessionId, expiresAt}` → `POST /auth/login {loginType:"campus", campusAccount, campusPassword, captchaCode, jsessionId}` |
| `normal` | `POST /auth/login {loginType:"normal", username, password}` |
| `sms` | `POST /sms/send {phoneNumber, purpose}` → `POST /sms/login {phoneNumber, code}` |
| `token` | 浏览器 F12 → Application → localStorage → `token` 字段复制 |

campus 模式即**校园网账号直连学社**，与 xmyz 校内系统同源账号体系；
验证码与人机绑定靠 `jsessionId`（一次性、随验证码下发，非登录会话）。

## CLI

```bash
python tools/StudentHub/HubSession.py captcha                    # ① 取验证码图（临时目录），jsessionId 自动暂存
python tools/StudentHub/HubSession.py campus -a <账号> -p <密码> --code ab12   # ② 看图后提交
python tools/StudentHub/HubSession.py campus -a <账号> -p <密码> --ocr 6       # 无读图能力：OCR 投票重试
python tools/StudentHub/HubSession.py normal -u <用户名> -p <密码>
python tools/StudentHub/HubSession.py token --token <localStorage.token>
python tools/StudentHub/HubSession.py check                      # 自检：/user/profile 有 username 即有效
```

## 判据与坑

- 登录成功判据 = `/user/profile` 返回有 `username`（与 xmyz 的「看 loginName」同理，
  不能用任何「loggedIn 布尔」字段——学社 401 信封是 `{code:401}`，公开端点则永远 200）
- `jsessionId` 是**验证码绑定**不是会话；`expiresAt` 是 unix 秒，过期必须重取
- OCR 复用 `Access/LoginSession.ocrCaptcha`（591iq/AutoXMYZ 同源同参）；
  `rapidocr-onnxruntime` 未安装时 `--ocr` 会空转报错，优先 vision/token
- 凭据只进 argv 由调用方决定；本工具不读取、不落盘密码原文，会话文件只存 token

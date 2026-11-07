# Login — 统一登录编排（一组凭据 → 三站会话）

三站同组学号密码；本脚本只是**编排器**，全部以子进程调用各子树自己的登录 CLI
（`cwd=子树根`），零跨子树 import——避免 `tools` 顶层包名冲突。

| 子命令 | 行为 |
|---|---|
| `all -u -p [--ocr N] [--code-hub X]` | ① CampusNet 门户登录（验证码 OCR/vision）→ send `session.json`；② 用同 JSESSIONID 调 XinYiWo `LoginToken.py jsessionid` → `iq_token.json`；③ 学社 `HubSession.py campus`（学社自己的验证码）→ `hub_session.json` |
| `campusnet -u -p` | 仅校内系统 |
| `xinyiwo [-u -p]` | 优先复用 CampusNet 会话换 ssoToken；无会话时可自行登录门户 |
| `xmyzstudent -a -p [--code X \| --ocr N]` | 仅学社（服务端回调 CampusNet 校验，客户端无需 CampusNet 会话） |
| `status` | 三站自检汇总（CampusNet --health / XinYiWo token verify / 学社 check） |

## 认证拓扑

```
学号+密码
 ├─ CampusNet：门户直登 → JSESSIONID
 ├─ XinYiWo ：同门户 JSESSIONID → ssoToken（无需二次验证码）
 └─ XmyzStudent：学社服务端拿同凭据回调 CampusNet（共享凭据，不共享会话）
```

## 会话位置（仓库外）

`%LOCALAPPDATA%\AutoXMYZ\`：`session.json` / `iq_token.json` / `hub_session.json`
（`AUTOMXYZ_SESSION`、`AUTOMXYZ_HUB_SESSION` 可覆盖前两者）。

## 提示

- 有读图能力时，逐站用各自 `--code/vision` 流程更稳；`all` 的 OCR 是兜底。
- 学社登录会把密码经学社服务器转发 CampusNet（站点设计）——不可信网络下勿用。

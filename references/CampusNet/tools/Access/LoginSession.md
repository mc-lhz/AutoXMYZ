登录（三种方式，输出同一个 JSESSIONID）：

- `password` —— 账号密码 + 验证码 OCR 自动重试
- `jsessionid` —— 浏览器已登录时复制会话，免验证码
- `vision` —— 取验证码图 / 凭 `--code` 提交
- `check` —— 无凭据探测端点可达性

**有读图能力时优先 `vision`**（实测 100%）；无读图能力用 `password` 的 OCR（变体池投票）。

会话落在**仓库外**的用户目录，默认 `%LOCALAPPDATA%\AutoXMYZ\session.json`
（类 Unix 为 `~/.local/share/AutoXMYZ/`），可用 `--out <PATH>` 覆盖。

> 刻意不写进仓库：靠 `.gitignore` 挡是「记得配才行」，靠路径隔离才是「不配也不会漏」。
> 仓库里那份 `reference/.session.json` 只是占位模板，仅供未登录时给出可读提示。

验证码实测：**4~5 位、只含小写字母、一次性、服务端大小写敏感**。
`--interactive` 会阻塞，**agent 不得使用**。

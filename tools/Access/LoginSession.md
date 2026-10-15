登录（三种方式，输出同一个 JSESSIONID）：

- `password` —— 账号密码 + 验证码 OCR 自动重试
- `jsessionid` —— 浏览器已登录时复制会话，免验证码
- `vision` —— 取验证码图 / 凭 `--code` 提交
- `check` —— 无凭据探测端点可达性

**有读图能力时优先 `vision`**（实测 100%）；无读图能力用 `password` 的 OCR（变体池投票）。

会话落在 `reference/.session.json`（含真实凭据，**不入库**）。

验证码实测：**4~5 位、只含小写字母、一次性、服务端大小写敏感**。
`--interactive` 会阻塞，**agent 不得使用**。

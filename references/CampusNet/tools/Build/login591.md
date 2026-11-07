建库阶段一：登录。直接复用 591iqAutomatic 的 `Access/LoginToken.py`
（`ocrCaptcha` / `newSession` / `portalLogin`），因为 xmyz.xmedu.cn 与
591iq.cn **是同一个门户**，验证码特征一致（4~5 位、纯小写、一次性）。

产出会话与菜单树，是后续所有步骤的前置。

依赖：`IQ_SKILL` 环境变量指向 591iqAutomatic 目录（默认 `~/.config/opencode/skills/591iqAutomatic`）。

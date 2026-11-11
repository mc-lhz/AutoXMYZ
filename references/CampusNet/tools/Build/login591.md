建库阶段一：登录。直接复用 XinYiWo 子技能（原 591iqAutomatic，上游已归档）的
`Access/LoginToken.py`（`ocrCaptcha` / `newSession` / `portalLogin`），因为
xmyz.xmedu.cn 与 591iq.cn **是同一个门户**，验证码特征一致（4~5 位、纯小写、一次性）。

产出会话与菜单树，是后续所有步骤的前置。

依赖：`IQ_SKILL` 环境变量指向 XinYiWo 子树目录（默认本仓 `references/XinYiWo`，可用 `IQ_SKILL` 覆盖）。

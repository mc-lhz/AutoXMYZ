建库阶段三：三方端点合并。

读取 desktop（菜单树 + 97 模块）、m2.html 主 bundle、m.html 主 bundle，
去重合并成一份 `endpoints.json`，每条带 `sources`（来自哪个前端）、
`kind`（读/写，由 `endpoint_kind` 判定）、`menus`（所属菜单）、`files`。

⚠️ 抽取正则必须含连字符：`[A-Za-z0-9_\-/]+!`。早期漏了 `-`，
`growth-record` 被截成 `record`，端点数从 491 少算成 159。

产出 683 个唯一端点（只读 359 / 写类 324）。

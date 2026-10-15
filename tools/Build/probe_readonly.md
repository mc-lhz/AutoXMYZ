建库阶段四：只读端点全量探测。

对 359 个只读端点各发一次 GET + POST，`start=0&limit=1`，
`id` 一律用不存在的 `-1`（保证即使端点语义含删除也只会命中「无此记录」），
限速 180ms。实测 813 秒。

判定口径见 `tools/TestCases/TestApiReadOnly.md`：解析出 JSON 即 ALIVE，
空数组也算（端点通、无数据 ≠ 不可用）。

⚠️ 本脚本**只跑 kind == 'read' 的端点**，写端点一律跳过 ——
判定复用 `endpoint_kind`，与运行时守卫同源。

产出：`<work>/validation.json`

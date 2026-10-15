只读端点全量探测 35 项，可重复运行。
`--limit N` 快速冒烟，`--report` 输出报告 JSON。

⚠️ 判定口径：本系统有两类响应——

- **信封型**：`{"total":n,"data":[...],"success":true}`
- **裸数组 / 裸对象**：`dict!getTree` / `grade!loadTree` /
  `recipient!statInfo` / `community!loadTree`

只认信封会把 5 个真实可用端点误报 FAIL。**只要解析出 JSON 即 ALIVE，空数组也算**
（端点通、无数据 ≠ 不可用）。

退出码：0 全通过 / 1 有失败 / 4 会话不可用。

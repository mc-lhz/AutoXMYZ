# TestAggregate — 聚合契约审计（离线）

三子技能分区结构的守门人：

| 检查 | 内容 |
|---|---|
| 结构·三子技能 | 根 SKILL/AGENTS/README/VERSION/Login.py + 三个 `references/<Sub>/{SUBSKILL,AGENTS,tools,reference}` |
| 结构·无游离 SKILL | `references/**` 下只允许 `SUBSKILL.md`（否则宿主重复注册） |
| 路由·根 description | 含三站点名/域名、「数据不互通」、「不加载其他子技能」、关键触发词 |
| 契约·三子树 | 子进程从各自根运行：CampusNet 9/9、XmyzStudent 15/15、XinYiWo FAIL=0 |
| 体积·reference | 三子树各自 ≤150KB（分区预算） |
| 版本·CLI | VERSION 形如 v2.0；`tools/Login.py -h` 通过 |

```bash
python -B tools/TestCases/TestAggregate.py
```

---
name: AutoXMYZ
description: 厦门一中三站聚合工具集（同一组学号密码）：CampusNet=校内系统 xmyz.xmedu.cn（成绩/成绩单、成长记录、综评写实记录、社团志愿、短信、待办、会考练习/信息技术会考、选科、选课、心理预约、打卡、投票、教师评测）；XmyzStudent=学社 xmyzstudent.com（唱票、票务、评分社区、声音问答、校园博物馆、辩论场、纳新、站内消息）；XinYiWo=新壹我/591iq www.591iq.cn（综评写实记录与活动总结、成长报告、待办任务、荣誉、xlsx 导出）。Use when the user mentions xmyz、厦一中、一中校园、校内系统、591iq、新壹我、天蛙、学社、xmyzstudent、学生社区、成绩查询、成绩单、成长记录、成长报告、综合素质评价、综评系统、写实记录、待办、志愿者、社团、会考练习、信息技术会考、选科、选课、心理预约、打卡、投票、唱票、抢票、票务、评分社区、声音问答、校园博物馆、辩论场、ssoToken，或要查询/导出/提交本人的上述数据。三站数据不互通；CampusNet/XmyzStudent/XinYiWo 三个子技能按诉求分流，只读取并执行命中的那一个，不加载其他子技能。
---

# AutoXMYZ — 厦门一中三站聚合工具集

本技能由 3 个子技能构成，**三站共用同一组学号密码**，但数据互不互通。
收到诉求后先按下表定位唯一匹配的子技能，再
`Read references/<子技能>/SUBSKILL.md` 进入，按其内部说明继续执行。不要一次性通读全部子技能。

## 子技能索引

| 子技能 | 站点 | 职责 |
|---|---|---|
| [`CampusNet`](references/CampusNet/SUBSKILL.md) | `xmyz.xmedu.cn` | 校内系统（3 前端共用 JSESSIONID）：成绩/成绩单、成长记录、综评写实记录、社团志愿、短信、待办、会考练习、选科、选课、日程、心理预约、打卡、投票、评测、考勤 |
| [`XmyzStudent`](references/XmyzStudent/SUBSKILL.md) | `xmyzstudent.com` | 学社（学生自建平台，功能完备含写）：实时唱票(+WS)、票务、评分社区、声音问答、校园博物馆、辩论场、纳新、站内消息 |
| [`XinYiWo`](references/XinYiWo/SUBSKILL.md) | `www.591iq.cn` | 新壹我（天蛙）综评系统：写实记录读写/发布/删除、活动总结、评论互动、成长报告与自我总结、待办、荣誉、xlsx 导出 |

<system-reminder>
本技能由「子技能分区」构成：每个子技能位于 `references/<子技能名>/`，各自保留完整的
`SUBSKILL.md` 与 `tools/`、`reference/`（XinYiWo 另有 AGENTS（含变更历史与开发记忆）/VERSION）目录树。
子技能内部的相对路径一律以它自己所在的 `references/<子技能名>/` 为基准解析——读到
`tools/x.py`、`reference/y.md` 时，实际指向 `references/<子技能名>/tools/x.py`，不要退回到
本技能根目录查找，也不要再加一层 `references/` 前缀。

执行某一子技能的命令时，须使用完整路径 `references/<子技能名>/tools/...`；
子技能文档里写的 `python tools/...` 是相对它自身目录的，不能照搬到本技能根下运行。
先按下表定位「子技能」，只 `Read` 那一个 `SUBSKILL.md`，不要一次性通读全部子技能。

三站同一组凭据（学号+密码）。统一登录编排在根目录 `tools/Login.py`：
`python tools/Login.py all -u <学号> -p <密码>` 一次登录三站；`status` 查看会话状态。
认证拓扑：CampusNet 门户签发 JSESSIONID；XinYiWo 用同一 JSESSIONID 换发 ssoToken；
XmyzStudent 由学社服务端拿同一凭据回调 CampusNet 校验（客户端无需 CampusNet 会话）。
</system-reminder>
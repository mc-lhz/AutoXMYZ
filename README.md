# AutoXMYZ — 厦门一中三站聚合工具集

三站**同一组学号密码**，数据互不互通：

| 子技能 | 站点 | 能力 |
|---|---|---|
| [CampusNet](references/CampusNet/SUBSKILL.md) | `xmyz.xmedu.cn` | 校内系统：成绩/成绩单、成长记录、综评、社团志愿、短信、待办、会考练习、选科、选课、日程、心理预约、打卡、投票、评测 |
| [XmyzStudent](references/XmyzStudent/SUBSKILL.md) | `xmyzstudent.com` | 学社：唱票(+WS)、票务、评分社区、声音问答、校园博物馆、辩论场、纳新、站内消息 |
| [XinYiWo](references/XinYiWo/SUBSKILL.md) | `www.591iq.cn` | 新壹我：综评写实记录读写/发布/删除、活动总结、成长报告、待办、荣誉、xlsx 导出 |

## 快速开始

```bash
# 统一登录（一组凭据登录三站；验证码按提示看图或 OCR）
python tools/Login.py all -u <学号> -p <密码>
python tools/Login.py status            # 三站会话状态

# 进入某站（示例：CampusNet 成绩）
python references/CampusNet/tools/XMYZClient.py --health
python -c "import sys; sys.path.insert(0,'references/CampusNet/tools'); from XMYZClient import XMYZClient; c=XMYZClient(); print(c.transcript()['total'])"
```

各站详细用法见对应 `SUBSKILL.md`；开发契约见 `AGENTS.md`。

## 结构

- `references/<子技能>/` — 各自完整子树（`SUBSKILL.md` + `tools/` + `reference/`）
- `tools/Login.py` — 统一登录编排（子进程，零跨子树 import）
- `tools/TestCases/TestAggregate.py` — 聚合契约
- 会话/token 全部在仓库外：`%LOCALAPPDATA%\AutoXMYZ\`（类 Unix `~/.local/share/AutoXMYZ/`）

## 安全

- 三站同一组凭据；**学社登录会把密码经其服务器转发 CampusNet**（站点设计），
  不可信网络下勿用学社登录态。
- 未成年人个人信息：账号信息、凭据、导出文件不入库、不外传；入库文档禁真实姓名。
- XinYiWo 红线：不人员枚举、写操作 `--yes` + 回执校验、默认脱敏。

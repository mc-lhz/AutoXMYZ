---
name: CampusNet
description: 厦门一中校内系统（xmyz.xmedu.cn，Struts2，三前端）工具集。Use when the user mentions xmyz、厦一中、一中校园、校内系统、成绩单、成绩查询、成长记录、志愿者、社团、电子成绩单、待办审批、校园短信、菜单树、会考练习、信息技术会考、选科、选课、厦一大讲堂、心理预约、打卡、投票、教师评测、综合素质评价（校内系统口径），或要查询本人成绩/成长记录/考勤/选科结果，或提交综评写实记录。
---

# CampusNet — 厦门一中校内系统（xmyz.xmedu.cn）

> **路径基准**：本文件位于 `references/CampusNet/`，下文 `tools/...`、`reference/...`
> 均相对本目录。从技能根执行时写完整前缀 `references/CampusNet/tools/...`。

> **能力政策（2026-10-24 由仓库所有者修订）**：早年「纯只读」已解除，
> 读写均放行；`endpoint_kind.py` 的读写分类只作文档/统计口径。
> **写纪律**：只写本人数据、可逆优先（create→verify→destroy 闭环）、
> 不封装 `resetPassword`、不碰他人审批流；服务端账号权限是最终边界。
> 共同纪律：含未成年人个人信息——账号信息、凭据、导出文件不入库、不外传；
> 会话文件一律写仓库外用户目录。

三个前端入口共用同一 `JSESSIONID`（`Path=/`，同源）：

| 入口 | 技术栈 | 角色 |
|---|---|---|
| `manager.html` | ExtJS 3.4，服务端驱动按需加载 | 桌面管理端（门户登录指向） |
| `m2.html` | Vue 3 + Vant，hash 路由 | 移动端新版（待办审批等） |
| `m.html` | Vue 2 + Vux | 移动端旧版（已被 m2 取代） |

端点注册表 **2625**（读 1194 / 写 1431，2026-10-24 真实会话对账；
m2 已改版重建，含拼接族/无 `!` 直连路由收口）。完整清单见 `reference/api.md`。

## 登录（与 XinYiWo 同门户；凭据与 XmyzStudent 同源）

```bash
python tools/Access/LoginSession.py vision                                   # ① 取验证码图（有读图能力）
python tools/Access/LoginSession.py vision -u <学号> -p <密码> --code ab12   #    看图后提交
python tools/Access/LoginSession.py password -u <学号> -p <密码> --retry 6   # ② OCR 兜底
python tools/Access/LoginSession.py jsessionid --jsessionid <JSESSIONID>     # ③ 浏览器会话直填
python tools/Access/LoginSession.py check                                    # ④ 无凭据可达性
```

会话在仓库外：`%LOCALAPPDATA%\AutoXMYZ\session.json`（`--out` 可改）。
`reference/.session.json` 只是占位模板。

## 使用

```python
import sys; sys.path.insert(0, "tools")     # 从 references/CampusNet 起
from XMYZClient import XMYZClient
c = XMYZClient()                            # 自动读用户目录会话
c.healthCheck()
c.status(); c.menuTree(); c.quality(); c.myScores(); c.transcript()
c.growthRecords(); c.myCommunities(); c.myVolunteerActivities(); c.inbox()
c.mySelectSubject()                          # 选科汇总
c.getMyAnswerStats(examId=...)               # 会考练习统计
```

具名方法 331 个（18 个业务域），另有泛化 `get/post/destroy/paged` 可达全部端点。
会话自检：`python tools/XMYZClient.py --health` / `--summary`。

## 命令速查

```bash
python tools/TestCases/TestContract.py      # 仓库契约（离线 9 项）
python tools/TestCases/TestApiReadOnly.py   # 只读 35 项
python tools/TestCases/TestMethodSmoke.py   # 具名方法线上冒烟（116 法，GET+read 安全集）
python tools/Build/precommit_check.py       # 入库前四道闸
```

## 端点与分页契约

- 桌面端分页 `start` + `limit`（不是 m2 的 page/pageSize）
- 两种响应：信封 `{total,data,success}` 与裸数组/裸对象；`success:false` 不代表端点不可用
- `destroy` 统一契约：POST `data=<单对象JSON含id>`（`Http.destroy()` 已封）
- 学生端综评写入真身是 `edu/growth-record-detail!saveByStudent`（`growth-record!createByStudent` 是 grid 代理路径）
- 会考练习：`exam/answer!statByStudent?examId=` 忽略题库参数，一次返回整场统计
- 选科：`select-subject!getComboStoreByStudentOrParent` → `select-subject-result-detail!loadId`；
  签名图走 `system/attachment!send.action?id=<签名id>`
- `transcript!detail.action` 与 `member!readByStudent` 等为线上 404（GONE，文档已标注）

## 端点清单怎么来的（`tools/Build/`）

```bash
python tools/Build/login591.py          # 复用 XinYiWo 登录（IQ_SKILL 指向 references/XinYiWo）
python tools/Build/fetch_modules.py     # 菜单树 → 97 模块
python tools/Build/merge_endpoints.py   # 三方合并（含 DIRECT_ROUTES/FRAMEWORK_ENDPOINTS）
python tools/Build/probe_readonly.py    # 只读全量探测（增量续跑）
python tools/Build/gen_api_md.py        # 重生成 reference/api.md
python tools/Build/precommit_check.py   # 四道闸
```

中间产物用 `AUTOMXYZ_WORK` 指到仓库外（含真实姓名/学号，不入库）。

## 注意事项

- 写操作按上文纪律；`account/user!resetPassword.action` 不封装
- 会话过期就重新登录；单账号串行、限速 ≥180ms；遇 4xx/429 停手
- 探测未知端点用不存在的 `id=-1`，不要遍历真实 id
- 入库文档禁止真实姓名/token；`reference/` 体积上限 150KB（当前 ≈105KB）
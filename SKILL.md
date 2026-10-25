---
name: AutoXMYZ
description: 厦门一中校内系统（xmyz.xmedu.cn，只读）与学生社区（xmyzstudent.com，功能完备）聚合工具集。Use when the user mentions xmyz、厦一中、一中校园、综合素质评价、成绩单、成绩查询、成长记录、志愿者、社团、电子成绩单、待办审批、校园短信、菜单树，或学社、xmyzstudent、学生社区、唱票、实时唱票、抢票、票务、评分社区、声音问答、校园博物馆、辩论场、投票活动，或要查询本人的综评记录、成绩、成长记录、社团与志愿活动、短信通知，或要管理唱票活动、审核投稿、群发消息、管理博物馆与票务。
---

# 厦门一中双源站工具集：校内系统（只读）+ 学生社区（功能完备）

> **能力红线分工**：
> - **xmyz.xmedu.cn（校内系统）。仅用于快捷查询本人数据，
>   不得用于*攻击、压力测试、窥探隐私*；不得用于发布*涉黄、涉暴、危害国家安全、颠覆国家统一的内容*；
>   发现越权或泄露类问题时*只上报、不封装*。
>   由 `Access/HttpTransport.py::_guard` 强制拦截。
> - **xmyzstudent.com（学生社区，下称「学社」）——功能完备**。站点是学生自建平台，
>   唱票、审核、发布等写操作是需求本身；删除类方法名显式含 delete，批量操作先自查 id。
> 共同纪律：含未成年人个人信息——*账号信息、凭据、导出文件不入库、不外传*；
> 会话文件一律写仓库外用户目录。

两个源站：

| 门面 | 源站 | 鉴权 | 能力 |
|---|---|---|---|
| `XMYZClient` | `https://xmyz.xmedu.cn`（Struts2，`模块!方法.action`） | JSESSIONID | 纯只读，1176 只读端点 |
| `StudentHubClient` | `https://api.xmyzstudent.com/api/v2`（JSON API） | Bearer token | 284 REST + 2 WS，读写齐备 |

纯 HTTP 完成全部操作，无需浏览器。

---

## 三个前端入口

| 入口 | 技术栈 | 角色 |
|---|---|---|
| `manager.html` | ExtJS 3.4，服务端驱动按需加载 | **桌面管理端**，学校门户「登录」按钮指向的正式入口 |
| `m2.html` | Vue 3 + Vant，hash 路由 | 移动端新版，待办审批 + 4 项委托功能 |
| `m.html` | Vue 2 + Vux | 移动端旧版，已被 m2 取代 |

三者**共用同一 `JSESSIONID`**（`Path=/`，同源），一份会话通吃。

合并去重后 **2606** 个唯一端点（只读 1176 / 写类 1430；2026-10-24 真实会话对账，m2 已改版重建）。
**端点层几乎不重叠**（三方共有 0 个）——三个前端各写各的 Action 名；
功能层互补，桌面端没有 `activiti/*` 审批流，移动端没有 `quality/*` 综评面板。

---

## 登录

```bash
# ① 优先：有读图能力走 vision（实测 100%）
python tools/Access/LoginSession.py vision                                   # 取验证码图
python tools/Access/LoginSession.py vision -u <学号> -p <密码> --code ab12   # 看图后提交

# ② 无读图能力：OCR 变体池投票
python tools/Access/LoginSession.py password -u <学号> -p <密码> --retry 6

# ③ 浏览器已登录：直接复制会话，免验证码
python tools/Access/LoginSession.py jsessionid --jsessionid <JSESSIONID>

# 无凭据探测端点可达性
python tools/Access/LoginSession.py check
```

会话落在**仓库外**的用户目录（`%LOCALAPPDATA%\AutoXMYZ\session.json`，
类 Unix 为 `~/.local/share/AutoXMYZ/`）。`--out <PATH>` 可改到别处。

> 刻意**不写进仓库**：仓库里那份 `reference/.session.json` 只是占位模板。
> 靠 `.gitignore` 挡是「记得配才行」，靠路径隔离才是「不配也不会漏」。

**有读图能力却去用 OCR 是浪费；无读图能力却去用 vision 则会卡在 `--code`。**

---

## 使用

```python
import sys; sys.path.insert(0, "tools")
from XMYZClient import XMYZClient

c = XMYZClient()                  # 自动读用户目录下的会话（仓库外）
c = XMYZClient(token="<JSESSIONID>")

c.status()                        # 本人账号与学籍摘要
c.menuTree()                      # 有权访问的菜单树（端点清单权威来源）
c.quality()                       # 综合素质评价总表
c.myScores()                      # 我的成绩
c.transcript()                    # 电子成绩单
c.growthRecords()                 # 我的成长记录
c.myCommunities()                 # 我参与的社团
c.myVolunteerActivities()         # 我参与的志愿活动
c.inbox()                         # 短信收件箱
c.schoolTermCombo()               # 学期下拉
```

分页方法（`myScores` / `quality` / `inbox` / `growthRecords` …）返回 `(rows, summary)`，
内部按桌面端契约 `start` + `limit` 循环，上限 2000 行。

```bash
python tools/XMYZClient.py --health     # 会话自检
python tools/XMYZClient.py --summary    # 跨域摘要
python -B tools/TestCases/TestMethodSmoke.py   # 具名方法线上冒烟（GET+read 安全集）
```

成绩趋势（transcript 全量 → 科目×场次矩阵 / xlsx）：
`LifeOffice/ScoreTrend.py` 的 `collectTrend / toXlsx / toConsole`。）

---

## 命令速查

```bash
python tools/TestCases/TestApiReadOnly.py                  # 只读全量 35 项
python tools/TestCases/TestApiReadOnly.py --limit 20       # 冒烟
python tools/TestCases/TestApiReadOnly.py --report r.json  # 出报告
python tools/TestCases/TestContract.py                     # 契约与红线审计（离线）
```

---

## 端点与分页契约

- 桌面端分页参数是 `start` + `limit`（`Config.js` 里 `LIMIT=60`），**不是** m2 的 `page`/`pageSize`
- 响应有两类，**都要能处理**：
  - 信封型 `{"total": n, "data": [...], "success": true}`
  - **裸数组 / 裸对象**（`dict!getTree`、`grade!loadTree`、`recipient!statInfo`、`community!loadTree`）
- 业务失败是 `{"success": false, "message": "..."}`，**`success:false` 不等于端点不可用**
- `system/parameter!getParameterValue.action` 返回 AES-128-ECB 密文，密钥 `Tk8IVNJ8B75nHDgb`
- 字典清单约 400 个 `dictCode`，见 `reference/api.md`

完整端点清单、来源前端、只读探测结果见 **`reference/api.md`**。

---

## 端点清单怎么来的（`tools/Build/`）

2606 个端点不是静态扒出来的，是「登录 → 菜单树 → 定向抓模块」跑出来的（2026-10-24 重跑：桌面端 97/97 模块零漂移，m2 新版 2161 chunk 全量重提）。
想复现或站点改版后重建，按序执行：

```bash
python tools/Build/login591.py                            # ① 登录（复用 591iq 的 OCR）
python tools/Build/fetch_modules.py                       # ② 按菜单树抓 97 个 JS 模块
python tools/Build/merge_endpoints.py                     # ③ 三方合并去重
python tools/Build/probe_readonly.py                      # ④ 只读端点全量探测（约 13 分钟）
python tools/Build/gen_api_md.py                          # ⑤ 重生成 reference/api.md
python tools/Build/precommit_check.py                     # ⑥ 入库前检查：扫描 + 审计
```

关键点：桌面端的模块**由服务端菜单树下发**（`action.jsFile` 字段），
所以菜单树一次请求同时给出「端点清单 + 待抓 JS 清单」，不需要扫全站。

数据目录用环境变量指定，默认 `<仓库>/build_data`（**不入库**，含真实姓名与学号）：

| 变量 | 默认 | 用途 |
|---|---|---|
| `AUTOMXYZ_WORK` | `<仓库>/build_data` | 中间产物（`js/`、`endpoints.json`、`validation.json`） |
| `AUTOMXYZ_BUNDLE` | `AUTOMXYZ_WORK/bundles` | 存放 m.html / m2.html / manager.html 主 bundle |
| `IQ_SKILL` | `~/.config/opencode/skills/591iqAutomatic` | `login591.py` 借用的模板 |

---

## 学社（xmyzstudent.com）——功能完备侧

学生自建社区平台：实时唱票、投票征集、电子票务、评分社区、声音问答、校园博物馆、
辩论场、站内消息、宿舍楼宇。前端 `xmyzstudent.com`，API `api.xmyzstudent.com/api/v2`。

### 登录（Bearer token，四种方式）

```bash
# ① campus（推荐）：校园网账号 + 验证码，两步走，验证码图给读图模型看
python tools/StudentHub/HubSession.py captcha                       # 取图并暂存 jsessionId
python tools/StudentHub/HubSession.py campus -a <校园网账号> -p <密码> --code ab12
# ② OCR 兜底（需 rapidocr-onnxruntime）
python tools/StudentHub/HubSession.py campus -a <账号> -p <密码> --ocr 6
# ③ 站内账密 / ④ 浏览器复制 token（F12 → localStorage → token）
python tools/StudentHub/HubSession.py normal -u <用户名> -p <密码>
python tools/StudentHub/HubSession.py token --token <token>
python tools/StudentHub/HubSession.py check                          # 自检
```

### 使用

```python
import sys; sys.path.insert(0, "tools")
from StudentHubClient import StudentHubClient
c = StudentHubClient()                    # 自动读 %LOCALAPPDATA%\AutoXMYZ\hub_session.json
c.healthCheck()                           # /user/profile 有 username 即有效

# 唱票：看活动 → 录票 → 流水 → 撤销；大屏快照走 WS
c.getAdminTallyActivities()
c.voteAdminTallyCandidates(candidateId, 10)
c.getAdminTallyActivitiesRecords(activityId)
c.undoAdminTallyActivities(activityId)
c.wsSnapshots("/ws/tally/activity/%d" % activityId, print, seconds=10)

# 其它高频
c.getMessages(); c.getUnreadMessageCount()          # 站内消息
c.searchRatingItems("食堂")                          # 评分社区
c.getVoiceQuestions(); c.createVoicesQuestionsAnswers(questionId, "内容")   # 声音问答

# 会考练习（信息技术会考）
c.getMyOnlineExamCombo()                                    # 我的考试场
c.getQuestionBankCombo(examId=场id)                          # 题库
c.getMyAnswerStats(examId=场id)                              # 答题统计（一次返回全部题库）

# 选课 / 日程 / 心理预约 / 打卡 / 投票 / 评测（2026-10 全量补齐）
c.readElectiveCourseByStudentOrParent(**kw)                 # 我的选课课程
c.getComboStoreByStudentElective(**kw)                      # 可选课程下拉
c.readCalendar()                                            # 个人日程
c.readAppointment()                                         # 心理预约
c.getComboStoreWorkCard()                                   # 打卡任务
c.getFormVoteQuestion() / c.voteVoteResult(**kw)             # 投票
c.getEvaluationFormEvaluationItem(**kw)                      # 教师评测表单
各域完整方法表见 tools/<域>/<Mixin>.md
c.getPublicTicketActivities(); c.getTicketsMy()      # 抢票
c.getAdminMuseumEvents(); c.publishAdminMuseumEvents(id)        # 博物馆
```

284 个端点方法清单见 `reference/hub-api.md`（事实来源
`tools/StudentHub/HubEndpoints.py`，由 `Build/gen_hub_api_md.py` 派生）。
未包装端点直接 `c.get/post/put/delete(path, json=...)`。

### 契约要点

- 信封 `{code, message, data}`，**业务失败也是 HTTP 200**，`code!=200` 由传输层抛
  `HubError`（401 → `HubAuthError`，重新登录，不要换参数重试）
- 分页 `page` + `size`（部分端点 `pageSize`）
- **学社无写拦截**（与 xmyz 相反）：删除类方法名显式含 delete，
  `HubEndpoints.is_write(path, method)` 只做文档标注
- 站点为学生自建平台，写操作先确认身份与影响面；**不要碰他人隐私数据**

---

## 注意事项

- **校内系统写操作一律不做**。需要提交、审批、删除、改密码时，如实告知不在能力范围内，
  不要尝试绕过 `_guard`。学社侧写操作按上文红线纪律执行。
- `account/user!resetPassword.action`（重置他人密码）是教师常规功能，但**本技能不封装**。
- 会话会过期，报「会话无效」就重新登录，不要试图换参数绕过。
- 单账号、串行、限速 ≥180ms，遇 4xx/429 立即停手。
- 探测未知端点时 `id` 一律用不存在的 `-1`，`limit=1`，**不要遍历真实 id**。
- 入库文档里禁止出现真实姓名，一律写「某学生」。
- `reference/` 体积上限 150 KB：原始 JSON（含姓名、学号、会话）留在本机临时目录，不入库。
- **提交前必跑** `python tools/Build/precommit_check.py`：会话泄漏、`.pyc` 明文、
  硬编码凭据一次全查（`.pyc` 曾实测把「字符元组拆开存」的凭据还原成明文）。
# AGENTS.md

**双源站**工具集：厦门一中校内系统（xmyz.xmedu.cn，只读）+ 学生社区
（xmyzstudent.com，功能完备）。纯 HTTP，无需浏览器。

## 架构

多源站聚合：**每源站 = 一个门面 + 一套传输/会话 + 若干业务域目录**。
未来站点（心意我 / hfs / 校园网）按同模式加目录 + 门面注册。

```
tools/
  XMYZClient.py                  门面①：xmyz.xmedu.cn，纯只读（_guard 强制）
  endpoint_kind.py               xmyz 端点读写分类的唯一权威判定
  Access/HttpTransport.py        xmyz 传输层：_call / get / post / paged / login / _bindUser
  Access/LoginSession.py         xmyz 登录四种方式：password / jsessionid / vision / check
  StudentBase/ProfileDict.py     身份、字典、学期、班级、网络磁盘
  LifeOffice/StudyMessage.py     成绩、成绩单、成长记录、作业、短信、通知、附件
  QualityCenter/QualityRead.py   综合素质评价（quality 域，20 个读取方法）
  CommunityCenter/VolunteerRead.py  社团（community）与志愿服务（volunteer）
  ExamCenter/ExamPractice.py     会考练习（信息技术会考）与在线考试
  StudentHubClient.py            门面②：学社 xmyzstudent.com，功能完备（含写）
  StudentHub/
    HubTransport.py              学社传输层：Bearer、信封解包、限速、upload、WS 快照
    HubSession.py                学社登录四种方式：campus(+vision 验证码) / normal / sms / token
    HubEndpoints.py              学社端点注册表（284 REST + 2 WS，事实唯一来源）
    AccountMixin.py              auth / user / sms / permissions
    PortalMixin.py               横幅 / 年级绑定 / 文件上传 / 音乐 / QQ音乐
    MessageMixin.py              站内消息（收件箱 + 管理端群发/模板）
    TallyMixin.py                实时唱票（含 WS 快照订阅）
    CampaignMixin.py             投票征集活动（投稿 / 投票 / 后台审核）
    TicketMixin.py               电子票务（活动 / 抢票 / 核销 / 审核）
    MuseumMixin.py               校园博物馆（事件 / 区块 / 标签 / 瞬间审核）
    RatingMixin.py               评分社区（浏览 / 投稿 / 评分 / 评论 / 后台 74 端点）
    VoicesMixin.py               声音问答（提问 / 回答 / 举报 / 后台治理）
    AdmissionMixin.py            纳新/准入（分组/成员/豁免/扫码 + 用户验证，2026-10 新增）
    CampusMixin.py               校区 / 楼宇 / 时段 + 管理端用户检索
    DebateMixin.py               辩论场管理（含 WS）
  TestCases/TestApiReadOnly.py   xmyz 只读 35 项探测，可重复运行
  TestCases/TestContract.py      仓库契约与能力红线审计（离线，无网络无凭据）
  TestCases/TestHub.py           学社契约审计（离线：注册表/门面/传输 mock/文档一致）
  Common/Logcat.py               彩色分等级日志（内部诊断；单例 `Log`）
```

- `reference/api.md` — xmyz 端点清单（本仓库 xmyz 侧唯一参考文档）
- `reference/hub-api.md` — 学社端点清单（由 `Build/gen_hub_api_md.py` 从注册表派生）
- `SKILL.md` — skill 定义
- 每个 `.py` 都有同名 `.md`（门面 `XMYZClient.py` 豁免）
- 每个业务目录有 `__init__.py`

## 红线

**两套能力模型，不要混：**

1. **xmyz（校内系统）读写均可用（2026-10-24 政策修订）。** 早年 `_guard` 强制拦截已解除，
   `endpoint_kind.kind()` 仅作文档/统计口径：

- 判定逻辑**只有一份**，在 `tools/endpoint_kind.py::is_write`，已用全量 2606 端点校验
  （1176 只读全放行 / 1430 写端点全拦截）。写判定除前缀表外还有
  **后缀通则**（`WRITE_SUFFIX`：*Complete/*Approval/*Save/*Create/*Update——
  新版 m2 上百个工作流动作靠它归位，逐个枚举必漏）
- `_guard` 只做**转发**，不得在传输层维护第二套名单 ——
  曾经在 `_guard` 里另写白名单，结果误拦 230/360 个只读端点，
  同时把 `toDraft`/`signAll`/`setRead`/`resend` 这些写动作放行了（见「已踩过的坑」第 3 条）
- 同名两义按 namespace 分流（`attachment!send` 读 / `short-message-detail!send` 写），
  例外清单也写在 `endpoint_kind.py`，不散落各处
- `_call` 是唯一出口，**不得新增绕过 `_guard` 的调用路径**

2. **学社功能完备（含写）。** xmyzstudent.com 是学生自建平台，写操作是需求本身：
- **不设 _guard**；`HubEndpoints.is_write(path, method)` 只是文档标注（语义与 xmyz 相反）
- 删除类方法名显式含 delete；批量删除调用前自查 id 列表
- 端点事实只有一份：`HubEndpoints.py`；`reference/hub-api.md` 与各 Mixin `.md`
  全部由 `Build/gen_hub_api_md.py` 派生，**改注册表不改文档 = TestHub 报漂移**

新增能力时：先判断属于哪个源站。xmyz 与学社读写都可加；
**写纪律**：只写本人数据、可逆优先（create→delete 闭环验证）、
不碰他人密码（`resetPassword` 不封装）、不碰他人审批流、删除类先查 id。

## 开发契约

- 命名：目录大驼峰、模块文件大驼峰、类大驼峰、方法小驼峰、常量 UPPER_SNAKE
- **文件名不得重复目录名**；**目录名禁止与标准库同名**（`types`/`json`/`code`…）
- 每业务一个目录 + 每个 py 一个同名 `.md`；新增业务域 = 新目录 + mixin + md + 门面注册
- **日志分工写死**：结论一律 `print` 走 stdout；内部诊断一律 `from Common.Logcat import Log` 走 stderr
  统一用单例 `Log`，不要在业务模块再实例化
  ⚠️ DEBUG 日志含凭据与个人信息，**不得提交进仓库**
- `Http` 必须留在 `XMYZClient` 继承链末位（基类）
- 对外 API 只增不改；改方法名必须同步门面、测试、SKILL.md、api.md
- **新功能一律先在系统临时目录原型化**，确认要长期维护才移入 `tools/`；
  一次性探针**用完即删**（含凭据）
- 探针脚本里写死的账号密码**只进环境变量不进 argv**，用完 `Remove-Item Env:` 清掉
- **代码与文档不得绑定特定 AI 工具 / IDE**，不写死工具私有路径
- **禁止用正则批量替换目录名**——会误伤 API 路径与字段名
- **argparse 的 help 字符串里不能留裸 `%`**：`--help` 会对 help 再做一次 `%` 格式化，
  `ValueError: unsupported format character` 就是这么来的
- ⚠️ **改这些文件不要用 PowerShell here-string**：反引号会被当转义符吃掉。
  要批量改就写一个 Python 补丁脚本再执行

## 已踩过的坑（改代码前先读）

1. **`loggedIn` 不能判会话**。未登录时 `status.action` 返回 `{"loggedIn":false}`，
   登录后该字段**直接消失**，`get()` 返回 `None`。`== False` 判会误报未登录，
   `== True` 判则永远失败。判据是 profile 里有无 `loginName`/`id`。

2. **`Http.__init__` 默认路径必须自己读会话文件**。曾写成 `elif cookie:`，
   于是无参构造（门面最常见用法）**静默以未登录身份运行**；
   而未登录时多数只读端点照样返回 200 —— 测试「全绿」而一条真实数据都没取到。
   排查假阳性时先确认 `menuTree()` 非空、`status()` 有 `loginName`。

3. **端点分类不能靠正则硬拼**。旧实现每分支后接 `\.action$`，
   `approve` 只匹配到 `approvedComplete` 前 7 字母就接不上，**漏判 88 个**写端点。
   正确做法见 `endpoint_kind.py`：先取动作名，再做词元判定。

4. **只读探测的判定不能只认信封**。本系统有裸数组 / 裸对象响应
   （`dict!getTree`、`grade!loadTree`、`recipient!statInfo`、`community!loadTree`），
   只认 `{"success":...}` 会误报 5 个 FAIL。**解析出 JSON 即 ALIVE，空数组也算。**

5. **`send` 同名两义，必须按 namespace 分流**。`system/attachment!send` 是**下载**（读）；
   `message/short-message-detail!send` 是**真发短信**（写）。
   只按动作名判会把只读端点拦死、或把写端点放行 —— 两边都是事故。

6. **`.pyc` 会把编译期常量还原成明文**。`scan_sensitive.py` 把学号/密码/姓名
   拆成字符元组 `_PARTS`，源码里确实没有连续明文；但 `py_compile` 之后，
   字节码里那几个元组就是**重新拼好的明文串**。而扫描器当时只读文本、
   且主动 `skip __pycache__` —— 泄漏从它眼皮底下走了过去。
   现在的处理：扫描器同时扫二进制、不跳过 `__pycache__`，且
   `precommit_check.py` 的闸①直接判 `__pycache__`/`*.pyc` 存在为**失败**。
   **拆字符串不是防泄漏手段，别把它当保险。**

7. **两层覆盖没有等价性测试，缺口靠用户点破**（2026-10-24 考试域事件）。
   注册表层（流水线，持续增长到 2625）与具名方法层（手写 mixin，初期范围冻结）
   长期脱节：考试域 10 个端点在册、客户端却只有泛化调用，直到用户问
   「这个没在技能吗」才暴露。对策：发现/新增功能域时**立即建域**
   （目录 + mixin + md + 门面注册），不要用「泛化调用能跑」当借口；
   新菜单模块进注册表时，同步在对应域 md 里登记。

7. **入库前检查器会污染它自己检查的东西**。`precommit_check.py` 的契约审计要
   import 模块，若不设 `PYTHONDONTWRITEBYTECODE=1`，跑一次就长出 `__pycache__`，
   下一次跑闸①必然失败 —— 检查器永远在报上一次运行留下的产物。
   两道保险：子进程一律 `-B` + 环境变量；闸①排在**最后**做兜底扫。

## 常用命令

```bash
# xmyz 校内系统（只读）
python tools/Access/LoginSession.py check                                   # 无凭据探测
python tools/Access/LoginSession.py vision -u <学号> -p <密码> --code ab12  # 登录（有读图能力）
python tools/Access/LoginSession.py password -u <学号> -p <密码>            # 登录（OCR）
python tools/XMYZClient.py --health                                          # 会话自检
python tools/TestCases/TestApiReadOnly.py                                    # 只读 35 项

# 学社（功能完备）
python tools/StudentHub/HubSession.py captcha                                # 取验证码图
python tools/StudentHub/HubSession.py campus -a <账号> -p <密码> --code ab12 # 校园网账号登录
python tools/StudentHub/HubSession.py token --token <localStorage.token>     # 浏览器复制 token
python tools/StudentHubClient.py --health                                    # 会话自检

# 审计（全离线）
python tools/TestCases/TestContract.py                                       # 仓库契约
python tools/TestCases/TestHub.py                                            # 学社契约
```

## 发布前必跑

```bash
python tools/TestCases/TestHub.py        # 学社契约（含文档一致性）
python tools/Build/precommit_check.py    # 四道闸：产物 / 敏感串 / 会话模板 / 契约审计
```

外加 `reference/` 未超 150 KB（api.md + hub-api.md 合计）。

⚠️ **本仓库内不要用 `py_compile` / `compileall` 做语法校验** —— 它们会写出
`__pycache__`，正是闸①要拦的东西（见「已踩过的坑」第 6 条）。用内存编译：

```bash
python -c "import sys; compile(open(sys.argv[1],encoding='utf-8').read(), sys.argv[1], 'exec')" <file>
```

## 依赖

requests、rapidocr-onnxruntime（验证码 OCR）、numpy + Pillow（预处理）。

## 安全纪律

- 提交前脱敏：不得包含密码 / 会话 id / 姓名 / 学号 / 班级 / userId
- 入库文档禁止出现任何真实姓名（含本人与他人），一律写「某学生」
- `reference/.session.json` 是**占位模板**，没配 .gitignore 也不会漏 ——
  真实会话默认写在仓库外的用户目录（`%LOCALAPPDATA%\AutoXMYZ\` / `~/.local/share/AutoXMYZ/`），
  由 `HttpTransport.SESSION_FILE` 决定，可用 `AUTOMXYZ_SESSION` 或 `--out` 覆盖
- 学社侧同理：`hub_session.json` / `hub_captcha_pending.json` 都在仓库外同目录，
  由 `HubTransport.SESSION_FILE` / `CAPTCHA_PENDING_FILE` 决定，`AUTOMXYZ_HUB_SESSION` 可覆盖
- 学社文档/示例不得出现真实 token（32+ hex 由 TestHub 安全闸拦截）、手机号
- 每加一条合规红线，必须配一条能证明它会红的**反向用例**
  （恒 PASS 的检查是装饰品）；反向用例不得真删文件，只 monkeypatch 或改临时副本，`finally` 还原
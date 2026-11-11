# AGENTS.md

新壹我综合素质评价系统（www.591iq.cn）自动化工具集。纯 HTTP，读操作不需要浏览器。

## 架构

`tools/` 按业务域分目录，**每个目录 = 一个业务域**，门面 `IqClient.py` 留在 `tools/` 根：

```
tools/
  IqClient.py                     门面：组合下列各域 mixin，对外 API 就是 IQClient
  Access/HttpTransport.py         传输层：_call / get / post / login / userId + IQError
  Access/LoginToken.py            登录（获取 sso Token 的四种方式）
  StudentBase/ProfileInfo.py      本人档案、家长、兴趣特长
  StudentBase/DictOptions.py      平台字典、学期、活动/荣誉类型枚举
  HomeWorkbench/TaskAndMessage.py 待办任务、未读消息、公告
  RecordCenter/RecordQuery.py     写实记录读取（列表/标签/统计/详情）
  RecordCenter/RecordWrite.py     图片上传、发布写实记录
  RecordCenter/PublishActivity.py 活动记录发布/编辑 CLI（--yes 才写，--dry-run 只读）
  RecordCenter/DeleteRecord.py     写实记录删除 CLI（--yes 才删，--dry-run 只看目标）
  RecordCenter/RecordComment.py   记录/活动评论互动 CLI（发删 --yes 才写，回执核条数）
  EvaluateActivity/SummaryWrite.py 活动总结域（写）：提交/重交、总结状态回读
  EvaluateActivity/AutoDraft.py    总结自动草稿 + 批量计划生成（只读）
  EvaluateActivity/SubmitSummary.py 总结提交 CLI（单条/批量/失败续跑，--yes 才写）
  AppsCenter/IntegralQuery.py     积分应用（读）：排名/流水/勋章/兑换信息
  AppsCenter/SurveyQuery.py       问卷应用（读）：任务/题目/历史作答
  AppsCenter/AppsQuery.py         应用中心只读 CLI（integral/prizes/exchanges/surveys）
  GrowReport/GrowthReport.py      成长报告列表与详情
  GrowReport/GrowthStatistics.py  荣誉统计、活动维度统计
  GrowReport/GrowComment.py       成长报告自我总结读写 CLI（覆盖式，--yes 才写）
  Export/ExportXlsx.py            个人综评全量数据导出 xlsx（13 sheet）
  Export/ExportSummaryList.py     活动课程总结清单导出（已交/未交/可编辑重交）
  Export/XlsxWriter.py            共用的最小 xlsx 写出器（纯标准库 zipfile）
  TestCases/TestApiReadOnly.py    只读 52 项（加 `--upload` 满 53 项）
  TestCases/TestRecordRead.py     13 项
  TestCases/TestContract.py       仓库契约与卫生审计（离线，无网络无凭据）
  TestCases/ApiCoverageAudit.py   端点覆盖审计（bundle 清单 vs 封装集，同族缺口报告）
  Release/PackSkill.py            技能包打包（XinYiWo.zip，根目录结构；仅自检，不再单独发版）
  Common/Logcat.py                彩色分等级日志（内部诊断用；默认 stderr+WARNING，单例 `Log`）
  Feedback/FeedbackClient.py      反馈接口投递（独立服务，非 591iq 网关，不注册门面）
  Feedback/Ticket.py              工单HTML 模板 + 学号脱敏 + 投递前敏感信息闸门
  Feedback/SendFeedback.py        反馈工单 CLI（--dry-run 预览 / --yes 真发）
```

- `reference/api.md` — 端点清单；`reference/frontend.md` + `reference/recordForms.json` —
  学生端 22 类写实记录的字段/必填/平台提示（由前端组件提取，只存结论不存原始代码）；
  `SKILL.md` — skill 定义
- 每个 `.py` 都有同名 `.md` 说明
- 每个业务目录有 `__init__.py`（**必需**：否则会退化成 namespace package，
  与标准库同名目录冲突时会被标准库抢先）
- 拆分依据：目录 = 端点前缀聚类 + 业务语义（**只放一个文件的域应合并进更宽的目录**，
  如档案与字典同属学生端基础数据 → `StudentBase/`）；文件 = 域内职责（读/写、报告/统计）

## 开发契约

- 命名（对齐 Java 命名，2026-10-02 起）：**目录大驼峰**（`RecordCenter/`），
  **模块文件大驼峰**（`RecordQuery.py`），类大驼峰（`IQClient`/`QueryMixin`），
  **方法小驼峰**（`taskStats()`），常量 UPPER_SNAKE；禁止下划线与短横线做目录/模块名
- **文件名不得重复目录名**（不要出现 `StudentBase/StudentBase.py` 这类冗余）
- **目录名禁止与标准库同名**（`profile`、`types`、`code`、`json`… 会冲突），
  复合名同时解决可读性与冲突
- 每业务一个目录 + 每个 py 一个同名 .md 说明；说明含：职责、对应端点、方法清单、最小用法、注意事项
- 新增业务域 = 新目录（含 `__init__.py`）+ mixin + 说明 + 在 `IqClient.py` 门面注册
- **唯一例外**：`Release/`（仓库维护工具，与 591iq 平台 API 无关）**不注册门面**，
  其模块也不 mixin 进 `IQClient`；它仍需同名 `.md` 说明与 `__init__.py`
- **门面例外**：`Feedback/` 与 `Release/` 同理——反馈接口是独立服务
  （`feedback.mclhz.de5.net`，裸 JSON、不带 AccessToken），**不注册门面**、不 mixin。
  `Common/` 是通用工具（Logcat），同样不注册门面，仅被内部模块 import
- **日志分工写死**：给 AI/用户看的结论一律 `print` 走 stdout；内部诊断一律
  `from Common.Logcat import Log, setVerbose` 走 stderr。**统一用单例 `Log`**，
  不要在业务模块里再 `Logcat()`，否则一份日志散到两个实例、等级各调各的。
  打开 DEBUG：CLI `--verbose` 或环境变量 `IQ_VERBOSE=1`。
  ⚠️ 脱敏**只挡密码与身份证**（用户 2026-10-05 定调），token/会话/姓名/学号原样输出——
  所以 DEBUG 日志含凭据与个人信息，**不得提交进仓库**。
- `Http` 必须留在 `IQClient` 继承链末位（基类）
- 对外 API 只增不改；改方法名必须同步 `IqClient.py` 门面、两个测试、SKILL/README/api.md
- **改目录/模块名只改 import 语句与文档路径**；API 路径（`/record/...`）、
  JSON 字段（`recordType`/`recordContent`）、方法名（`records()`）里的
  `record`/`grow` 等词**不受目录改名影响**，不要一起替换
- **禁止用正则批量替换目录名**——会误伤 API 路径与字段名；逐条精确替换并做内容完好性断言
- **新功能一律先在系统临时目录原型化，不得直接写进 skill 源码目录**：
  探索脚本、一次性探针、dump 文件一律放 `%TEMP%\591iq_scratch\`（自建，不依赖任何
  特定 AI 工具/编辑器的私有目录约定）；
  确认「确实有用且要长期维护」后，才整理成符合本契约的模块移入 `tools/`，
  并补同名 `.md`、加入 `README`/`SKILL`/`AGENTS`。**不要让半成品、临时产物、
  未验证脚本长期盘踞源 skill 目录**（`%TEMP%\591iq_scratch` 里的东西含凭据，严禁入库）
- **原型必须有出口**（上面那条的后半段，2026-10-11 补）：验证完立刻分诊——
  **有用的移入 `tools/`，无用的当场删**；一个专题做完（发一条记录 / 删一项能力 /
  生成一批材料）**盘点一次**。别让几十个一次性探针永久堆积：
  它们既是噪声，也是凭据泄漏的来源（见下一条）。
  ⚠️ **不要把一次性脚本迭代成 v2/v3/v4**：能用一次说清的，结论直接进文档；
  迭代出多版的，多半是前几版在试错而不是在验证。
- **兄弟清扫**（2026-10-25，点赞漏检教训）：从某个 chunk 建成模块时，必须把该 chunk 内
  **全部 `"/xxx"` 路径字面量列出来逐条分诊**（封装 / 留档 / 排除）——教训是取了评论
  四口就把同 chunk 的 `favour`/`collect` 挑剩了。复跑同族缺口用
  `tools/TestCases/ApiCoverageAudit.py`（bundle 清单 vs 封装集差集报告，只读）。
- **`%TEMP%\591iq_scratch` 自身含凭据与个人信息，且不被现有闸门覆盖**：
  盘点发现全量快照 JSON 里会有会话凭据、明文身份证、考号、同班同学姓名、
  家长/教师评语；日志里有真实 `JSESSIONID`；探针脚本里硬编码了凭据。
  处置纪律：① 全量快照**分析完即删**，要留结论就只留统计字段；
  ② 含 `JSESSIONID` 的登录日志用完即删；③ 一次性探针随原型结束即删。
  **发布前体检要扩到覆盖 `%TEMP%\591iq_scratch` 全目录**，不能只扫对外产物——
  否则源码与临时产物成了一条绕过闸门的通路。台账见「开发记忆 §8.3」。
  ⚠️ 探针脚本里写死的账号密码，**只进环境变量不进 argv**，且用完 `Remove-Item Env:` 清掉。
- **代码与文档不得绑定特定 AI 工具 / IDE**：不写死 `%TEMP%\opencode\`、`%TEMP%\claude\`、
  `.opencode/`、`.cursor/` 等工具私有路径与配置名；工具专属约定只允许出现在 `SKILL.md`
  的调用说明里，工具无关的行为（临时目录、缓存、产物路径）一律用项目自己的名字
  （本项目为 `591iq_scratch` / `591iq_*.xlsx`）
- **Git 大小写**：仓库已设 `core.ignorecase=false`；仅改大小写必须 `git rm --cached` + `git add` 两步登记。
  Windows 上文件系统大小写不敏感，`git mv A a` 可能「假成功」，**必须走临时名两段式**
  （`git mv A A__tmp && git mv A__tmp a`），改完用 `git ls-files` 复核索引里的真实大小写。
  ⚠️ Windows 上 Python 导入也不敏感，改错大小写测试仍可能全绿——改名后必须跑一次
  **大小写审计**（按 `git ls-files` 校验每个 import 路径按原样大小写可命中），别只信测试结果
- 提交：一次一个 commit，按步骤提交（用户要求）；每个 commit 后推送
- **每个 py 都要有同名 `.md`**；门面 `IqClient.py` 与最小写出器 `XlsxWriter.py`
  是 `TestContract.py` 里唯一两个豁免项，新增豁免前先想清楚是不是该补文档
⚠️ **改这些文件不要用 PowerShell here-string**：2026-10-04 在 `@"..."@` 里写反引号，
  反引号被当转义符吃掉，5 处代码标记损坏、`\t` 还被解释成 TAB。
  要批量改就写一个补丁脚本文件再执行
- **argparse 的 help 字符串里不能留裸 `%`**：`--help` 会对 help 再做一次 `%` 格式化，
  ``ValueError: unsupported format character 'T'`` 就是这么来的。
  连 ``"默认 %%TEMP%%\\%s" % NAME`` 这种「先 %% 转义再 % 代入」的写法也不行——
  `%` 运算后仍会留下裸 `%T`。**help 文案里索性别用 `%`**。
  已两次踩坑（`VisionLogin.py`、`PackSkill.py`），均由 `TestContract.py` 的 `-h` 冒烟当场抓住

## 常用命令

```bash
# 从仓库根目录执行
# —— 门户登录：有读图能力走 VisionLogin（实测 100%），否则走 LoginToken 的 OCR（50%）
python tools/Access/VisionLogin.py new                               # ① 取验证码图（无需凭据）
python tools/Access/VisionLogin.py submit -u <学号> -p <密码> --code ab12   # ② 看图识别后提交
python tools/Access/LoginToken.py password -u <学号> -p <密码>      # 无读图能力时的 OCR 路径
python tools/Access/LoginToken.py token <32hex>                  # 校验已有 token
python tools/IqClient.py <ssoToken>                       # 验证并打印摘要
python tools/TestCases/TestApiReadOnly.py --token <ssoToken>    # 只读全量 52 项
python tools/TestCases/TestApiReadOnly.py -u <学号> -p <密码>    # 门户登录换 token → 只读 52 项
python tools/TestCases/TestApiReadOnly.py -u .. -p .. --upload  # 53 项（追加上传项，会落一个文件）
python tools/TestCases/TestRecordRead.py <ssoToken>              # 写实记录 13 项断言
python tools/Export/ExportXlsx.py --token <ssoToken>            # 综评全量导出 xlsx（13 sheet）
python tools/Export/ExportSummaryList.py --token <ssoToken>     # 活动总结清单导出 xlsx
```

## 关键注意事项

- 请求体必须是 `request={"data":{...}}` form 编码；发 JSON 会 `code:10`
- 写操作（`RecordCenter/RecordWrite.py`）调用前必须向用户确认；成功判据 = 读回执
  （如 `querySummary.pdlist` + `count_task.unfinished`），不看返回值
- **发布活动记录走 `RecordCenter/PublishActivity.py` CLI，不要写一次性脚本**：
  登录/上传/定位 id/回读校验每次都一样，脚本不沉淀等于每次重抄；
  写入必须显式 `--yes`（代表已确认），只读预览用 `--dry-run`（连图片都不上传）；
  退出码 0 成功 / 2 服务端拒绝 / 3 回执不一致 / 4 token 失效 / 5 前置校验失败。
- `querySummary` / `sysDict` 返回 `{list:[…]}` 或 `{pdlist:[…]}`，不是裸数组；
  **不可对返回值直接 `.get(code)`** —— 需要 code→name 映射时遍历 `["list"]`（见 `RecordWrite._semesterName`）
- **响应信封有两种**：`{code,msg,data}` 与 `{meta:{code,msg},…}`（已确认家长评语提交属后者）。
  判断 code/msg 只能用 `Access/HttpTransport.py` 的 `unwrapEnvelope()`，
  **不要在别处重写「取顶层 code」** —— 那正是 D17 的成因（失败被当成成功）
- `records()` 的 `type_` 参数带下划线（避免遮蔽内置 `type`），用关键字传
- **门户登录必须先判断自身有无读图能力，再选路径**：
  有 → `Access/VisionLogin.py new` → 读「识图推荐」PNG → `submit --code`（实测 30/30，累计 46/46）；
  无 → `Access/LoginToken.py password`（OCR 42/70 ≈ 60%，靠 `--retry` 兜底）。
  **有读图能力却去用 OCR 是浪费**；无读图能力却去用 VisionLogin 则会卡在 `--code`。
  退出码按契约分支：0 成功 / 2 验证码错（换图重试）/ 3 凭据或网络错（**换验证码无用**）。
  `--interactive` 用 `input()` 阻塞，**仅真人终端可用，agent 不得使用**。
  验证码**长度 4 或 5 位不定**，不要按固定 4 位处理。
- **查未知槽位结构按优先级链走**（详见 `reference/api.md`「未知槽位结构怎么查」）：
  ① 查 `reference/frontend.md` + `recordForms.json`（22 类已全覆盖，本地查表）
  → ② 反查本校 feed 样本 → ③ 查 `api.md` + `RECORD_TYPE_MAP`
  → ④ 按 `recordForms.json` 里的 `chunk`/`moduleId` 定位那一个 chunk
  → ⑤ 全量搜 564 个 chunk（约 2.5 min，**仅在前四步全失败时**）。
  禁止从第 ⑤ 步起手；翻 bundle 必须先映射定位、落盘建索引，并区分发布态/查看态 chunk
- **`reference/` 体积上限 150 KB**（2026-10-11 实测已用 **109.3 KB**：`api.md` 39.4 +
  `recordForms.json` 47.3 + `frontend.md` 19.7，另有 gitignored 的受限文档 2.8；
  原 100 KB 预算于 2026-10-05 抬高，
  原因见「开发记忆 · Phase 1」）：只放提炼后的结论，
  **原始前端代码、chunk、映射中间产物一律留在 `%TEMP%\591iq_scratch`，不入库**。
  （`reference/frontend-js/` 那 13 MB 原件也算这类：已 gitignore 且 PackSkill 排除。）
  要加内容先减：表格按类聚合、不要逐字段成行；`frontend.md` 的表格以
  `recordForms.json` 为准（生成脚本未入库），改 JSON 后要同步改 md 里的表
- PowerShell 5.1：不要用 Get-Content/Set-Content 处理 UTF-8 中文（会乱码），用文件工具或 python
- **导出（`Export/`）只读，但产出含学生个人信息**：默认写 `%TEMP%\591iq_*.xlsx`，
  已 gitignore `*.xlsx`；不要把导出文件或含真实姓名的 json 提交进仓库
- 提交前脱敏：不得包含 token / 密码 / 姓名 / userId / 班级
- **入库文档里禁止出现任何真实姓名**（含本人与他人），一律写「某学生」。
  敏感串扫描抓不到散文里的中文人名（通用检测必然误报，见 SENSITIVE 注释），
  所以靠这条人工约定 + 两条窄规则兜底（带计数后缀的「某（2 封）」形态、夹具 userId）
- **每加一条合规红线，必须配一条能证明它会红的破坏用例**（2026-10-11 补）：
  恒 PASS 的检查是装饰品，只说明它对当前这版代码成立。`TestContract` 的「能力红线」
  项已带反向用例（移除白名单 / 移除归属校验 / 关闭脱敏 → FAIL，还原 → PASS）。
  新增红线时照此补；自证粒度与成本分档见「开发记忆 §8.1」。
  ⚠️ 反向用例**不得真删**：只 monkeypatch 或改临时副本，`finally` 还原。
- **节流与节制**：单账号、串行、禁止并发；分页与导出有硬上限（`ExportXlsx.py` 的 `while off < 2000`）；遇 4xx/429 立即停手
- 测试需要有效 ssoToken；无 token 时 `TestApiReadOnly.py` 的登录步骤会失败
- **删除类操作（`RecordCenter/DeleteRecord.py`）默认只读**：先 `--dry-run` 看清目标（id/类型/标题/学期/图片数），再显式 `--yes`；删除**不可撤销**。
  `TestApiReadOnly.py` 里的 `record/delRecord` 用例只用 32 个 `0` 探测路由存在性，**任何情况下都不得改成真删**
- 端点命名规律：删除类一律 `del` 前缀（`delRecord` / `delSummary` / `delComment` / `reviewDel`），**不是** `deleteRecord`。查删除接口别只 grep `delete`

## 版本与发布规范

- **版本号唯一落点是仓库根 `VERSION`**，内容必须与 release tag **逐字一致**（含 `v` 前缀）
- **禁止在 README / SKILL / 代码注释里手写版本号**——多处必然漂移；文档只说「见 VERSION」
- 手动发版（**本仓库无 CI 发布流程**）：
  1. 改 `VERSION`
  2. 提交 `chore(release): 升版到 <v>`
  3. `git tag -a <v> -m "<v>"` → `git push origin <v>`
  4. 在 GitHub 网页端建 Release、勾 **Pre-release**、粘贴说明、点发布
     → `.github/workflows/release.yml` 会在 `release: published` 时自动打包
       并把 `XinYiWo.zip` 挂为该 Release 的附件（用 runner 自带 `GITHUB_TOKEN`，
       本地不需要任何令牌；预发布同样会触发）
- 命名：`v0.1-betaN`（预发布）→ `v0.1.0`（首个可用版）→ **`v1.0.0` 起走严格 SemVer**，
  即 `MAJOR.MINOR.PATCH`，破坏性改动升 MAJOR，新增能力升 MINOR，修 bug 升 PATCH。
  已知 `v0.1-betaN` **不是严格 SemVer**（规范写法 `v0.1.0-beta.1`），
  GitHub 正常但 SemVer 工具无法排序先后——有意选择，记录在案。
  ⚠️ **`v1.0` 不用写三段**：tag 用 `v1.0`（GitHub 惯用），
  `VERSION` 与 tag 逐字一致即可（`AGENTS.md:187`），不强制补 `.0`。
  `v1.0` 的重大改动是**删除遴选/投票域与人员枚举能力**（对下游是 breaking），
  所以从 `v0.1-beta2` 直接跳 `v1.0` 而非 `v0.1.0`——这个决定记在案。
- 发版前必跑：`compileall` + `TestContract.py` + 敏感串扫描 +
  `reference/` 未超 150 KB；线上回归（`TestApiReadOnly` / `TestRecordRead`）在本地跑
- **打包规则**（实现在 `Release/PackSkill.py`，规则改这里，别改 workflow）：
  · 文件来源 `git ls-files`，额外排除 `.github/` 与 `.gitignore`（流水线配置与 git 内部约定不必随包分发）
  · 产物固定名 `591iqAutomatic.zip`（历史；现包名 `XinYiWo.zip`），**根目录结构**：`SKILL.md` / `tools/` / `reference/` 直接在顶层，**不套外层目录**（与 GitHub 自动源码包不同）
  · 因此安装要自己先建目录：`mkdir -p ~/.config/opencode/skills/<技能目录名>` 再解压进去；这一步必须写进 Release 说明
  · 打包后自检：根目录必备齐全、未套层、包内无 .git/.github/__pycache__/*.pyc/*.xlsx/图片，
    并输出 **sha256**；Release 说明注明「以 tag 为准，zip 是同快照的便利副本」
  · `--version-check` 强制 VERSION 与 tag 逐字相同，`--require-clean` 拒绝把本地脏改动打进包
  · 打包结构由 `TestContract.py` 第 13 项每次 CI 都验，改规则当天就能发现坏掉

## 依赖

requests、rapidocr-onnxruntime（验证码 OCR）、numpy + Pillow（预处理）

`Export/` **只用标准库**（`zipfile` + SpreadsheetML），不要引入 pandas / openpyxl——
保持「无重依赖即可导出」。

---

## 变更历史（原 CHANGELOG.md，并入）

本文件记录对外可见的变更。**用户可见的功能/行为变化才写这里**，
内部重构、中间提交不写——那些在 `git log` 里。

版本号唯一落点是仓库根 `VERSION`，本文档不写死版本号，只按标题标注。

---

### 未发布（v1.1 之后，2026-10-25）

自 v1.1 起累计 7 个提交、14 个文件、+498/−11。**纯增量、无破坏性变更。**
v1.2 已发布（tag `v1.2`），`VERSION` 已对齐；契约的「VERSION 与最近 tag 一致」检查转 PASS。

#### 维护（2026-11，登录链路健壮性）

- 门户登录的菜单树探测改为**先判 HTTP status + Content-Type**：瞬时 503/风控 HTML
  报“服务端瞬时不可用，请稍后重试”，不再伪装成“凭据/会话错”。
- `verify(ssoToken)` 响应非 JSON 时返回可读原因（含 HTTP 码），不再是裸
  `JSONDecodeError` 文案。
- `serverTime` 预热探测改为 **best-effort**：404/非 JSON/网络异常 → 打印原因并跳过，
  返回 0，不再 `int()` 裸解析崩掉整个登录（实测 2026-11-11：匿名探测会被门户
  认证门卫以 404 页/302 两种形态拦截，属正常现象；真机登录成功后 200+JSON，
  预热值本身可有可无）。归档仓 591iqAutomatic（v1.2 只读）不再回同步，本仓库
  为唯一活体。

#### 新增

- **互动补全：点赞与收藏（三组开关）** —— 新增 `recordFavours(recordId)`（点赞名单）、
  `favourRecord(recordId, like=True)`（记录赞/取消）、`favourActivity(summaryId, like=True)`
  （活动总结赞/取消）、`collectActivity(eventId, collect=True)`（活动收藏/取消）；
  CLI 新增 `like` / `activity-like` / `activity-collect`——默认只预览、`--yes` 才写、
  写后回读回执。
- **同族漏检清单补齐（+5 读口）** ——
  - `messages(offset, limit)` 消息列表（分页键是**裸 `offset`/`limit`**）；
  - `dynamicMessages(offset, limit)` 动态消息（分页键是 **`pageRowBounds`**——
    系统内三套分页键并存，不能互相套用）；
  - `checkRecordExist(recordType, gradeAliasId)` 编辑页查重/回填；
  - `receivedComments(userId=None, offset, limit)` / `receivedFavours(...)`
    个人主页「收到的评论 / 赞」（行内 `userInfo` 已白名单收敛）。
- **端点覆盖审计 `TestCases/ApiCoverageAudit.py`** —— bundle 端点清单 vs 实时扫描
  `tools/` 得到的封装集，输出「同族缺口」报告（某段已有封装却仍有未覆盖的兄弟端点）；
  支持 `--segment <段>` / `--out diff.json` / `--inventory <清单>`；
  已登记进契约的 18 个 CLI 条目参与 `-h` 冒烟。

#### 实验

- **`TestCases/AiProxyTest.py`（已于 v1.2 移除）** —— AI 网关本地流式代理原型
  （Flask/SSE 转发）。属一次性实验，冻结为孤儿脚本后删除，不入包、不进 CI。
- **AGENTS「兄弟清扫」纪律** —— 从某个 chunk 建模块时，必须把该 chunk 内全部
  `"/xxx"` 路径字面量列出来逐条分诊（封装 / 留档 / 排除），再用覆盖审计复跑。
  教训直接来自本区间：评论四口取了，同 chunk 的 `favour`/`collect` 就被挑剩了。
  配套在 MEMORY 留了「点赞漏检」复盘。

#### 文档

- CHANGELOG 本段即 v1.1 之后累计变更的对外汇总；MEMORY 同步复盘记录；
  AGENTS 结构清单补 `ApiCoverageAudit.py` 一项说明。

---

### v1.1 — 评论 / 总结 / 应用中心工具化

自 v1.0 以来首次功能升级。**纯增量、无破坏性变更**：新增三个业务域与两个测试设施，
把「填写所有活动总结」从一次性脚本升级为正式工具，并收口若干实测发现的坑。

#### 新增

- **评论互动域**（`tools/RecordCenter/RecordComment.py`，含 CLI）——写实记录与活动课程
  总结的评论查看 / 发布 / 删除、点赞名单；评论列表内嵌在记录详情 `recordComment` 字段。
  评论对象内嵌的完整 `userInfo`（含身份证/考号）已白名单收敛。
- **成长报告自我总结**（`tools/GrowReport/GrowComment.py`，含 CLI）——学生端评语的读取与
  覆盖写入（userType=01，800 字上限）。⚠️ 写入受 `studentEnd` 窗口强制（过期返回
  「学生总结已截止」），与「活动总结逾期不拦截」相反。
- **总结提交工具化**（`tools/EvaluateActivity/`）——`SubmitSummary.py`（单条 / `--plan`
  批量 / 失败清单续跑，`--yes` 才写、回执逐字核对）+ `AutoDraft.py`（按活动类型出草稿、
  扫描任务生成计划；只读）+ `SummaryWrite` 域方法。招牌用例「填写所有活动总结」
  从一次性脚本升级为正式工具。
- **应用中心读侧**（`tools/AppsCenter/`）——积分（排名/流水/勋章/兑换信息）、问卷
  （任务/题目/历史作答，`templateId` 实测打通）+ 只读 CLI `AppsQuery.py`；
  按校配置，未配置时逐项降级不崩。
- **图书查询** —— `historyBooks()` 历史图书列表；`book(isbn)` 按 ISBN 查书详情
  （自动清洗格式，只收 10/13 位纯数字）。
- **公告已读上报** —— `markAnnouncementRead(objId)`，与公告列表接口配对。
- **会话卫生** —— `IQClient.logout()` 主动注销 token，缩小凭据存活窗口。
- **写路径演练**（`TestCases/TestWriteRehearsal.py`）——评论 / 活动评论 / 自我总结
  （快照-恢复）/ 发布+删除 四组自清理用例，零残留；批量写操作前先跑它证明渠道通畅。

#### 修复

- **评论响应 PII 收敛**——`/record/comment` 响应与评论列表内嵌 51 字段 userInfo，
  首次实跑被 CLI 直出；已改为白名单收敛 + 打印只出 id（与 `queryRecord` 同纪律）。
- `Feedback/SendFeedback.py`、`Export/ExportXlsx.py` 补 `Log` 导入——漏导入只在主流程
  NameError，`-h` 冒烟覆盖不到；`TestContract` 新增「Log 导入完备性」检查兜住这一类。
- 工单模板「发现时间」不再写死 2026-10-05，缺省 = 当天。
- `tasks()` 文档修正 status 语义（**1=逾期未完成 / 2=已办**），并固化实测结论
  「逾期总结服务端不拦截」。
- 只读回归套件 47 → **52 项**（新增 book/get、积分/问卷/评论探针），
  跨文档计数同步（SKILL / AGENTS / api.md）。

---

### v1.0 — 首个可用版

从 `v0.1-beta2` 直接转正，不经 `v0.1.0`。

#### ⚠️ 破坏性变更（升级必读）

**1. 删除了遴选/投票域**（`tools/Selection/` 整模块，5 个文件）

原能力：修改他人的遴选结果、代替发起人强制确认。**这类写操作会改动他人数据，
属于越权代操作**，因此整块删除而非加开关。调用方若依赖
`SelectionQuery` / `SelectionVote`，升级后该能力不再存在。

**2. 删除了人员枚举能力**（`searchPeople()` / `findPeople()`）

原能力：在全校范围枚举他人（实测可跨关键字去重出数万人，含身份字段）。
**不留 env 变量旁路** —— 留一个开关等于「藏起来但没关掉」，反而诱导绕过。
需要拿某人 `userId` 时改用 `records(type_="2")`（班级 feed，UI 本来就有的范围）
或 `records(type_="1", userName=…)`。

搜索域现在只剩「搜记录」，且命中项的 `userInf` 默认脱敏。

#### 新增

- **`IQClient.summary()`** —— 登录后一次性聚合 19 个字段的账号摘要
  （姓名/性别/生日/民族/籍贯/学号/学校/年级/班级/班主任/意向专业/
  艺术爱好/体育爱好/待办/逾期/已完成/未读/本人写实记录/本人成长报告/累计活动时长）。
  之前这些字段跨 5 个端点、且「累计活动时长」要逐份展开成长报告求和，
  每个使用者都得自己重新推一遍来源。默认即全量。
  命令行：`python tools/IqClient.py <ssoToken>` 直接打印全量摘要。

- **DEBUG 日志铺满业务层** —— 传输层之外，每个 mixin 记录传输层看不到的
  业务语义（命中条数、解析结果、脱敏、落盘路径、退出分支）。
  打开方式：`IQ_VERBOSE=1` 或 CLI `--verbose`。
  日志走 stderr、默认 WARNING 阈值，用户看 stdout 不受污染。

#### 修复

- **响应信封兼容**（D17）—— 少数端点返回 `{meta:{code,msg}}`，顶层没有 `code`。
  旧实现会把失败当成功。实测撞到过：家长评语提交实际被拒
  （`meta.msg=学生总结已截止`，逾期 22 天），代码却以为成功。
  已抽出统一的 `unwrapEnvelope()`，7 种信封都能正确解析。

- **验证码识别**（D18）—— OCR 从多变体投票 + 数字→形近字母映射，
  离线 48 张逐字真值 33/48 → 43/48；**服务端实测 15 轮真实登录
  12/15 = 80%**，同一样本上旧逻辑仅 6/12 = 50%。

- **三处日志计数与真实返回对不上** —— `semesters` 因信封键名取错恒打「0 个学期」，
  `interests` 因把 list 当 dict 恒打「0 键」，`records()` 因信封是两层
  `{"list":{"count":N,"list":[行]}}` 而少剥一层、此前一行日志都没打。

#### 安全

- **客户端闸门加到两处「服务端比前端宽松」的范围扩大**（D19）
  · `records(type_=)` 只放行前端 4 个 tab（`1`我的/`2`班级/`3`学校/`4`年段），
    非法值抛错且请求不发出，旁路须显式 `unsafeScope=True` 并留 WARNING
  · `queryRecord(id)` 比对 `userInf.userId` 与登录者，不符即拒，
    旁路须 `allowOther=True` 并留 WARNING
  · `userInf` 默认从 51 字段收敛到 10 字段白名单

  ⚠️ **闸门只防误用，不构成安全控制** —— 绕过本工具直接发 HTTP 请求仍可获得全量数据。
  真正的修复必须在服务端。

- **合规红线进 CI** —— `TestContract.py` 新增「能力红线」项，每次 CI 验证：
  搜人入口与授权开关不许复活、非法范围参数必须被客户端拦住、身份字段默认脱敏。
  该项带**反向用例**（移除白名单 → FAIL、移除归属校验 → FAIL、关闭脱敏 → FAIL），
  恒 PASS 的检查等于装饰品。

- **文档撤下越权端点载荷** —— 能力已删，文档不该留操作手册。
  端点细节与厂商构件编号移到 `reference/api-privileged.md`（gitignored，不进包）。

#### 已知限制

- 两处检索接口漏洞已作为通报 `RISK-2026-1006-01` 递交学校信息技术中心，
  **服务端修复前风险不变**，客户端闸门是唯一屏障。
- `/apps/integral/rank/integralRecord/account_integral` 返回
  `code=1 找不到对应的积分配置`（学校侧未开通，接口本身可达）——只读回归里唯一的 WARN。
- 验证码 OCR 线上通过率约 80%，不是 100%。有读图能力的 agent 建议走
  `VisionLogin.py`（实测 30/30）。

---

### v0.1-beta2

- 发布自动化：`PackSkill.py` + `release.yml`，Release 自动挂根目录 zip
- 首个 pre-release `v0.1-beta1`（53 文件 / 133.3 KB）

### v0.1-beta1

- 首个可发布版本：登录、写实记录读写删、22 类表单测绘、彩色 xlsx 导出、
  离线 CI 双平台矩阵

---

## 开发记忆（原 MEMORY.md，并入）

本文件是**跨会话记忆与决策日志**，记录开发过程、验证结论、外部情报与已知缺陷。

- 不属于 SKILL 入口，用户不会读到；`SKILL.md` 不引用它。
- 只存**结论与教训**，不存原始证据。原始邮件、chunk、日志留在本地临时目录，不入库。
- 写入前必须过 `tools/TestCases/TestContract.py` 的隐私闸门：禁 32 位 hex（token/recordId）、手机号、真实图片地址、硬编码密码、中文姓名示例。
- 涉及他校/他人数据一律脱敏或剔除，本文件不含任何真实学生姓名。

---

### 一、项目时间线

| 阶段 | 内容 | 提交 |
| --- | --- | --- |
| 起点 | 用户要求发布一条活动日志并抓取全站 22 类写实记录结构 | — |
| 发布工具 | `PublishActivity.py`：配文、本地图片上传、发布/编辑、`--dry-run`、`--yes`、三口径回执校验 | `22f6919` |
| 结构测绘 | `reference/frontend.md` + `reference/recordForms.json`，22 类槽位/字段/必填项 | `a814d34` `aacb009` |
| 登录修复 | `VisionLogin.py` argparse `%T` help 崩溃 | `27076c3` |
| 删除能力 | 发现 `/record/delRecord`；`DeleteRecord.py` + `RecordWrite.deleteRecord()`；真实发→删闭环 | `6d5aa14` `fe61bd4` |
| 离线 CI | Ubuntu + Windows 双平台矩阵，13 项契约检查 | `dae225f` `7ae110e` `e79be23` `10963d0` |
| 发版自动化 | `tools/Release/PackSkill.py` + `.github/workflows/release.yml`，Release 自动挂根目录 zip | `5adeb35` |
| 首个 pre-release | `v0.1-beta1`（tag `fc75ef3`），53 文件 / 133.3 KB，附件校验通过 | — |
| SearchCenter | `/search/search` + `searchRecords` + `records(userName=)`（搜人能力已于 2026-10-06 删除） | `7e49632` |
| 辅助模块 | `tools/Common/` 彩色日志 + `tools/Feedback/` 反馈工单 | `362b262` |
| 口径更正 | `type` 语义、人口数、schId/租户边界（本文件第六节） | 见 git log |
| 正确性 | D17 信封兼容、D18 OCR 投票、Logcat 部署（`d13814d`） | 见 git log |
| 合规分层 | 人员枚举默认关闭 + 记录搜索默认脱敏（D10），受限文档移出仓库（D14） | 见 git log |
| 会话沉淀（10-24/25） | 评论/自我总结/总结提交三域 + AppsCenter 读侧 + 写路径演练常驻化；只读套件扩至 52 项 | 见 git log |

#### 能力分层（2026-10-06 定的合规基线）

| 层 | 内容 | 约束 |
|---|---|---|
| Tier 1 | 本人档案、任务、记录读写、荣誉、报告、导出、`searchRecords` | 默认可用 |
| Tier 2 | ~~`searchPeople` / `findPeople`（可在全校范围枚举他人）~~ | **已整体删除**（2026-10-06）：不封装、不测试、不文档化，连授权开关都没留 |
| Tier 3 | D14 越权端点、人员枚举实测规模、厂商 chunk/moduleId | 记在 `reference/api-privileged.md`，**gitignored、不进包** |

- **为什么 Tier 2 从「默认拒绝 + 强制留痕」升级为「整体删除」**：留 env 变量旁路
  等于「藏起来但没关掉」，反而诱导绕过；对未成年人个人信息的暴露面，
  「自觉填授权来源」不构成有效控制。正当需求（拿某人 userId）走
  `records(type_="2")` 班级 feed 或 `records(type_="1", userName=…)` 即可。
  代价是失去 D3/D12 那两条已知限制的适用对象（都随能力一起消失）。
- `TestContract.py` 第 15 项每次 CI 都验这条红线：门面与模块都搜不到任何搜人入口，
  授权开关（`enablePeopleSearch`/`peopleSearchReason`/`IQ_ALLOW_PEOPLE_SEARCH`）
  也不许复活——否则一次无害重构就能悄悄把能力加回来，且没有任何测试会红。
- **客户端闸门（2026-10-06，针对服务端比前端宽松的两处）**：`records(type_=)` 只放行前端
  4 个 tab（`1/2/3/4`），非法值抛错不发请求，旁路须 `unsafeScope=True`；
  `queryRecord(id)` 比对 `userInf.userId` 与登录者，不符即拒，旁路须 `allowOther=True`；
  两者旁路都打 WARNING 留痕，且 `userInf` 默认脱敏到 10 字段白名单。
  ⚠️ **闸门只防误用，不是安全控制**——绕过本模块直接发 HTTP 一样拿全量数据，
  所以真正的修复要在服务端。

#### 4.1 递交状态（2026-10-06 起）

**两处检索接口漏洞已递交学校信息技术中心**，通报编号 `RISK-2026-1006-01`：

| 处| 通报章节 | 服务端端点 | 本仓库对应缺陷 |
|---|---|---|---|
| 搜索 | 问题一 | `GET /search/search` `type=2` 未按角色限制 | D2 / D10 / D11（工具侧已删能力、默认脱敏） |
| 查询写实记录 | 问题二 | `POST /record/queryRecordList` 非法 `type` 走无过滤兜底分支；`POST /record/queryRecord` 不校验归属 | D19 |

- 学校侧**预计 2026-10-13（下周）起可见并进入处置流程**。在那之前服务端未修复，
  **风险不变**，客户端闸门继续是唯一屏障。
- 自建 feedback 站的工单（`rEGwKxCIz…` / `EMflgkmw2B…`）是**我方留痕**，不是学校已受理的凭据——
  学校与平台方不会自动收到。两件事都别混为一谈。
- ⚠️ 递交后到修复前这段时间，**对外一律说「已上报、待平台修复」**，
  不要说「已提交修复」或「已受理」。

**当前 `main` 见 `git log -1`（本文件不写死 hash——写死必过期，已过期过两次）。**

---

### 二、能力验证矩阵

#### 已实测确认

| 能力 | 状态 | 证据 |
| --- | --- | --- |
| 学生 token 登录、用户档案 | 通过 | 多轮 |
| 22 类记录读取与槽位还原 | 通过 | rt 0/1/5/6/7/17 与真实记录逐字段核对 |
| 活动日志发布/编辑 | 通过 | 正式记录留存至今 |
| 荣誉发布 | **通过** | 修掉封装层漏传 `itemName` 后，发→读回→删 `16→17→16` |
| `honorTypes()` 作为 typeId 来源 | 通过 | 6 个类型；注意返回项字段是 `eventConfigId`/`title`/`levelInfo`（原始 dict） |
| 写实记录删除 | 通过 | 15→16→15、278→279→278，删后查不到 |
| 学校开通类型 | 已确定 | `get_sch_feature` 返回 12 类：`0,1,2,3,4,5,6,7,14,15,16,17` |
| 本轮补测 rt 2/3/4/14/15/16 | **6/6 通过** | 见下节 |
| `delSummary` 存在性 | 端点存在 | 正确参数 `summaryId`；对不存在 id 也返回 `code=0`（危险） |

#### 未验证 / 无样本

- 图片 URL 复用：需用**他人** fs 地址，本校 feed 前 30 行全被本人最新记录占满，取不到样本。**未验证。**
- 其余 10 类记录提交：学校未开通，提交失败无法区分「载荷错」与「未开通」，**无验证信号**。
- macOS：用户明确要求不测。

---

### 三、本轮实测的四条服务端契约

补测 6 类时，第一轮全部 `999999 发布失败`，逐一定位后第二轮 6/6 成功。教训值得长期记住：

1. **服务端严格拒绝未知字段。** 我给 form 多塞了组件里不存在的 `desc`，全部被拒；删掉多余字段立刻全通。构造载荷必须与前端组件字面量 1:1。
2. **`code` 能区分失败原因。**
   - `999999` = 载荷/业务失败（字段错、槽位 key 错、未开通）
   - `1` = 缺必填参数，且**会带明文原因**（如「荣誉名称不能为空」「ISBN不能为空」「学生ID不能为空」）
   - `0` = 成功，但**不代表有可见效果**（如 `delSummary` 对不存在 id 也返回 0）
3. **rt 2 需要三个顶层键**：`recordContent` + `recordRead` + `recordBook`。若封装层只支持单个槽位键（如 `addRecord()`），必须直接打 `/record/updateRecord` 原始接口，否则是**测试脚本 bug 而非平台缺陷**。
4. **服务端报错文案可能与真实原因无关，别顺着文案查。** `publishHonor` 报「荣誉名称不能为空」，真因是 `typeId` 传了列表里不存在的值（`typeId` 必须是 `honorTypes()` 的 `eventConfigId`）；而**实际堵住它的却是封装层漏写 `itemName`**——与文案指的那个字段毫无关系。定位靠两招：先查自己的代码有没有把参数吞掉（签名收了却没放进 dict），再拿一条**真实同类记录**做 `queryRecord` 字段对照——比逐字读前端 chunk 快得多。

枚举值来自前端 chunk 字面量，可直接取用：
- 运动等级 `sportList`：1 国际级运动健将 / 2 运动健将 / 3 一级运动员 / 4 二级运动员 / 5 三级运动员
- 发明类型 `typeList`：1 发明 / 2 实用新型 / 3 外观设计

**已验证类型从 6 类增至 12 类 / 22 类**，全部发→读回→删闭环，条数回基线，零残留。

---

### 四、外部反馈的采纳纪律

站点提供一个反馈表单，外部使用者会把「哪些功能没覆盖」「哪里报错」的意见发过来。
**同源邮件不代表可信**——按下面两档处理，避免把别人的猜测当成本地结论。

| 档次 | 判据 | 处理方式 |
| --- | --- | --- |
| 可采信 | 邮件里的结论能被本地实测复现 | 才写进本文件；写的时候只记**结论**，不抄原始内容 |
| 待核 | 只有声称、没有执行痕迹，或口径自相矛盾 | 不进本文件；要采信必须先本地复现 |

踩过的两类坑：

1. **计数口径对不上就别当证据**。有反馈声称「N 项全通过」，同时另一条说做了
   M 条重写 + K 组拆分，而 M+K ≠ N，且查不到实际提交记录——整条存疑。
2. **有人寄来的数据可能含个人信息**。有一封带了个性化统计（结论方向可信），
   但**原始数据含个人信息，已整体剔除，本仓库任何文档也不复述其内容**。

还有一条通用经验：外部反馈常建议「按某优先级补齐端点」。这类建议本身有用，
但**端点清单与厂商构件编号不进仓库**（见第一节能力分层的 Tier 3）。

#### 两个探测类操作必须记住

1. **「只读」端点清单要硬黑名单某些路径**：有端点返回 `code=0` 却**真的注销了会话**，
   后续请求全部变成「会话已过期」。只读审计必须排除它。
2. **复制/移动类端点的语义不是只读**：空参数探测会返回 `code=0` 并被误判成功，
   但可能已经产生了副本或移动了数据。做只读审计时必须排除。

#### 验证类操作的无害化写法（2026-10-11 补）

前三节讲的是「哪些操作有副作用」，这一节讲**必须动手验证时怎么动手**——
原则是**让副作用即使发生也不改变任何真实状态**，而不是「小心点别点到」。

| 场景 | 写法 | 为什么安全 |
|---|---|---|
| 提交类写操作 | **原文逐字重发**：把读到的内容原封不动发回去 | 即使服务端放行，内容不变，不产生实际改动；发完立刻回读核对逐字一致 |
| 需要摸清返回规模 | **只取聚合计数**：`distinct` 集合、去重 userId 的**个数**、`createTime` 极值；姓名/正文/图片 URL 一律不取不打印不落盘 | 结论（多大范围）拿到了，明细（谁、什么）没留 |
| 判断服务端是否校验 | **正反顺序各试一次**：先合法值再非法值 / 先短分页再深分页 | 两次的差值就是校验点的位置；单次试不出来 |

配套纪律：**研究性取证也要最小留存**。`%TEMP%` 下的全量快照
（如「把个人综评各域各 dump 一份」）在分析完成后应立刻删——
留着就是一份等着被误提交的个人信息合集。

---

### 五、已知缺陷与待办

| 编号 | 问题 | 状态 |
| --- | --- | --- |
| D1 | ~~`publishHonor()` 荣誉名称字段层级错~~ **已修（`itemName` 从未被写进 form，封装层吞字段）** | 已发→读回→删闭环，`16→17→16` |
| D2 | `searchRecords()` 返回 `idNumber` 等敏感字段且未脱敏 | 待修（调用方自行处理） |
| D3 | ~~`findPeople()` limit=50 会截断~~ | **随能力删除而失效**（2026-10-06） |
| D4 | 文档端点计数与实测脱节 | **部分已同步**：`api.md` 已加「count 会漂，别当断言用」的警示；`TestApiReadOnly` 现为 **52 项（PASS 51 / WARN 1）**，加 `--upload` 变 53 项 |
| D5 | `delSummary` 对不存在 id 也返回 `code=0`，无异常保护 | 高危，需二次确认 |
| D6 | 登录链路遇瞬时网络异常会漏栈而非按退出码契约退出 | 待修 |
| D7 | release workflow 用插值方式把 tag 拼进 shell 命令，存在注入面 | **已修（`fa5e7be`）**：五处 tag 全改 `env:` 传递，YAML 已复检 |
| D8 | `release: published` 触发时用的是 **tag 上的旧 workflow 定义**，`workflow_dispatch` 路径已用新定义验证过，自动路径未验证 | 需下一个 release 才能验证 |
| D9 | SearchCenter 提交后 CI 未复查 | **已复查**：CI #8（`7e49632`）曾因 TestContract 隐私闸门失败（双平台红），`9256f53` 修复后 CI #9 转绿 |
| D10 | ~~`searchRecords()` 无 `redact` 开关，每条命中项内嵌 `userInf`（51 字段）含身份标识/照片~~ | **已修（2026-10-06）**：`redact=True` 成为**默认**，命中项 `userInf` 收敛到 `PERSON_KEEP` 白名单；`redact=False` 才给原始返回并打 WARNING。已由 TestContract 新增「能力闸门」项离线守着 |
| D11 | ~~`searchPeople(redact=False)` 原始返回含他人隐私信息，且脱敏是客户端丢弃——服务端照发~~ | **已随能力删除而消解（工具侧，2026-10-06）**：工具不再封装搜人；**服务端缺陷本身未修**，已作为通报 `RISK-2026-1006-01` 问题一递交学校（预计 2026-10-13 起进入处置流程，见 §4.1）。风险不变 |
| D12 | ~~`findPeople(exact=True)` 砍不掉完全同名账号~~ | **随能力删除而失效**；结论保留：**认人只能靠 `userId`**，姓名不是主键 |
| D13 | `searchRecords("")` 抛 999997，但 `"   "`（纯空格）返回 1729 条——空串与空格行为不一致 | 已知限制：别拿空白串当有效关键词 |
| D14 | 教师端学分名册端点（**路径见私有工单**，已移出本文件）——**学生 token 可读**，返回全校 `studentName` + `idNumber` + `className` | **已上报（2026-10-06）**：security 工单已投递 feedback（id `rEGwKxCIz…`）。跨角色越权 + 未成年人敏感个人信息，**服务端未修前风险不变**。端点细节已移出本文件到 `reference/api-privileged.md`（gitignored，不进包） |
| D15 | 部分配置/导出端点接受客户端传入的 `schId`（`/apps/assess/scheme/list_semester` 实测 `200`→21 条 / `999999`→0 条，无兜底校验） | **待平台方验证**：需真实外校 `schId` 才能确认可利用性，本地单校数据无法判定 |
| D16 | `/studentMgr/export`、`/teacherMgr/export` 把 `session` 放进 URL query | 待评估：凭据走 URL 的泄露面（日志/Referer） |
| D17 | ~~`HttpTransport._call` 只检查顶层 `code`~~，部分端点信封是 `{meta:{code,msg}}` → 错误码被吞、返回 `null` | **已修**：拆出纯函数 `unwrapEnvelope(out, path)`，`meta` 是 dict 且含 `code` 时以它为准；`TestContract` 新增第 14 项离线守着（7 种信封），已验证旧实现下该项 FAIL。撞到它的现场：家长评语提交实际被拒（`meta.msg=学生总结已截止`，逾期 22 天），代码却以为成功。**遗留：无**。2026-10-05 靠 `IQ_VERBOSE=1` 的全量日志枚举出 6 个 `{meta:…}` 端点（家长评语提交 + `/user/getUserInfoDetail` `/studentMgr/getParentList` `/announcement/listAnnouncementRead` `/eventTwo/listActivityStatisticsByDimension` `/growReport/summary/listGrowReportStuByStudentId`），另34 个是顶层 `code` 型；清单见 `reference/api.md`。线上回归无回归：`TestApiReadOnly` 47 项 PASS 46 / WARN 1 / FAIL 0、`TestRecordRead` 13/13 |
| D18 | ~~`ocrCaptcha` 逻辑 bug：`texts[0]` 恒为预处理图结果，原图识别被丢弃~~ | **已修（离线实测）**：改 3 个全画布阈值化变体投票（170×3 / 180×4 / 200×4）+ `DIGIT2LETTER` 数字映射。48 张逐字真值（输入用文件路径，与生产同路径）**43/48 ≈ 90%**，A 批 21/24、B 批 22/24；旧实现同条件 33/48 ≈ 69%，历史上服务端实测 42/70 = 60%。**服务端实测（2026-10-06，15 轮真实登录）：12/15 = 80%**，同一样本上旧逻辑只对 6/12 = 50% —— 离线 90% 比服务端保守 10 个点，**对外只报服务端数字**。**两个反直觉结论**：①「裁剪归一化」变体只有 7/24，混进投票会把强变体带跑；②变体文件名曾互相覆盖（默认 out 都是 `.prep.png`），投票等于单变体 |
| D19 | `queryRecord(id)` **不校验记录归属**（只按 id 返回），且 `userInf` 原始 51 字段含身份证号/考号/政治面貌/住址/照片；`queryRecordList` 的非法 `type`（空串即可）走**无过滤兜底分支**返回 146,021 条（**与「学校」tab 同一数据集**，倍数 1.00，见 6.7）；且列表行内**无 `userInf`**，故列表本身不返回身份字段，风险落在 `queryRecord` 这一跳 | **已递交学校**（通报 `RISK-2026-1006-01` 问题二，预计 2026-10-13 起进入处置流程，见 §4.1）+ **客户端已加两道闸门**：`records` 只放行前端 4 个 tab（其余抛错，旁路要 `unsafeScope=True` 留 WARNING）、`queryRecord` 比对 `userInf.userId` 不符即拒（旁路要 `allowOther=True`）+ 默认脱敏。**闸门只防误用不是安全控制**——绕过本模块直接发 HTTP 一样拿全量。**服务端未修前风险不变** | 

---

### 六、schId 与租户边界（2026-10-05 实测，本节结论推翻过三次才对）

#### 6.1 平台形态：每校独立部署的多租户

- `schId` 是租户标识，由 `loginBySSOToken` 依据 `ssoToken` 决定后返回（`schoolId:"200"`）。
- **数据查询类端点的请求里不含任何学校标识**，租户完全由 `AccessToken` 请求头决定：
  - `/search/search` —— 前端全站仅 1 处调用，参数只有 `type` / `content` / `pageRowBounds`
  - `/record/queryRecordList` 与教师端学分名册端点（D14）—— 同样不传
- 实测所有返回的学校标识**恒为同一部署**：多种检索路径与一份跨部署名册的样本都只有
  一个学校值（取样规模与方法见私有文档）。
- **结论：数据查询类端点不存在跨校读取路径**（因为根本没有学校参数可传）。

#### 6.2 `schId` 作为客户端参数只出现在配置/导出类端点

前端 `localStorage.get("schoolId")` 共 20 处，**只有 6 处真正进请求**：

| 端点 | 传法 |
|---|---|
| `/studentMgr/export` | POST body（另带 URL 内 `session`） |
| `/teacherMgr/export` | URL query |
| `/ctc/criticism/export` | URL query |
| `/apps/club/evaluate/listTemplate` | GET data |
| `/apps/integral/scheme/integralAppraisalScheme/*` | POST body |
| `/cqesBank/scheme/confirm` | POST body（写） |

其余 14 处是本地判断，如 `["1","3","50"].includes(schoolId)` 做功能开关（**说明各校配置不同**）。

#### 6.3 学校切换器：已定性（2026-10-05 复查，**推翻本节原「未定性」结论**）

`chunk-7961fa63` 的 `schoolChange` 真实实现：

```js
schoolChange(l){ this.$http.post("/account/switch", {data:{schId:l}}).then(l=>{
    this.$localStorage.clear();                                   // 清空本地态
    "0"!==String(l.data.code) ? 登录失败提示 : this.toHomeView(l.data); // 成功后整页重载
})}
```

- **结论：切换学校 = 后端重新签发身份 + 清 localStorage + 重载**，
  **不是**「仅改前端查询条件」。因此「数据查询端点不校验 schId」是**设计（必然行为），
  不是缺陷**——原 6.3 那一节的疑问到此关闭。
- `schools` 来自 `localStorage.switchStr`（`{school:[{schId, schName}]}`），
  `isMultiSchool = schools.length > 0`——**学校列表由后端在登录态里下发**，
  前端不自带任何学校常量。
- ⚠️ 该组件是 `teacher-user-bar`，`toHomeView` 跳 `/#/teacher/index`，
  `userType` 判断只覆盖 `02/03/04`。**学校切换器是教师端功能，学生端没有这条 UI 路径。**
- `/account/switch` 对**学生 token 也存在**（用不存在的 `999999` 探测 → `code=1 登录失败`，
  探测后 session 仍可用、非破坏）。但它是**写端点、会换身份**，
  本仓库**不封装**，也不得用真实 schId 调用（那是跨租户访问尝试）。

#### 6.4 跨租户边界的实测结论（探测过程见私有文档）

向数据查询端点的 payload 里塞学校标识做有效性探测，结果：**对结果零影响**，
租户完全由 `AccessToken` 请求头决定。三条结论：

1. **数据查询面没有跨校读取路径**——请求里根本没有能参与过滤的学校参数。
2. 传非数字类型的学校标识会报参数校验失败，说明后端**认识这个字段并校验类型，
   却不取值参与过滤**——比「完全不读」更能说明它是死参数。
3. 命中项里的学校标识可用于单租户断言（本部署恒为一个值）。

⚠️ **探测手法与完整证据表在 `reference/api-privileged.md`**（gitignored、不进包）。
留在这里的是结论与纪律，方法不留。

#### 6.5 由此产生的纪律

- **不要用真实存在的其他学校标识做验证**——那是跨租户访问尝试。
  只用不存在的值做有效性探测。
- 本仓库只覆盖单一部署，任何「跨校」结论都必须由平台方自查，不能由我们断言。

#### 6.6 同批修正的错误口径（都已作废）

| 曾经的错误表述 | 实际 |
|---|---|
| `type=""` 是「全平台 / 含外校」 | 后端**兜底分支**，前端无对应 tab，不做范围过滤 |
| `type="2"` 是「本校可见」 | 前端 tab 名是「**班级**」 |
| 人口 34,624 | **28,196**（`searchPeople` 是子串匹配，把各姓 `totalResult` 相交会重复计数） |
| 「14.6 万条是跨校数据」 | 全部 `schId=200`；把「作者数 14,005」误当成人口是错的根源 |
| 兜底分支比「学校」tab **宽 12 倍** | **同一数据集**，倍数 1.00。根因是把 `4`=年段误当成学校、把 `3`=学校误当成非法值——同一条错误的两个版本（详见 6.7） |

**教训**：这几条错误都源于「拿接口参数名推断业务语义，而不去前端找 tab 定义」。
`type` 的四个取值在 `chunk-7c090c4c` 的 `modules` 数组里写得清清楚楚：
`[{id:"2",name:"班级"},{id:"4",name:"年段"},{id:"3",name:"学校"},{id:"1",name:"我的"}]`（默认 `type:"2"`）。

#### 6.7 `type=3` 归属实测定案（2026-10-06）

上面那条「宽 12 倍」的错误此前长期留在 `SKILL.md` 里。本次用同一 token 逐个探测
`limit=1`（不分页、不取内容），比对 `count` 与首条 `recordContent.id` 的 sha1：

| type | 前端 tab | count | 首条 id sha1 |
|---|---|---:|---|
| `1` | 我的 | 18 | `c4c068e1df70` |
| `2` | 班级（默认） | 281 | `c4c068e1df70` |
| `4` | 年段 | 12,139 | `c4c068e1df70` |
| `3` | 学校 | 146,021 | `3acc20305aec` |
| `0` / `abc` | *（无 tab）* | 146,021 | `3acc20305aec` |

**定案：**

1. `type=3` 是**学校** tab，不是兜底分支；
2. 非法值与 `type=3` **是同一数据集**——`count` 完全相等、倍数 **1.00**、首条 id 摘要一致；
3. 数字（`0`）与任意字符串（`abc`）都落进同一兜底分支，说明**不是解析失败兜底，而是压根缺 `type` 校验**（`code` 仍为 0）；
4. `type=4`=年段（12,139），印证 12,13x 才是年段、146,02x 才是学校。

**方法论补充**：`count` 会漂（10-05 的 146,020 → 10-06 的 146,021），**单看数字分不出分支归属**——
`SKILL.md` 旧表的 12,136 与实测 12,139 只差 3 条，两边都能自圆其说。
**判定分支归属必须比数据集身份（记录 id），不能比 count。**

---

### 七、环境与纪律

- 仓库（唯一活体）：本子树，随三站聚合仓 `mc-lhz/AutoXMYZ` 发布，会话/token 不入库
- 上游 `mc-lhz/591iqAutomatic` 已**归档冻结**（v1.2，只读，2026-11-08）：仅作历史参考，
  不再回同步；上述独立发版流程只对历史版本成立，当前走聚合仓统一 Release（AutoXMYZ.zip）
- 凭据、token、姓名、手机号、userId、真实记录 ID **一律不入库**；临时数据只放 `%TEMP%\591iq_scratch`。
- 写入类测试**必须按序逐条跑**，否则前后条数快照互相干扰。
- 只删本次会话创建的记录；既有记录清单用快照文件固化，删除前逐一比对。
- `reference/` 预算 **150 KB**（2026-10-05 由 100 KB 抬高，当时已用 97 KB／剩 3 KB，
  无法容纳本轮核验结论与新接口契约；2026-10-11 实测已用 **109.3 KB**），
  只存提炼结论，不存原始前端代码。
- 每业务一个目录、模块 PascalCase、入口 `main(argv) -> int`，CI 以 `--help` 零退出码作为导入自检。
- 完成改动**不自动 commit**，需显式要求。

---

### 八、验证方法论（2026-10-11 整理自 `%TEMP%\591iq_scratch` 的原型工作）

D18/D19 记的是「验出了什么」，这一节记「怎么验的」——后者才是能复用的部分。
原始脚本都在 `%TEMP%\591iq_scratch`（不入库），这里只留结论与教训。

#### 8.1 合规检查若恒 PASS 就是装饰品

**每加一条红线，必须配一条能证明它会红的破坏用例。** 否则「检查通过」只说明
它对当前这版代码成立，说明不了它在起作用。

`TestContract` 的「能力红线」项就是照这个标准建的几道破坏用例：
移除 `records` 白名单 → FAIL；移除 `queryRecord` 归属校验 → FAIL；
关闭 `userInf` 脱敏 → FAIL；还原 → PASS。**反向用例才是证据。**

自证粒度由轻到重，按成本选：

| 粒度 | 做法 | 适合 |
|---|---|---|
| 纯函数 | 正例/反例各几条，**含故意设计的阴性**（该命中的命中、不该命中的不命中） | 单条规则 |
| 进程内 monkeypatch | 同进程改掉被测函数，跑检查项看是否 FAIL，再还原 | 客户端闸门 |
| 真子进程 + 真文件 | 往被扫文件里追加违规内容 → 子进程跑检查 → 看 stdout 有 FAIL → `finally` 还原 | 提交前扫描类 |
| 端到端双用例 | 违规输入期望拦下 N 处 + 合规输入期望 0 处 | 外发闸门 |

**「该涂的没涂」和「不该涂的涂了」同等重要**：脱敏器过度涂改会毁掉可调试性，
所以断言里必须有几条要求**原样保留**（会话 id / token / userId）。

#### 8.2 基准要有真值、双批防过拟合、且由线上裁决

来自 D18 那条 OCR 链的三条通用规律：

1. **基准输入形态必须与生产调用完全一致**。同一个 OCR 库，传 PIL 对象和传文件
   路径结果不同；基准里用了哪种，生产就用哪种，两边数字才可比。
2. **调参批与验证批必须分批抓**（不同会话 + 不同时间窗）。只在调参批上选出的最优，
   到验证批通常掉几个点；而**掉点幅度**本身就是有没有过拟合的信号。
3. **离线准确率 ≠ 线上通过率**。D18 的离线 43/48 ≈ 90%，线上 12/15 = 80%。
   差值来自「所有变体同时失败」这种情况——**投票/集成方案有天花板，
   这个天花板必须单独度量，不能用离线数字代表线上**。
   所以对外一律只报服务端数字。
4. **长任务边跑边落盘**。全网格扫描跑到 35/112 组被掐断，落盘的 35 组仍然可用。

#### 8.3 `%TEMP%\591iq_scratch` 台账

该目录是原型工作台，**不入库、不打包**（AGENTS 已定）。2026-10-11 盘点：
550 文件 / 21 MB，其中约 14 MB 是与本项目无关的外部工作，两个目录可以直接清掉。

⚠️ **它自己通不过自己的闸门**——盘点发现下列文件含活跃凭据或个人信息：

| 文件 | 含什么 | 处置 |
|---|---|---|
| `full_info.json`（237 KB） | 会话凭据 + 明文身份证（多处）+ 考号 + 同班同学姓名 + 班主任手机号 + 三方评语 | **分析完即删**；真要留结论，只留三个统计块（约 0.5 KB），其余全是 PII |
| `article_dump.txt` | 明文身份证（2 处）+ 姓名 + 考号 | 用完即删 |
| `serverbench.log` / `.log.err` | 多次真实门户 `JSESSIONID` | 用完即删 |
| `vl_*.state.json` | 门户 `JSESSIONID` | 一次性，用完即删 |
| `probe*.py` / `tasks.py` / `verify.py` | 硬编码的会话凭据 | 一次性探针，随原型结束即删 |

**由此补一条流程**：现有的「对外材料发布前体检」只扫发布产物本身，
**应当扩到覆盖 `%TEMP%\591iq_scratch` 全目录**——
否则源码与临时产物成了一条绕过闸门的通路。

**原型工作台的纪律**（补 AGENTS「先原型化」那条的后半段）：
- 原型验证完，**有用的移入 `tools/` 并补同名 `.md`，无用的当场删**；
- 一个专题做完（提交 / 能力删除 / 材料生成）**盘点一次**，
  别让几十个探针永久堆积——它们既是噪声，也是上面那张凭据台账的来源；
- 一次性脚本不要迭代出 v2/v3/v4：能用一次说清的，结论直接进文档。

---

### 九、2026-10-24/25 会话沉淀（评论 / 总结 / 应用中心 / 工程事故）

#### 服务端契约（新增实测）

- **窗口策略不对称**：活动总结**逾期不拦截**（60 条逾期数月照收，`count_task.expired`
  随之下降）；成长报告自我总结**窗口强制**（过期 `code=1 学生总结已截止`）。
  跨写域类比前先看实测。
- **`task/list` status 语义定案**：`0`=待办 / `1`=逾期未完成 / `2`=已办，与
  `count_task` 的 unfinished/expired/finished 一一对应（旧文档「1=已完成」已作废）。
- **`delSummary`**：参数名是 `summaryId`（实测露出）；沿用 api.md 定性
  （对不存在对象也 code=0、不当探测口、对真实 id 真删）——**不封装**。
- **`/book/get`**：ISBN 只收 10/13 位纯数字（展示格式需清洗）；查无回
  `999999 该ISBN未查询到书籍`。
- **问卷读三件套**：必填 `templateId`（任务列表行 `id` 可直接当之）；
  `questions[]` 含 type/required/itemList；真实问卷（5 题）读全通过。
- **积分按校配置**：schId=200 未配置积分体系（`code=1 找不到对应的积分配置`）；
  `rank_type` 有 5 维度枚举；排行分页键是 **`pageRowBounds`**（offset/limit 会被拒）。
- **AI 网关**（10-24）：`/ai/dashscope` OpenAI 兼容、`/models` 180 个模型、
  function calling 闭环可用；`ZHIPU/*` 通道未激活（400 product not activated），
  无前缀 `glm-5.3` / `glm-5.3-prime` 可用；后端为自建多渠道聚合网关
  （Envoy 网格 + DashScope 协议指纹，非公网中转 SaaS）。
- **评论家族**：概述评论在记录详情 `recordComment` 内嵌；活动评论走
  `summaryId`；载荷 `{id, comment[, replyUserId]}`（详见 RecordComment.md）。

#### 工程事故与加固（都已修 + 有闸门）

- **Log 导入缺失**（`SendFeedback` / `ExportXlsx`）：后加的日志代码 + `-h` 冒烟
  只走到 argparse → 函数体 NameError 落在 CI 盲区。新增 `TestContract`
  「Log 导入完备性」检查（**含反向用例**）。
- **工单「发现时间」写死 2026-10-05** → 缺省 = 当天。
- **演练首跑残留事故**：记录定位查错字段——标题在**槽位对象** `.name`
  （`recordActivityFJ.name`），不在 `recordContent`；发布成功却定位不到、
  没删掉，残留 1 条（当场清）。教训：**任何「发布 + 回收」闭环，
  必须先用一轮演练验证定位逻辑，再上批量**。
- **写路径演练常驻化**：`TestCases/TestWriteRehearsal.py`（记录评论 / 活动评论 /
  自我总结快照恢复 / 发布+删除，全部自清理零残留）——批量写操作前先跑它。
- **只读套件扩容 52 项**：新增 book/get、integral rank_type、prize/list、
  queryComment、listSurveyTask 探针；跨文档计数（SKILL/AGENTS/api.md/md）同步。
- **评论响应内嵌完整 userInfo（含身份证/考号）**：`/record/comment` 响应与评论列表
  携带 51 字段 userInfo；首次实跑时被 CLI 直出（`ok` 误用 `and` 语义——
  `A and dict` 返回 dict 而非布尔，整个响应 dict 被当「回执一致」打印）。
  已修：`bool()` 断言 + `redactComment()` 白名单收敛（复用 `USERINF_KEEP`）+
  「打印/日志只给 id 与条数」规矩（RecordComment.md）。评论列表/活动评论返回同步收敛。
- **点赞功能漏检复盘**（2026-10-25）：`/record/favour`（22 chunk）与 `/record/comment`
  同处**记录卡片 chunk 家族**，但学生面闭包（20 seeds）对两者的命中率是 **0/22**——
  评论区能落地纯靠点名 + 定向 grep；建评论模块时也没做**兄弟清扫**，同 chunk 的
  `favour`/`collect` 被挑剩。已补：三组开关（记录赞/总结赞/活动收藏，实测幂等且零残留）+
  `TestCases/ApiCoverageAudit.py`（同族缺口可复跑）+ AGENTS「兄弟清扫」纪律。
  扩种子重跑闭包（44 chunk）另浮出**活动报名家族**：`/evaluateActivity/join`
  GET `{eventId, eventActivityRoleId}`（写，待单独评估）、`queryRoleInfo`（读，角色列表，
  前端过滤掉主持策划者/主要参与者）；`reviewDel`（GET {id} 删除，对象类型未知）与
  `/activity/summary/export_picture`（教师侧倾向）**留档不封装**。
  同类漏检清单已同修：`/record/checkRecordExist`（查重回填）、`/sm/comment` + `/sm/favour`
  （收到的评论/赞，行内 userInfo 已白名单收敛）、`/msg/queryList` + `/msg/queryDynamicList`
  （消息/动态列表——**两套分页键不一致**：裸 `offset/limit` vs `pageRowBounds`）。

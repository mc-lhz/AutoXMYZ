# CampusNet — 开发契约（xmyz.xmedu.cn）

本子树对应校内系统（Struts2，`模块!方法.action`）。路径相对 `references/CampusNet/`。

## 架构

```
tools/
  XMYZClient.py                  门面：组合各业务域 mixin（331 具名方法）
  endpoint_kind.py               端点读写分类（文档/统计口径，非运行时闸门）
  Access/HttpTransport.py        传输层：_call/get/post/destroy/paged/login/_bindUser
  Access/LoginSession.py         登录四式：password / jsessionid / vision / check
  StudentBase/ProfileDict.py     身份、字典、学期、班级、网络磁盘
  LifeOffice/StudyMessage.py     成绩、成绩单、成长记录、作业、短信、通知、附件、ScoreTrend
  QualityCenter/QualityRead.py   综合素质评价
  CommunityCenter/               社团与志愿服务（+ CommunityExtra/VolunteerNew）
  ElectiveCenter/                选课系统（课程/结果/活动记录/考勤）
  ScheduleCenter/                个人日程与分类消息
  PsychCenter/                   心理咨询预约
  WorkCardCenter/                作业打卡
  VoteCenter/                    投票
  EvaluationCenter/              教师评测 + 校本课程评测
  ExamCenter/                    会考练习（信息技术会考）与在线考试
  SelectSubjectCenter/           选科 3+1+2
  StudentCenter/                 学生向零引用端点收口
  Build/                         端点建库流水线（登录→抓模块→合并→探测→生成文档）
  TestCases/                     TestContract(9) / TestApiReadOnly(35) / TestMethodSmoke
```

- `reference/api.md` — 端点清单（唯一参考文档；Build/gen_api_md.py 生成）
- 每个 `.py` 有同名 `.md`（`XMYZClient.py` 豁免）；每个业务目录有 `__init__.py`

## 红线（能力政策 2026-10-24 修订）

- **读写均放行**；`endpoint_kind.kind()` 只作文档口径。`TestContract` 的
  `policy_no_guard` 反向用例防止旧 `_guard` 被加回。
- **写纪律**：只写本人数据、可逆优先（create→verify→destroy）、
  不封装 `resetPassword`、不碰他人审批流；服务端账号权限是最终边界。
- `_call` 是唯一出口；分类判定只有一份（`endpoint_kind.py`），
  任何地方不得维护第二套名单（`merge_endpoints.py` 曾违规，已废除）。

## 开发契约

- 命名：目录/文件/类大驼峰、方法小驼峰、常量 UPPER_SNAKE；文件名不得重复目录名；
  目录名禁止与标准库同名
- 新增业务域 = 新目录 + `__init__.py` + mixin + 同名 md + 门面注册
- 日志：结论 `print` 走 stdout；内部诊断 `from Common.Logcat import Log` 走 stderr
- `Http` 必须留在 `XMYZClient` 继承链末位
- 对外 API 只增不改；改方法名同步门面/测试/SUBSKILL/api.md
- 新功能先在临时目录原型化；一次性探针用完即删
- **发现/新增功能域立即建域**（目录+mixin+md+门面），不要用「泛化调用能跑」当借口

## 已踩过的坑（改代码前先读）

1. `loggedIn` 不能判会话（登录后字段消失；判据是 profile 有 `loginName`/`id`）
2. 无参构造必须自己读会话文件（曾静默以未登录身份运行，「测试全绿」假象）
3. 端点分类不能靠正则硬拼（`approve` 断词漏判 88 个写端点）
4. 只读探测不能只认信封（裸数组/裸对象：dict!getTree、grade!loadTree 等）
5. `send` 同名两义按 namespace 分流（`attachment!send` 读 / `short-message-detail!send` 写）
6. `.pyc` 会还原明文凭据——扫描器必须扫二进制且不跳过 `__pycache__`
7. 入库前检查器会污染它自己检查的东西（`precommit_check.py` 用 `-B` + 环境变量）
8. **两层覆盖无等价性测试**：注册表持续增长 vs 手写 mixin 冻结——考试域事件后
   立规矩「发现功能域立即建域」；`TestAggregate` 盯住聚合层
9. **分类器漏判靠后缀通则**：`WRITE_SUFFIX=(Complete,Approval,Save,Create,Update)`；
   `report`/`autograph` 按调用点核为写；`delte*` 是站点拼写，不是手误
10. **网关限流伪装成 404/500**：连发 ~70 请求后 502，探测必须二遍慢速重探
11. `transcript!detail`、`member!readByStudent`、`activity-record!readByTeacher`
    等为线上 404（GONE）——调用前看 md 标注

## 常用命令

```bash
python tools/Access/LoginSession.py password -u <学号> -p <密码>
python tools/XMYZClient.py --health
python tools/TestCases/TestContract.py
python tools/TestCases/TestApiReadOnly.py
python tools/TestCases/TestMethodSmoke.py          # 线上，116 法，约 2-4 分钟（可后台）
```

## 发布前必跑

```bash
python tools/TestCases/TestContract.py     # 9 项
python tools/Build/precommit_check.py      # 四道闸（产物/敏感串/会话模板/契约）
```

外加 `reference/` ≤150KB（当前 ≈105KB）。禁止 `compileall`/`py_compile` 写 `__pycache__`；
用内存编译 `python -c "compile(open(f).read(), f, 'exec')"`。

## 依赖

`requests`、`rapidocr-onnxruntime`（可选 OCR）、`numpy` + `Pillow`、`openpyxl`（ScoreTrend 导出）。

## 安全纪律

- 会话/凭据/导出文件不入库；`reference/.session.json` 是占位模板；真实会话在
  `%LOCALAPPDATA%\AutoXMYZ\session.json`（`AUTOMXYZ_SESSION` 可覆盖）
- 入库文档禁止真实姓名与真实 token
- 探测未知端点 `id=-1`、`limit=1`；不遍历真实 id
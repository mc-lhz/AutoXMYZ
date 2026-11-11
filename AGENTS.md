# AutoXMYZ 聚合技能 — 开发者契约

三站聚合：**CampusNet**（xmyz.xmedu.cn，校内系统）、**XmyzStudent**（xmyzstudent.com，学社）、
**XinYiWo**（www.591iq.cn，新壹我/591iq）。三站同一组学号密码，数据互不互通。

## 结构（子技能分区，非物理合并）

```
SKILL.md                    聚合入口：只写索引表 + 路径契约（懒加载，只读命中的 SUBSKILL）
AGENTS.md                   本文件：跨站点规则
README.md / VERSION / .gitignore
tools/
  Login.py                  统一登录编排（子进程调用，零跨子树 import）
  TestCases/TestAggregate.py 聚合契约
references/
  CampusNet/{SUBSKILL.md, AGENTS.md, tools/, reference/}
  XmyzStudent/{SUBSKILL.md, AGENTS.md, tools/, reference/}
  XinYiWo/{SUBSKILL.md, AGENTS.md（含变更历史与开发记忆）, README.md, VERSION, tools/, reference/}
```

**为什么分区而不是合并 `tools/`**：三边都用裸包名导入（`Access`/`Common`/`StudentBase`/
`TestCases` 同名）。同一 `sys.path` 下 `tools` 会解析到唯一目录（且 regular package 优先于
namespace package）——物理合并必然互相覆盖、双 `Log` 单例、异常类错位。分区 + 各自以
子树根为 cwd/sys.path 运行是唯一可靠解。

## 路径契约

- 子技能内部相对路径以 `references/<子技能>/` 为基准（文档中 `tools/...` 即该子树内）。
- 从聚合根执行：写完整前缀 `references/<子技能>/tools/...`。
- 根 `SKILL.md` 的 `<system-reminder>` 是唯一权威；新增子技能时同步更新索引与契约。

## 认证拓扑（单一凭据）

```
学号+密码
 ├─ CampusNet：门户直登（自有验证码）→ JSESSIONID（%LOCALAPPDATA%\AutoXMYZ\session.json）
 ├─ XinYiWo ：同一门户，用该 JSESSIONID 换发 ssoToken（不需要第二次验证码）
 └─ XmyzStudent：客户端只把同一凭据+学社自己的验证码发给学社；
                 学社服务端**服务端侧回调 CampusNet 校验**（不共享会话，只共享凭据）
```

- `tools/Login.py` 统一编排；每步子进程 `cwd=对应子树根`。
- 会话全部仓库外：`session.json` / `hub_session.json` / `iq_token.json`。
- 安全提示：学社登录会把密码经学社服务器转发 CampusNet（站点设计），
  不可信网络下勿用学社登录态。

## 红线（按子技能分治，不跨站统一）

- **CampusNet**：只写本人数据、可逆优先（create→verify→destroy）、不封装 `resetPassword`、
  不碰他人审批流；服务端权限是最终边界。
- **XmyzStudent**：自有平台功能完备；删除类方法名显式 `delete`，批量先自查 id；
  管理端点需 `*.manage` 权限（服务端 403 属预期）。
- **XinYiWo**：客户端闸门 + `--yes` + 回执校验；`records(type_)` 白名单；
  `queryRecord` 归属校验；默认脱敏；**不人员枚举**（已整体删除，不得复活）。
- 共性：未成年人个人信息不入库/不外传；入库文档禁止真实姓名与真实 token。

## 开发契约

- 子技能各自遵守其 `AGENTS.md`（目录/命名/mixin/同名 md/门面组合等）。
- **禁止跨子树 import**。需要联动时用子进程或按路径 `importlib` 加载（参考
  CampusNet `Build/login591.py` 的处理：`from tools.Access...` 会被 CampusNet 的正规包抢占）。
- 新增站点 = 新 `references/<Name>/` 子树（SUBSKILL + tools + reference + 可选 AGENTS）
  + 根索引/契约/`Login.py` 子命令 + `TestAggregate` 校验项。
- 各子树的契约/测试保持独立：CampusNet `TestContract`(9)+`TestApiReadOnly`(35)+
  `TestMethodSmoke`；XmyzStudent `TestHub`(15)+`TestHubSmoke`；XinYiWo `TestContract`(17)
  +`TestApiReadOnly`(52/53)+`TestRecordRead`+`TestWriteRehearsal`+`ApiCoverageAudit`。

## 测试矩阵

```bash
# 各子树（在各自目录下跑）
python tools/TestCases/TestContract.py      # CampusNet 9 项
python tools/TestCases/TestHub.py           # XmyzStudent 15 项
python tools/TestCases/TestContract.py      # XinYiWo 17 项（--strict 可阻断）

# 聚合层（根）
python tools/TestCases/TestAggregate.py     # 三子树存在/无游离 SKILL.md/路由关键词/子树契约/体积预算
```

线上冒烟（需会话）：`TestMethodSmoke`（CampusNet）、`TestHubSmoke`（XmyzStudent）。
线上测试不放 CI（避免学生账号进 secrets）。

## 发布

- 统一发版：根 `.github/workflows/release.yml` 打单包 `AutoXMYZ.zip`
  （根 SKILL/AGENTS/README/VERSION + `references/**` + `tools/Login.py`）。
- XinYiWo 不再单独发版（历史产物名 `591iqAutomatic.zip`；其子树内 `tools/Release/PackSkill.py`
  改产 `XinYiWo.zip` 供独立打包自检，但不再挂 Release）。
- CI 用内存编译（**不用 `compileall`**，避免 `__pycache__`），
  `PYTHONDONTWRITEBYTECODE=1`，ubuntu+windows，Python 3.11（声明 3.9+）。

## 已踩过的坑

1. **跨子树 `tools` 包名抢占**：`from tools.Access...` 在聚合仓库内解析到 CampusNet 的
   正规包（regular > namespace），XinYiWo 的模块找不到。解法：子进程或按路径 importlib。
2. **入口改名连带**：591iq 的 TestContract/PackSkill/README 都硬编码 `SKILL.md`，
   改 `SUBSKILL.md` 后必须同步（含打包必备清单）。
3. **reference 预算分区**：三子树各自 ≤150KB；合并计算会超限。
4. **触发词重叠**：「综合素质评价/成长记录/待办」在 CampusNet 与 XinYiWo 都出现——
   根 description 必须点名站点与系统边界，并声明数据不互通。
5. **git ls-files 作用域**：在子树内运行是 cwd 相对（无前缀），但文件必须先 `git add`
   才能被 PackSkill 收集。
6. 各子树的历史坑见其 `AGENTS.md`（CampusNet 11 条、XmyzStudent 5 条、XinYiWo 见其「开发记忆」并入段）。

## 安全纪律

- 会话/token/导出/验证码一律不入库；`.gitignore` 只挡产物（真正隔离靠仓库外路径）。
- `reference/api-privileged.md`（XinYiWo）继续不入库、不进包。
- 探测未知端点用 `id=-1`；短延迟串行；遇 4xx/429/502 停手并慢速重探。
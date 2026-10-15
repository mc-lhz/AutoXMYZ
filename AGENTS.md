# AGENTS.md

厦门一中信息校园综合应用系统（xmyz.xmedu.cn）**只读**工具集。纯 HTTP，读操作不需要浏览器。

## 架构

`tools/` 按业务域分目录，每个目录 = 一个业务域，门面 `XMYZClient.py` 留在 `tools/` 根：

```
tools/
  XMYZClient.py                  门面：组合各域 mixin，对外 API 就是 XMYZClient
  endpoint_kind.py               端点读写分类的唯一权威判定（建库与审计共用）
  Access/HttpTransport.py        传输层：_call / get / post / paged / login / _bindUser
  Access/LoginSession.py         登录四种方式：password / jsessionid / vision / check
  StudentBase/ProfileDict.py     身份、字典、学期、班级、网络磁盘
  LifeOffice/StudyMessage.py     成绩、成绩单、成长记录、作业、短信、通知、附件
  QualityCenter/QualityRead.py   综合素质评价（quality 域，20 个读取方法）
  CommunityCenter/VolunteerRead.py  社团（community）与志愿服务（volunteer）
  TestCases/TestApiReadOnly.py   只读 35 项探测，可重复运行
  TestCases/TestContract.py      仓库契约与能力红线审计（离线，无网络无凭据）
  Common/Logcat.py               彩色分等级日志（内部诊断；单例 `Log`）
```

- `reference/api.md` — 端点清单、来源前端、只读探测结果（本仓库唯一的参考文档）
- `SKILL.md` — skill 定义
- 每个 `.py` 都有同名 `.md`（门面 `XMYZClient.py` 豁免）
- 每个业务目录有 `__init__.py`

## 红线

**本技能纯只读。** 能力红线由 `Access/HttpTransport.py::_guard` 在**发请求前**强制执行：

- `WRITE_DENY_PREFIX` 列 60 余个写语义动词前缀，命中即抛 `WriteDenied`
- `READ_ALLOW` 豁免少数名字含动词但语义为读的端点（`attachment!send`、`!export`、`setRead`）
- `_call` 是唯一出口，**不得新增绕过 `_guard` 的调用路径**

新增能力时：先判断是否只读。**只读才加。**

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

## 常用命令

```bash
python tools/Access/LoginSession.py check                                   # 无凭据探测
python tools/Access/LoginSession.py vision -u <学号> -p <密码> --code ab12  # 登录（有读图能力）
python tools/Access/LoginSession.py password -u <学号> -p <密码>            # 登录（OCR）
python tools/XMYZClient.py --health                                          # 会话自检
python tools/TestCases/TestApiReadOnly.py                                    # 只读 35 项
python tools/TestCases/TestContract.py                                       # 契约审计（离线）
```

## 发布前必跑

`compileall` + `TestContract.py` + `TestApiReadOnly.py` + `reference/` 未超 150 KB。

## 依赖

requests、rapidocr-onnxruntime（验证码 OCR）、numpy + Pillow（预处理）。

## 安全纪律

- 提交前脱敏：不得包含密码 / 会话 id / 姓名 / 学号 / 班级 / userId
- 入库文档禁止出现任何真实姓名（含本人与他人），一律写「某学生」
- `reference/.session.json` 含真实会话，**不入库**（已 gitignore）
- 每加一条合规红线，必须配一条能证明它会红的**反向用例**
  （恒 PASS 的检查是装饰品）；反向用例不得真删文件，只 monkeypatch 或改临时副本，`finally` 还原
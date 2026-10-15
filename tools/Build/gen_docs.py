#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为每个 .py 生成同名 .md"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_work_dir()

DOCS = {
"tools/Common/Logcat.py": """彩色分等级日志。结论一律 `print` 走 stdout，内部诊断走这里走 stderr。
统一用单例 `Log`，不要在业务模块里再实例化，否则一份日志散到两个实例、等级各调各的。
打开 DEBUG：CLI `--verbose` 或环境变量 `XMYZ_VERBOSE=1`。
""",

"tools/Access/HttpTransport.py": """传输层：会话建立、只读调用、分页 + `XmyzError` / `WriteDenied`。

**`_call` 是唯一出口，能力红线守在这里。** `_guard` 在发请求前拦下所有写语义端点
（`WRITE_DENY_PREFIX`，60 余个动词前缀），命中即抛 `WriteDenied`。
少数名字含动词但语义为读的（`attachment!send`、`!export`、`setRead`）在 `READ_ALLOW` 豁免。

方法：`get` / `post` / `paged`（桌面端分页 `start`+`limit`）/ `login` / `loadCookie` / `_bindUser`。

⚠️ 两个踩过的坑：

1. `loggedIn` 字段不能用来判会话。未登录时返回 `{"loggedIn":false}`，
   登录后该字段**直接消失**，`get()` 于是返回 `None`——用 `== False` 判会误报未登录，
   用 `== True` 判则永远失败。判据是 profile 里有没有 `loginName` / `id`。

2. `__init__` 默认路径必须自己读会话文件。曾写成 `elif cookie:`，
   于是无参构造（门面最常见的用法）**静默不加载会话**，直接以未登录身份跑完全部方法；
   而未登录时多数只读端点照样返回 200，于是「测试全绿」，实则一条真实数据都没取到。
""",

"tools/Access/LoginSession.py": """登录（三种方式，输出同一个 JSESSIONID）：

- `password` —— 账号密码 + 验证码 OCR 自动重试
- `jsessionid` —— 浏览器已登录时复制会话，免验证码
- `vision` —— 取验证码图 / 凭 `--code` 提交
- `check` —— 无凭据探测端点可达性

**有读图能力时优先 `vision`**（实测 100%）；无读图能力用 `password` 的 OCR（变体池投票）。

会话落在 `reference/.session.json`（含真实凭据，**不入库**）。

验证码实测：**4~5 位、只含小写字母、一次性、服务端大小写敏感**。
`--interactive` 会阻塞，**agent 不得使用**。
""",

"tools/StudentBase/ProfileDict.py": """学生端基础数据：本人档案、字典、学期、班级、网络磁盘。
对应前缀 `account/` `system/` `edu/`。

- 身份：`status` / `profile` / `menuTree` / `readSimpleUser` /
  `readTeacherByParent` / `readStudentAndTeacherByParent` / `readBaseByClassTeacher`
- 字典：`comboStore` / `comboStoreCacheable` / `dictTree` / `schoolTermCombo` /
  `classCombo` / `gradeCombo` / `subjectCombo`
- 结构树：`gradeTree` / `classTreeByClassTeacher` / `parentCombo` / `classStudent` /
  `dormitoryStudent` / `teacherSimple`
- 其他：`weather` / `networkFolders` / `networkFiles`

`menuTree()` 是端点清单的**权威来源**：按当前账号权限下发，节点带 `action.jsFile`。
""",

"tools/LifeOffice/StudyMessage.py": """成绩、综评之外的学习与生活数据。
对应前缀 `edu/` `score/` `transcript/` `message/` `office/` `system/attachment`。

- 学业：`myScores` / `studentScoreTable` / `moduleScores` / `transcript` / `transcriptDetail` /
  `physicalExamination` / `classWork` / `homeworkCompleteTime` / `excellentWorks` /
  `matchAwards` / `attendanceByClass` / `speciality`
- 成长：`growthRecords` / `growthRecordDetail` / `classGrowthRecords`
- 消息：`inbox` / `outbox` / `messageDetail` / `unreadStat` / `recipientStat` /
  `categoryMessages` / `noticeFeedback` / `noticeByTarget` / `officeNotice`
- 附件：`attachmentsByIds` / `myAttachments` / `downloadUrl`

`downloadUrl` 只拼 URL 不下载内容——下载会落本地文件，超出只读查询范畴。
""",

"tools/QualityCenter/QualityRead.py": """综合素质评价域（`quality/`，30 端点）：学业之外十余项记录。
对应桌面端 `QualityPanel` 统辖的社团活动、党团活动、志愿服务、公益劳动、荣誉称号、
学科竞赛、体育比赛、艺术活动、军事训练、生产劳动、社会调查、勤工俭学、
科技创新、创造发明、典型案例。

`quality` / `qualityDetail` / `qualityScoreStat` / `selfDescription` / `honors` /
`volunteerService` / `volunteerLabour` / `competitionResult` / `sportsCompetition` /
`artActivity` / `studentArt` / `militaryTraining` / `productiveLabour` / `socialSurvey` /
`workStudy` / `learningOutcome` / `createInvention` / `typicalCase` /
`partyActivity` / `communityActivity`

注：本域与 591iqAutomatic 覆盖的新壹我综评系统（591iq.cn）是**两套独立系统**，数据不互通。
""",

"tools/CommunityCenter/VolunteerRead.py": """社团（`community/`，111 端点，全站最大域）与志愿服务（`volunteer/`，19 端点）。

- 社团：`communityTree` / `communityCombo` / `myCommunities` / `memberEvaluate` /
  `communityAttendance` / `communityNotice` / `propertyBorrow` / `forum` /
  `workDetail` / `memberTree`
- 志愿：`myVolunteerActivities` / `volunteerActivities` / `activityDetail` /
  `signRecords` / `surveys` / `registrations` / `volunteerHours`
""",

"tools/TestCases/TestApiReadOnly.py": """只读端点全量探测 35 项，可重复运行。
`--limit N` 快速冒烟，`--report` 输出报告 JSON。

⚠️ 判定口径：本系统有两类响应——

- **信封型**：`{"total":n,"data":[...],"success":true}`
- **裸数组 / 裸对象**：`dict!getTree` / `grade!loadTree` /
  `recipient!statInfo` / `community!loadTree`

只认信封会把 5 个真实可用端点误报 FAIL。**只要解析出 JSON 即 ALIVE，空数组也算**
（端点通、无数据 ≠ 不可用）。

退出码：0 全通过 / 1 有失败 / 4 会话不可用。
""",

"tools/TestCases/TestContract.py": """仓库契约与能力红线审计，**完全离线**（无网络、无凭据）。

9 项：写端点被拒、只读不被误拦、分类器一致、结构必备文件、每 py 有同名 md、
每目录有 `__init__.py`、reference 体积 ≤150KB、无硬编码凭据、全部 CLI `-h` 冒烟。

设计原则：**每条红线配一条能证明它会红的反向用例**——恒 PASS 的检查是装饰品，
只说明它对当前这版代码成立。
""",

"tools/endpoint_kind.py": """端点读写分类的**唯一权威判定**，被建库脚本与契约审计共用。

实现：先从 `模块!动作.action` 取出动作名，再做词元判定，不用正则硬拼。

⚠️ 旧实现每个正则分支后硬接 `\\.action$`，导致 `approve` 只匹配到 `approvedComplete`
的前 7 个字母、后面接不上 `.action` 而**漏判**，审批写端点被当成只读发起了请求
（返回「请选择同意或不同意」，因未传审批意见而无副作用）。

修正后 88 个端点重新归类：`delete` 121/121、`destroy` 30/30、`imp` 17/17 全部判写。
""",
}


def main():
    n = 0
    for rel, body in DOCS.items():
        src = os.path.join(D, rel.replace("/", os.sep))
        dst = src[:-3] + ".md"
        with open(dst, "w", encoding="utf-8") as f:
            f.write(body)
        n += 1
        print("  %s" % os.path.relpath(dst, D))
    print("已生成 %d 个同名 md" % n)


if __name__ == "__main__":
    main()
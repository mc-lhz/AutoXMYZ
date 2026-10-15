# 厦门一中信息校园综合应用系统 API 清单

目标站：`https://xmyz.xmedu.cn`（Struts2 后端，三个前端共用同一会话）

| 前端 | 入口 | 技术栈 | 端点数 | 角色 |
|---|---|---|---|---|
| 桌面管理端 | `manager.html` | ExtJS 3.4，服务端驱动按需加载 | 489 | 门户「登录」按钮指向的正式入口 |
| 移动端新版 | `m2.html` | Vue 3 + Vant，hash 路由 | 189 | 待办审批 + 4 项委托功能 |
| 移动端旧版 | `m.html` | Vue 2 + Vux，hash 路由 | 10 | 已被 m2 取代，m2 守卫失败时回落此处登录 |

合并去重后 **683** 个唯一端点：只读 360 / 写类 323。端点层几乎不重叠（三方共有 0 个），因为三个前端各写各的 Action 名；功能层互补。

## 授权口径

本文清单由**登录后的菜单树**（`POST /account/user!getGrantedMenuTree.action`）下发，并按各菜单节点携带的 `action.jsFile` 定向抓取 97 个模块得到，因此 desktop 一列的 489 个端点**是当前账号有权访问的**，不是静态猜测。
m2.html 一列来自前端 bundle 静态提取，反映能力面，实际可用性以运行时权限为准。

## 登录契约

```
GET  /system/system!currentTime.action                     # 取服务端毫秒时间，顺带分配会话
GET  /security/jcaptcha.jpg?_dc=<ms>                        # 验证码，与 JSESSIONID 强绑定
POST /j_spring_security_check                             # j_username / j_password=sha1(明文) / j_captcha
POST /account/user!getGrantedMenuTree.action              # 登录判据：返回非空菜单树
```

- 无 token / JWT，认证态就是 `JSESSIONID` Cookie（`Path=/`，同源三端共享）
- `j_password` 为 **无盐单次 SHA-1**（`hashlib.sha1(明文).hexdigest()`）
- 验证码 **4~5 位、只含小写字母、一次性、服务端大小写敏感**
- 桌面端另有 `account/user!qrCodeLogin.action`（扫码登录，需手机端配合）与 `account/user!sendSmsVerification.action`（短信），本技能不封装

## 只读探测结果

对 360 个只读端点各发一次 GET + POST（`start=0&limit=1`，`id` 一律用不存在的 `-1`），限速 180ms，结果：

| 判定 | 数量 | 含义 |
|---|---|---|
| ALIVE | 332 | 返回 2xx |
| FORBIDDEN | 9 | 401/403，账号无权 |
| GONE | 7 | 404，路由不存在 |
| REDIRECT | 1 | 302，典型是未绑定的单点登录 |
| ERROR | 11 | 连接异常或超时 |

`success:false` 且 `message` 是业务提示（如「合同申请或审批任务不存在」）也算 ALIVE——说明路由存在、鉴权通过，只是没有对应数据。

## 分页与信封

桌面端分页参数是 `start` + `limit`（`Config.js` 里 `LIMIT=60`），不是 m2 的 `page`/`pageSize`。响应根属性固定为：

```json
{"total": 12, "data": [ ... ], "success": true}
```

写入类响应则是 `{"success": false, "message": "..."}`。两者都叫 `success`，取值含义一致，但 `data` 可能缺失。

## 端点清单

> 只读端点带实测判定；写类端点仅登记，**本技能不封装任何写操作**。

### `edu`（118）

**只读 76**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `edu/attendance!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/class!getCampusLearnPhaseTree.action` | 桌面端 | ALIVE | 4 | json_list |
| `edu/class!loadTreeByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/class!loadTreeByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/class!loadTreeBySubjectTeacher.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/class-work!findWorkByStudent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/evaluation!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/grade!loadTree.action` | 桌面端 | ALIVE | 15 | json_list |
| `edu/grade!loadTreeByGradeTeacher.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/growth-record!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/growth-record!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/growth-record!exportByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/growth-record!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/growth-record!readByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/growth-record!readByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/growth-record!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/growth-record!readClassByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/growth-record-detail!detailJosn.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/homework-complete-time!exportTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/homework-complete-time!getTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/match-awards!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/match-awards-detail!delteAttachment.action` | 桌面端 | ALIVE | — | empty |
| `edu/match-awards-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module!loadTree.action` | 桌面端 | ALIVE | 16 | json_list |
| `edu/module!loadTreeByClassTeacher.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/module!loadTreeByGradeTeacher.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/module-score!export.action` | 桌面端 | ERROR | — | — |
| `edu/module-score!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!exportByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!exportByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!generateReferModuleScores.action` | 桌面端 | ERROR | — | — |
| `edu/module-score!handleArchiveScore.action` | 桌面端 | ERROR | — | — |
| `edu/module-score!initializtion.action` | 桌面端 | ERROR | — | — |
| `edu/module-score!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/module-score!readByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!readByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!readByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!readByStudent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/module-score!round.action` | 桌面端 | ERROR | — | — |
| `edu/notice!detailJosn.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/notice-grid!findClassReadByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/notice-grid!findGradeReadByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/notice-grid!findReadByGrade.action` | 桌面端 | GONE | — | html |
| `edu/notice-grid!findReadByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/notice-grid!findReadByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/parent!loadClassParent.action` | 桌面端 | FORBIDDEN | — | html |
| `edu/parent!loadSubjectTeacherClassParent.action` | 桌面端 | GONE | — | html |
| `edu/parent!loadTreeByTeacher.action` | 桌面端 | GONE | — | html |
| `edu/physical-examination!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!exportByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!initializtion.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!read.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/physical-examination!readByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!readByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/physical-examination!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/school-term!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `edu/school-year!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `edu/speciality!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/speciality!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `edu/student!getActivityRecord.action` | 桌面端 | ALIVE | — | empty |
| `edu/student!getClassmate.action` | m2.html | ALIVE | 1 | total, data, success |
| `edu/student!getComboStore.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/student!getTreeByStudent.action` | 桌面端 | ALIVE | 54 | json_list |
| `edu/student!loadClassStudent.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/student!loadDormitoryStudent.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/student!readBaseByClassTeacher.action` | m2.html | ALIVE | 0 | data, success, message |
| `edu/student!readBasic.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/student!verifyStudent.action` | 桌面端 | ALIVE | — | repeatList, studentIdList, notFoundList |
| `edu/teacher!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `edu/teacher!readSimple.action` | 桌面端+m2.html | ALIVE | 1 | total, data, success |

**写类 42**（不封装）

| 端点 | 来源 |
|---|---|
| `edu/growth-record!create.action` | 桌面端 |
| `edu/growth-record!createByStudent.action` | 桌面端 |
| `edu/growth-record!destroy.action` | 桌面端 |
| `edu/growth-record!imp.action` | 桌面端 |
| `edu/growth-record!impByClassTeacher.action` | 桌面端 |
| `edu/growth-record!impByGradeTeacher.action` | 桌面端 |
| `edu/growth-record!update.action` | 桌面端 |
| `edu/growth-record-detail!input.action` | 桌面端 |
| `edu/growth-record-detail!save.action` | 桌面端 |
| `edu/growth-record-detail!saveByStudent.action` | 桌面端 |
| `edu/homework-complete-time!updateTable.action` | 桌面端 |
| `edu/lesson-preparation-materials-detail!delete.action` | m2.html |
| `edu/match-awards!create.action` | 桌面端 |
| `edu/match-awards!destroy.action` | 桌面端 |
| `edu/match-awards!imp.action` | 桌面端 |
| `edu/match-awards!update.action` | 桌面端 |
| `edu/match-awards-detail!save.action` | 桌面端 |
| `edu/match-awards-detail!saveByStudentOrParnet.action` | 桌面端 |
| `edu/match-awards-detail!upload.action` | 桌面端 |
| `edu/module-score!create.action` | 桌面端 |
| `edu/module-score!deleteEmptyScore.action` | 桌面端 |
| `edu/module-score!destroy.action` | 桌面端 |
| `edu/module-score!imp.action` | 桌面端 |
| `edu/module-score!impByClassTeacher.action` | 桌面端 |
| `edu/module-score!impByGradeTeacher.action` | 桌面端 |
| `edu/module-score!impReport.action` | 桌面端 |
| `edu/module-score!update.action` | 桌面端 |
| `edu/module-score!updateClassCourse.action` | 桌面端 |
| `edu/notice-grid!setRead.action` | 桌面端 |
| `edu/physical-examination!create.action` | 桌面端 |
| `edu/physical-examination!destroy.action` | 桌面端 |
| `edu/physical-examination!imp.action` | 桌面端 |
| `edu/physical-examination!impByClassTeacher.action` | 桌面端 |
| `edu/physical-examination!impByGradeTeacher.action` | 桌面端 |
| `edu/physical-examination!impReport.action` | 桌面端 |
| `edu/physical-examination!update.action` | 桌面端 |
| `edu/physical-examination!updateCode.action` | 桌面端 |
| `edu/speciality!createByStudent.action` | 桌面端 |
| `edu/speciality!destroy.action` | 桌面端 |
| `edu/speciality!update.action` | 桌面端 |
| `edu/student-work-detail!input.action` | 桌面端 |
| `edu/student-work-detail!save.action` | 桌面端 |

### `community`（111）

**只读 63**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `community/attendance!action.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!buildMessageGridStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!generatedMessage.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!readAttendanceMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/community!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!exportByLeader.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getAllComboStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getComboStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getComboStoreByLeader.action` | 桌面端 | ALIVE | 0 | data, success |
| `community/community!getComboStoreByMember.action` | 桌面端 | ALIVE | 0 | data, success |
| `community/community!getComboStoreByTeacher.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/community!loadTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `community/community!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/community!readByLeader.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/community!readByMember.action` | 桌面端 | ALIVE | 0 | data, success |
| `community/community!readByRegister.action` | 桌面端 | ALIVE | 1 | total, data |
| `community/community!readByTeacher.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/community!sendMessage.action` | 桌面端 | ALIVE | — | text |
| `community/community-type!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/evaluate-item!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluate-item!getComboStoreByOwn.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/evaluation!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluation!exportByLeader.action` | 桌面端 | ALIVE | — | empty |
| `community/evaluation!initialization.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluation!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/evaluation!readByLeader.action` | 桌面端 | ALIVE | 0 | data, success |
| `community/exam-score!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/exam-score!stateByStudent.action` | 桌面端 | ALIVE | 0 | data |
| `community/lesson!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/member!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!exportAllMember.action` | 桌面端 | ALIVE | — | text |
| `community/member!exportByMember.action` | 桌面端 | ALIVE | — | text |
| `community/member!exportMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!grouping.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!loadParentTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `community/member!loadStudentTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `community/member!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/member!register.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!reportrAttendanceTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!evaluate.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!exportByAll.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!readByAll.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/member-evaluate!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/member-evaluate!readByTeacher.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/member-group!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/member-group!getComboStoreByOwn.action` | 桌面端 | ALIVE | 0 | data, success |
| `community/notice!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/notice!read.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/notice!readByMember.action` | 桌面端 | ALIVE | 0 | data, success |
| `community/notice-entity!read.action` | 桌面端 | ALIVE | — | empty |
| `community/property-borrow!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/property-borrow!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/property-borrow!read.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/property-borrow!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `community/reply!read.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/subject!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/work!download.action` | 桌面端 | ALIVE | — | text |
| `community/work!load.action` | 桌面端 | ALIVE | — | editorAttachmentIds, attachmentIds, content |

**写类 48**（不封装）

| 端点 | 来源 |
|---|---|
| `community/attendance!signAll.action` | 桌面端 |
| `community/community!create.action` | 桌面端 |
| `community/community!createByTeacher.action` | 桌面端 |
| `community/community!destroy.action` | 桌面端 |
| `community/community!update.action` | 桌面端 |
| `community/community-detail!input.action` | 桌面端 |
| `community/community-detail!save.action` | 桌面端 |
| `community/evaluate-item!create.action` | 桌面端 |
| `community/evaluate-item!destroy.action` | 桌面端 |
| `community/evaluate-item!update.action` | 桌面端 |
| `community/evaluation!create.action` | 桌面端 |
| `community/evaluation!destroy.action` | 桌面端 |
| `community/evaluation!imp.action` | 桌面端 |
| `community/evaluation!update.action` | 桌面端 |
| `community/exam-score!imp.action` | 桌面端 |
| `community/lesson!create.action` | 桌面端 |
| `community/lesson!destroy.action` | 桌面端 |
| `community/lesson!update.action` | 桌面端 |
| `community/member!cancelLeader.action` | 桌面端 |
| `community/member!create.action` | 桌面端 |
| `community/member!destroy.action` | 桌面端 |
| `community/member!imp.action` | 桌面端 |
| `community/member!setLeader.action` | 桌面端 |
| `community/member!update.action` | 桌面端 |
| `community/member!updateExit.action` | 桌面端 |
| `community/member!updateExpel.action` | 桌面端 |
| `community/member-evaluate!create.action` | 桌面端 |
| `community/member-evaluate!destroy.action` | 桌面端 |
| `community/member-evaluate!update.action` | 桌面端 |
| `community/member-group!destroy.action` | 桌面端 |
| `community/notice!create.action` | 桌面端 |
| `community/notice!destroy.action` | 桌面端 |
| `community/notice!update.action` | 桌面端 |
| `community/notice-entity!input.action` | 桌面端 |
| `community/notice-entity!save.action` | 桌面端 |
| `community/post!destroy.action` | 桌面端 |
| `community/property-borrow!destroy.action` | 桌面端 |
| `community/reply!create.action` | 桌面端 |
| `community/reply-entity!save.action` | 桌面端 |
| `community/subject!create.action` | 桌面端 |
| `community/subject!destroy.action` | 桌面端 |
| `community/subject!update.action` | 桌面端 |
| `community/subject-entity!save.action` | 桌面端 |
| `community/work!saveAttachment.action` | 桌面端 |
| `community/work!saveContent.action` | 桌面端 |
| `community/work!saveScoreOrSeatNumber.action` | 桌面端 |
| `community/work-detail!input.action` | 桌面端 |
| `community/work-detail!save.action` | 桌面端 |

### `elective`（98）

**只读 61**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `elective/activity-record!delteActivityPhotos.action` | 桌面端 | ALIVE | — | empty |
| `elective/activity-record!downloadAttachment.action` | 桌面端 | ERROR | — | — |
| `elective/activity-record!downloadAttachmentByCourseTeacher.action` | 桌面端 | ALIVE | — | text |
| `elective/activity-record!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/activity-record!exportByCourseTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/activity-record!exportByTeacher.action` | 桌面端 | GONE | — | html |
| `elective/activity-record!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `elective/activity-record!readByCourseTeacher.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `elective/activity-record!readByTeacher.action` | 桌面端 | GONE | — | html |
| `elective/activity-record!readByTeacherOrPresident.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective/activity-record!reportRollBook.action` | 桌面端 | GONE | — | html |
| `elective/attendance!export.action` | 桌面端 | ERROR | — | — |
| `elective/attendance!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!exportByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `elective/attendance!readByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!readByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!readByStudentOrParent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `elective/attendance!readByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!export.action` | 桌面端 | FORBIDDEN | — | html |
| `elective/course!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective/course!getComboStoreByElective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!getComboStoreByTeacher.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective/course!getComboStoreByTeacherOrPresident.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective/course!loadTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/course!loadTreeByAdvance.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/course!loadTreeByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course-detail!directSave.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective/elective!getComboStoreByAdvance.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective/elective!getComboStoreByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStoreByGradeOrClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective/elective!getComboStoreByTeacher.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective/elective!getGradeClassTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/elective!getGradeClassTreeByClassTeacher.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/elective-result!elective.action` | 桌面端 | ALIVE | — | success, refresh, message |
| `elective/elective-result!export.action` | 桌面端 | FORBIDDEN | — | html |
| `elective/elective-result!exportByAdvance.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!exportByClassTeacher.action` | 桌面端 | FORBIDDEN | — | html |
| `elective/elective-result!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!exportPacking.action` | 桌面端 | FORBIDDEN | — | html |
| `elective/elective-result!initProcessGrade.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!read.action` | 桌面端 | FORBIDDEN | — | html |
| `elective/elective-result!readByAdvance.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `elective/elective-result!readByClassTeacher.action` | 桌面端 | FORBIDDEN | — | html |
| `elective/elective-result!readByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!reportClassHourRegistration.action` | 桌面端 | ERROR | — | — |
| `elective/elective-result!reportClassHourRegistrationExcel.action` | 桌面端 | ERROR | — | — |
| `elective/elective-result!reportRollBook.action` | 桌面端 | ERROR | — | — |
| `elective/multiple-course!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-course!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective/multiple-course!getComboStoreByElective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-course!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `elective/multiple-course-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-result!elective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-result!lockElective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/wish!getStudentWish.action` | 桌面端 | ALIVE | — | json |

**写类 37**（不封装）

| 端点 | 来源 |
|---|---|
| `elective/activity-record!create.action` | 桌面端 |
| `elective/activity-record!createByCourseTeacher.action` | 桌面端 |
| `elective/activity-record!createByTeacherOrPresident.action` | 桌面端 |
| `elective/activity-record!destroy.action` | 桌面端 |
| `elective/activity-record!imp.action` | 桌面端 |
| `elective/activity-record!impByCourseTeacher.action` | 桌面端 |
| `elective/activity-record!update.action` | 桌面端 |
| `elective/activity-record!uploadActivityPhotos.action` | 桌面端 |
| `elective/activity-record-detail!delete.action` | m2.html |
| `elective/attendance!create.action` | 桌面端 |
| `elective/attendance!destroy.action` | 桌面端 |
| `elective/attendance!imp.action` | 桌面端 |
| `elective/attendance!update.action` | 桌面端 |
| `elective/attendance-detail!delete.action` | m2.html |
| `elective/course!create.action` | 桌面端 |
| `elective/course!destroy.action` | 桌面端 |
| `elective/course!imp.action` | 桌面端 |
| `elective/course!update.action` | 桌面端 |
| `elective/course-detail!input.action` | 桌面端 |
| `elective/elective-result!batchAdd.action` | 桌面端 |
| `elective/elective-result!batchPackingExport.action` | 桌面端 |
| `elective/elective-result!create.action` | 桌面端 |
| `elective/elective-result!createByAdvance.action` | 桌面端 |
| `elective/elective-result!destroy.action` | 桌面端 |
| `elective/elective-result!destroyByAdvance.action` | 桌面端 |
| `elective/elective-result!destroyByClassTeacher.action` | 桌面端 |
| `elective/elective-result!imp.action` | 桌面端 |
| `elective/elective-result!update.action` | 桌面端 |
| `elective/elective-result!updateByAdvance.action` | 桌面端 |
| `elective/elective-result!updateByClassTeacher.action` | 桌面端 |
| `elective/elective-result!updateByTeacher.action` | 桌面端 |
| `elective/multiple-course!create.action` | 桌面端 |
| `elective/multiple-course!destroy.action` | 桌面端 |
| `elective/multiple-course!imp.action` | 桌面端 |
| `elective/multiple-course!update.action` | 桌面端 |
| `elective/multiple-result!cancelElective.action` | 桌面端 |
| `elective/wish!saveWish.action` | 桌面端 |

### `activiti`（81）

**只读 3**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `/activiti/business/contract-approval!readByParticipate.action` | m2.html | ALIVE | 0 | total, data, success |
| `/activiti/business/parent-visit!read.action` | m2.html | ALIVE | 0 | total, data, success |
| `/activiti/business/parent-visit!readByParticipate.action` | m2.html | ALIVE | 0 | total, data, success |

**写类 78**（不封装）

| 端点 | 来源 |
|---|---|
| `/activiti/business/cj-contract-approval-detail!approvedComplete.action` | m2.html |
| `/activiti/business/cj-contract-approval-detail!approvedNoticeComplete.action` | m2.html |
| `/activiti/business/cj-contract-approval-detail!deptLeaderApprovalComplete.action` | m2.html |
| `/activiti/business/cj-contract-approval-detail!generalAffairsApprovalComplete.action` | m2.html |
| `/activiti/business/cj-contract-approval-detail!legalApprovalComplete.action` | m2.html |
| `/activiti/business/cj-contract-approval-detail!notApprovedComplete.action` | m2.html |
| `activiti/business/bfxx-document-flow-detail!delete.action` | m2.html |
| `activiti/business/bfxx-request-documents-detail!delete.action` | m2.html |
| `activiti/business/bfxx-use-car-detail!delete.action` | m2.html |
| `activiti/business/bsdhc-goods-purchase-detail!delete.action` | m2.html |
| `activiti/business/bsdhc-leave-detail!delete.action` | m2.html |
| `activiti/business/cj-document-flow-detail!delete.action` | m2.html |
| `activiti/business/cj-leave-detail!delete.action` | m2.html |
| `activiti/business/cj-overtime-detail!delete.action` | m2.html |
| `activiti/business/cj-purchase-request-detail!delete.action` | m2.html |
| `activiti/business/cj-seal-request-detail!delete.action` | m2.html |
| `activiti/business/cj-student-leave-detail!delete.action` | m2.html |
| `activiti/business/cj-topic-detail!completedComplete.action` | m2.html |
| `activiti/business/cj-topic-detail!notApprovedComplete.action` | m2.html |
| `activiti/business/cj-topic-detail!notifyOfficeComplete.action` | m2.html |
| `activiti/business/cj-topic-detail!principalApprovalComplete.action` | m2.html |
| `activiti/business/cj-topic-detail!schoolLeaderApprovalComplete.action` | m2.html |
| `activiti/business/cj-topic-detail!secretaryApprovalComplete.action` | m2.html |
| `activiti/business/cjkjxx-document-flow-detail!delete.action` | m2.html |
| `activiti/business/cjkjxx-leave-detail!delete.action` | m2.html |
| `activiti/business/cjkjxx-overtime-detail!delete.action` | m2.html |
| `activiti/business/cjkjxx-purchase-request-detail!delete.action` | m2.html |
| `activiti/business/cjkjxx-seal-request-detail!delete.action` | m2.html |
| `activiti/business/cjkjxx-student-leave-detail!delete.action` | m2.html |
| `activiti/business/currency-activity-leave-detail!delete.action` | m2.html |
| `activiti/business/currency-leave-detail!delete.action` | m2.html |
| `activiti/business/currency-outside-training-detail!delete.action` | m2.html |
| `activiti/business/currency-use-water-detail!delete.action` | m2.html |
| `activiti/business/dormitory-management-leave-detail!delete.action` | m2.html |
| `activiti/business/external-training-leave-detail!delete.action` | m2.html |
| `activiti/business/general-branch-meeting-detail!delete.action` | m2.html |
| `activiti/business/hcsyzx-document-flow-detail!delete.action` | m2.html |
| `activiti/business/hcsyzx-leave-detail!delete.action` | m2.html |
| `activiti/business/hcsyzx-student-leave-detail!delete.action` | m2.html |
| `activiti/business/information-release-detail!delete.action` | m2.html |
| `activiti/business/jmzx-goods-purchase-detail!delete.action` | m2.html |
| `activiti/business/jmzx-leave-detail!delete.action` | m2.html |
| `activiti/business/jmzx-student-leave-detail!delete.action` | m2.html |
| `activiti/business/jmzx-use-car-detail!delete.action` | m2.html |
| `activiti/business/material-exit-detail!delete.action` | m2.html |
| `activiti/business/matter-supervision-detail!delete.action` | m2.html |
| `activiti/business/open-school-affairs-detail!delete.action` | m2.html |
| `activiti/business/personal-info-auth!delete.action` | m2.html |
| `activiti/business/promotion-detail!delete.action` | m2.html |
| `activiti/business/record-class-detail!delete.action` | m2.html |
| `activiti/business/remote-gating-apply-detail!delete.action` | m2.html |
| `activiti/business/resign-detail!delete.action` | m2.html |
| `activiti/business/school-property-transfer-detail!delete.action` | m2.html |
| `activiti/business/seal-request-detail!delete.action` | m2.html |
| `activiti/business/student-certificate!delete.action` | m2.html |
| `activiti/business/student-leave-detail!delete.action` | m2.html |
| `activiti/business/study-trip-leave-detail!delete.action` | m2.html |
| `activiti/business/suggestion-box-detail!delete.action` | m2.html |
| `activiti/business/teacher-leave-school-detail!delete.action` | m2.html |
| `activiti/business/teaching-research-funds-detail!delete.action` | m2.html |
| `activiti/business/topic-detail!delete.action` | m2.html |
| `activiti/business/union-condolences-detail!delete.action` | m2.html |
| `activiti/business/xmyz-document-flow-detail!delete.action` | m2.html |
| `activiti/business/xmyz-leave-detail!delete.action` | m2.html |
| `activiti/business/xmyz-overtime-detail!delete.action` | m2.html |
| `activiti/business/xmyz-student-leave-detail!delete.action` | m2.html |
| `activiti/business/xnzx-activity-leave-detail!delete.action` | m2.html |
| `activiti/business/yfzx-course-adjustment-detail!delete.action` | m2.html |
| `activiti/business/yfzx-document-flow-detail!delete.action` | m2.html |
| `activiti/business/yfzx-leave-detail!delete.action` | m2.html |
| `activiti/business/yfzx-purchase-request-detail!delete.action` | m2.html |
| `activiti/business/yfzx-seal-request-detail!delete.action` | m2.html |
| `activiti/business/yjsy-leave-detail!delete.action` | m2.html |
| `activiti/business/yjsy-purchase-request-detail!delete.action` | m2.html |
| `activiti/business/ys-document-flow-detail!delete.action` | m2.html |
| `activiti/business/ys-leave-detail!delete.action` | m2.html |
| `activiti/business/ys-purchase-request-detail!delete.action` | m2.html |
| `activiti/business/ys-seal-request-detail!delete.action` | m2.html |

### `message`（32）

**只读 20**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `message/category!getSubCategory.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/message!html.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/message-grid!findReadByCategory.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/message-grid!findReadByParent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `message/message-grid!findReadByStudent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `message/message-grid!readByCategory.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `message/message-type!getDisplay.action` | 桌面端 | ALIVE | 2 | json_list |
| `message/recipient!exportByShortMessage.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/recipient!readByShortMessage.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `message/recipient!readNotReply.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/recipient!statInfo.action` | 桌面端 | ALIVE | 10 | notSignTotal, notReplyTotal, total, unreadTotal |
| `message/short-message!compressDownloadHasReturned.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/short-message!exportHasReturned.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/short-message!exportOutbox.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/short-message!inbox.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `message/short-message!outbox.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `message/short-message!readDialog.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/short-message!readHasReturned.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/short-message-detail!send.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/short-message-type!loadTree.action` | 桌面端 | ALIVE | 0 | json_list |

**写类 12**（不封装）

| 端点 | 来源 |
|---|---|
| `message/message-grid!destroy.action` | m2.html |
| `message/message-grid!setRead.action` | 桌面端 |
| `message/recipient!batchUpdateRead.action` | 桌面端 |
| `message/recipient!batchUpdateSign.action` | 桌面端 |
| `message/recipient!markAsUnread.action` | 桌面端 |
| `message/recipient!update.action` | 桌面端 |
| `message/short-message!destroy.action` | 桌面端+m2.html |
| `message/short-message!sendSms.action` | 桌面端 |
| `message/short-message!update.action` | 桌面端 |
| `message/short-message-detail!resend.action` | 桌面端 |
| `message/short-message-type!add.action` | 桌面端 |
| `message/short-message-type!remove.action` | 桌面端 |

### `quality`（30）

**只读 17**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `quality/quality!delteAttachment.action` | 桌面端 | ALIVE | — | empty |
| `quality/quality!downloadAttachment.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!export.action` | 桌面端 | FORBIDDEN | — | html |
| `quality/quality!exportByAudit.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!read.action` | 桌面端 | FORBIDDEN | — | html |
| `quality/quality!readByAudit.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `quality/quality!readByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!readByStudentOrParent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `quality/quality-category!getAuditPersonNames.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-score-stat!export.action` | 桌面端 | ERROR | — | — |
| `quality/quality-score-stat!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-score-stat!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `quality/quality-score-stat!readByStudentOrParent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `quality/student-description-detail!loadByStudentOrParnet.action` | 桌面端 | ALIVE | — | data, success |

**写类 13**（不封装）

| 端点 | 来源 |
|---|---|
| `quality/quality!create.action` | 桌面端 |
| `quality/quality!destroy.action` | 桌面端 |
| `quality/quality!imp.action` | 桌面端 |
| `quality/quality!update.action` | 桌面端 |
| `quality/quality!upload.action` | 桌面端 |
| `quality/quality-detail!batchImport.action` | 桌面端 |
| `quality/quality-detail!save.action` | 桌面端 |
| `quality/quality-detail!saveByStudentOrParnet.action` | 桌面端 |
| `quality/quality-score-stat!create.action` | 桌面端 |
| `quality/quality-score-stat!destroy.action` | 桌面端 |
| `quality/quality-score-stat!imp.action` | 桌面端 |
| `quality/quality-score-stat!update.action` | 桌面端 |
| `quality/student-description-detail!saveByStudentOrParnet.action` | 桌面端 |

### `archive`（23）

**只读 10**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `archive/archive-v2-campaign!completion.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-campaign!myOpen.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-export!teacher.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-record!detail.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-record!readMine.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-record!validate.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-review!detail.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-review!history.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-review!readPending.action` | m2.html | ALIVE | 0 | data, success, message |
| `archive/archive-v2-template!read.action` | m2.html | ALIVE | — | success, code, message |

**写类 13**（不封装）

| 端点 | 来源 |
|---|---|
| `archive/archive-v2-record!copy.action` | m2.html |
| `archive/archive-v2-record!deleteDraft.action` | m2.html |
| `archive/archive-v2-record!saveDraft.action` | m2.html |
| `archive/archive-v2-record!submit.action` | m2.html |
| `archive/archive-v2-record!toDraft.action` | m2.html |
| `archive/archive-v2-record!withdraw.action` | m2.html |
| `archive/archive-v2-review!approve.action` | m2.html |
| `archive/archive-v2-review!release.action` | m2.html |
| `archive/archive-v2-review!returnRecord.action` | m2.html |
| `archive/archive-v2-review!start.action` | m2.html |
| `archive/open-class-detail!delete.action` | m2.html |
| `archive/person-awards-detail!delete.action` | m2.html |
| `archive/unified-archives-detail!delete.action` | m2.html |

### `volunteer`（19）

**只读 10**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `volunteer/activity!readBySign.action` | 桌面端 | ALIVE | 1 | total, data |
| `volunteer/activity-registration!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity-registration!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `volunteer/activity-registration!registration.action` | 桌面端 | ALIVE | — | success, openVolunteerRegistration, message |
| `volunteer/activity-registration!unregistration.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity2!readByRegistration.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `volunteer/aimunc-detail!load.action` | 桌面端 | ALIVE | — | data, success |
| `volunteer/nhsdlc-detail!load.action` | 桌面端 | ALIVE | — | data, success |
| `volunteer/survey-detail!load.action` | 桌面端 | ALIVE | — | data, success |
| `volunteer/volunteer-registration-detail!load.action` | 桌面端 | ALIVE | — | data, success |

**写类 9**（不封装）

| 端点 | 来源 |
|---|---|
| `volunteer/activity-registration!create.action` | 桌面端 |
| `volunteer/activity-registration!destroy.action` | 桌面端 |
| `volunteer/activity-registration!imp.action` | 桌面端 |
| `volunteer/activity-registration!update.action` | 桌面端 |
| `volunteer/aimunc-detail!save.action` | 桌面端 |
| `volunteer/nhsdlc-detail!save.action` | 桌面端 |
| `volunteer/survey-detail!save.action` | 桌面端 |
| `volunteer/volunteer!sign.action` | 桌面端 |
| `volunteer/volunteer-registration-detail!save.action` | 桌面端 |

### `account`（15）

**只读 11**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `account/dept!loadTreeByUser.action` | 桌面端 | ALIVE | 17 | json_list |
| `account/dept!loadUserTree.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `account/user!calculateTotal.action` | 桌面端 | ALIVE | — | text |
| `account/user!getCustomUser.action` | 桌面端 | ALIVE | 0 | total |
| `account/user!readSimple.action` | 桌面端 | GONE | — | html |
| `account/user!readSimpleUser.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `account/user!readSimpleUserAndTeacher.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `account/user!readStudentAndTeacherByParent.action` | 桌面端 | ALIVE | 1067 | total, data, success |
| `account/user!readTeacherByParent.action` | 桌面端 | ALIVE | 43 | data |
| `account/user!simpleStatus.action` | m.html | ALIVE | — | success, loggedIn, loginName, name, dtype, principalSize, id |
| `account/user!status.action` | m2.html+m.html | ALIVE | — | communicate, sound, classTeacherName, seatNumber, studentId, classId, officePhone, loginName, schoolId, schoolUser, theme, id, address, dtype, dept |

**写类 4**（不封装）

| 端点 | 来源 |
|---|---|
| `account/dept!addUserDept.action` | 桌面端 |
| `account/dept!saveSelectedUser.action` | 桌面端 |
| `account/user!updateMobilePhone.action` | 桌面端 |
| `account/user!uploadUserPic.action` | 桌面端 |

### `psychological`（13）

**只读 7**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `psychological/appointment!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `psychological/appointment!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `psychological/appointment!readByRequest.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `psychological/appointment!readByTeacher.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `psychological/appointment-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `psychological/appointment-time!getComboStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `psychological/appointment-time!getComboStoreByRequest.action` | 桌面端 | ALIVE | 0 | data, success |

**写类 6**（不封装）

| 端点 | 来源 |
|---|---|
| `psychological/appointment!create.action` | 桌面端 |
| `psychological/appointment!createByTeacher.action` | 桌面端 |
| `psychological/appointment!destroy.action` | 桌面端 |
| `psychological/appointment!imp.action` | 桌面端 |
| `psychological/appointment!update.action` | 桌面端 |
| `psychological/appointment-detail!save.action` | 桌面端 |

### `system`（13）

**只读 9**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `system/attachment!download.action` | 桌面端 | ALIVE | — | empty |
| `system/attachment!readByIds.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `system/attachment!rotate.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `system/attachment!send.action` | 桌面端+m.html | ALIVE | — | empty |
| `system/attachment!toHtml.action` | 桌面端 | ALIVE | — | empty |
| `system/dict!getComboStore.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `system/dict!getComboStoreCacheable.action` | m2.html | ALIVE | 0 | data, success |
| `system/parameter!getParameterValue.action` | m2.html+m.html | ALIVE | — | text |
| `system/system!currentTime.action` | 桌面端 | ALIVE | — | text |

**写类 4**（不封装）

| 端点 | 来源 |
|---|---|
| `system/attachment!create.action` | 桌面端 |
| `system/attachment!destroy.action` | 桌面端 |
| `system/attachment!update.action` | 桌面端 |
| `system/attachment!upload.action` | 桌面端 |

### `office`（12）

**只读 7**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `office/calendar!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `office/calendar!gridCreate.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `office/calendar!gridDestroy.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `office/calendar!gridRead.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `office/calendar!gridUpdate.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `office/calendar!read.action` | 桌面端 | ALIVE | 0 | data |
| `office/notification-feedback-detail!load.action` | m2.html | ALIVE | 0 | data, success, message |

**写类 5**（不封装）

| 端点 | 来源 |
|---|---|
| `office/calendar!create.action` | 桌面端 |
| `office/calendar!destroy.action` | 桌面端 |
| `office/calendar!imp.action` | 桌面端 |
| `office/calendar!update.action` | 桌面端 |
| `office/notification-detail!delete.action` | m2.html |

### `exam`（9）

**只读 7**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `exam/answer!emptyByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/answer!statByStudent.action` | 桌面端 | ALIVE | 1 | data, success |
| `exam/online-exam!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `exam/online-exam!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success |
| `exam/question!readByExam.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/question!result.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/question-bank!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `exam/answer!saveAnswer.action` | 桌面端 |
| `exam/question!destroy.action` | 桌面端 |

### `evaluation`（8）

**只读 8**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `evaluation/evaluation!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `evaluation/evaluation!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success |
| `evaluation/evaluation-item!getEvaluationForm.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-result!evaluation.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-result!readEvaluationStudentByClassTeacher.action` | m2.html | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-result!readEvaluationStudentByGradeTeacher.action` | m2.html | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-result!studentEvaluationStatByClassTeacher.action` | m2.html | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-result!studentEvaluationStatByGradeTeacher.action` | m2.html | ALIVE | 0 | data, success, message |

### `m3`（7）

**只读 5**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `/m3/message!list.action` | m.html | ALIVE | 1 | json_list |
| `m3/weixin/bind-user!checkBind.action` | m.html | REDIRECT | — | empty |
| `m3/weixin/bind-user!existsWeixinUserId.action` | m.html | ALIVE | — | text |
| `m3/weixin/login!getBindingUserList.action` | m.html | ALIVE | 0 | data, success, message |
| `m3/weixin/login!loginSelectUser.action` | m.html | ALIVE | — | success |

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `m3/recipient-detail!delete.action` | m2.html |
| `m3/weixin/bind-user!bind.action` | m.html |

### `fund`（6）

**写类 6**（不封装）

| 端点 | 来源 |
|---|---|
| `fund/acceptance-detail!delete.action` | m2.html |
| `fund/contract-review-detail!delete.action` | m2.html |
| `fund/fund-settlement-detail!delete.action` | m2.html |
| `fund/procurement-execution-detail!delete.action` | m2.html |
| `fund/project-procurement-detail!delete.action` | m2.html |
| `fund/purchase-request-detail!delete.action` | m2.html |

### `moral`（6）

**只读 4**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `moral/class-month-activity!read.action` | m2.html | ALIVE | 0 | total, data, success |
| `moral/class-weekly-activity!read.action` | m2.html | ALIVE | 0 | total, data, success |
| `moral/guidance!read.action` | m2.html | ALIVE | 0 | total, data, success |
| `moral/student-check!readByStudent.action` | 桌面端 | ALIVE | 0 | total, data, success |

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `moral/guidance-detail!delete.action` | m2.html |
| `moral/home-visit-detail!delete.action` | m2.html |

### `score`（6）

**只读 6**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `score/score!exportParentScoreTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!exportStudentScoreTable.action` | 桌面端 | ALIVE | — | text |
| `score/score!getStudentOrParentScoreAnalysisOption.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!getSubjectAndTotalScoreTypeTreeByStudentOrPanel.action` | 桌面端 | ALIVE | 2 | json_list |
| `score/score!readParentScoreTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!readStudentScoreTable.action` | 桌面端 | ALIVE | 0 | data |

### `transcript`（6）

**只读 6**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `transcript/transcript!getTranscriptByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!getTranscriptByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!readByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!readByStudent.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `transcript/transcript!transcriptExportByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!transcriptExportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |

### `work-card`（5）

**只读 4**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `work-card/work!getWorkCardRecordWork.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `work-card/work-card!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `work-card/work-card!getComboStoreByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success |
| `work-card/work-card-record!statPercentRankByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `work-card/work-card-record!updateWorkCardRecord.action` | 桌面端 |

### `elective-evaluation`（4）

**只读 3**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `elective-evaluation/elective-evaluation!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective-evaluation/elective-evaluation!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success |
| `elective-evaluation/evaluation-feedback-detail!load.action` | 桌面端 | ALIVE | — | success, message |

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `elective-evaluation/evaluation-feedback-detail!save.action` | 桌面端 |

### `zz`（4）

**只读 4**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `zz/mobile!detail.action` | m2.html | ALIVE | — | result, logged, success, message |
| `zz/mobile!getArchive.action` | m2.html | ALIVE | — | result, logged, success, message |
| `zz/mobile!getGroupTree.action` | m2.html | ALIVE | — | result, logged, success, message |
| `zz/mobile!score.action` | m2.html | ALIVE | — | result, logged, success, message |

### `dormitory`（3）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `dormitory/dormitory!getTreeByManager.action` | 桌面端 | ALIVE | 0 | json_list |

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `dormitory/dorm-apply-detail!delete.action` | m2.html |
| `dormitory/quantify-detail!delete.action` | m2.html |

### `logistics`（3）

**写类 3**（不封装）

| 端点 | 来源 |
|---|---|
| `logistics/contract-detail!delete.action` | m2.html |
| `logistics/course-funding-apply-detail!delete.action` | m2.html |
| `logistics/payment-schedule-detail!delete.action` | m2.html |

### `note`（3）

**写类 3**（不封装）

| 端点 | 来源 |
|---|---|
| `note/activity-detail!delete.action` | m2.html |
| `note/notes-detail!delete.action` | m2.html |
| `note/notes-detail!save.action` | m2.html |

### `student-attendance`（3）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `student-attendance/attendance-type!getComboStore.action` | m2.html | ALIVE | 1 | data, success |

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `student-attendance/student-attendance-record-detail!delete.action` | m2.html |
| `student-attendance/student-long-term-attendance-detail!delete.action` | m2.html |

### `vote`（3）

**只读 3**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `vote/question!getForm.action` | 桌面端 | ALIVE | 0 | json_list |
| `vote/question!getStudentHomePageForm.action` | 桌面端 | ALIVE | 0 | json_list |
| `vote/result!vote.action` | 桌面端 | ALIVE | 0 | data, success, message |

### `award`（2）

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `award/student-award-record-detail!delete.action` | m2.html |
| `award/xmew-awards-detail!delete.action` | m2.html |

### `health`（2）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `health/health-info-settings!load.action` | m2.html | ALIVE | 0 | data, success, message |

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `health/health-info-settings!delete.action` | m2.html |

### `jmzx`（2）

**只读 2**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `jmzx/international-students-detail!load.action` | m2.html | ALIVE | — | success, message, data |
| `jmzx/recruit-teacher-detail!load.action` | m2.html | ALIVE | — | success, message, data |

### `print`（2）

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `print/print-application-detail!delete.action` | m2.html |
| `print/print-detail!delete.action` | m2.html |

### `purchase`（2）

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `purchase/funds-detail!delete.action` | m2.html |
| `purchase/purchase-request-detail!delete.action` | m2.html |

### `shake-attendance`（2）

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `shake-attendance/attendance!delete.action` | m2.html |
| `shake-attendance/unattendance!delete.action` | m2.html |

### `supervision`（2）

**写类 2**（不封装）

| 端点 | 来源 |
|---|---|
| `supervision/campus-feedback-person-detail!delete.action` | m2.html |
| `supervision/supervision-detail!delete.action` | m2.html |

### `tour-class`（2）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `tour-class/check-item!getComboStore.action` | m2.html | ALIVE | 0 | data, success |

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `tour-class/tour-class-detail!delete.action` | m2.html |

### `yfzx`（2）

**只读 2**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `yfzx/mobile!load.action` | m2.html | ALIVE | — | success, message, data |
| `yfzx/recruit-teacher-detail!load.action` | m2.html | ALIVE | — | success, message, data |

### `-detail`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `/-detail!delete.action` | m2.html |

### `base`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `base/building-detail!delete.action` | m2.html |

### `cjtcs`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `cjtcs/mobile!load.action` | m2.html | ALIVE | — | success, message, data |

### `class-evaluation`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `class-evaluation/civilized-class-evaluation-detail!delete.action` | m2.html |

### `duty`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `duty/duty-inspection-detail!delete.action` | m2.html |

### `enroll`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `enroll/mobile!load.action` | m2.html | ALIVE | — | success, message, data |

### `experiment`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `experiment/experimental-detail!delete.action` | m2.html |

### `experimental-class`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `experimental-class/mobile!load.action` | m2.html | ALIVE | — | success, message, data |

### `face`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `face/temporary-out-school-detail!delete.action` | m2.html |

### `general-affairs`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `general-affairs/property-inspection-record-detail!delete.action` | m2.html |

### `hcsytcs`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `hcsytcs/mobile!load.action` | m2.html | ALIVE | — | success, message, data |

### `homework-announcement`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `homework-announcement/homework-announcement-detail!delete.action` | m2.html |

### `jmzxtcs`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `jmzxtcs/mobile!load.action` | m2.html | ALIVE | — | success, message, data |

### `online-exam`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `online-exam/exam-situation!readAllExamSituation.action` | 桌面端 | ALIVE | 0 | data, success |

### `school-assets`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `school-assets/school-assets-detail!delete.action` | m2.html |

### `security`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `security/patrol-record-detail!delete.action` | m2.html |

### `service`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `service/service-detail!delete.action` | m2.html |

### `teaching-research`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `teaching-research/yfzx-quarterly-assessment-detail!delete.action` | m2.html |

### `venue`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `venue/venue-application-detail!delete.action` | m2.html |

### `visitor`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `visitor!delete.action` | m2.html |

### `visitor2022`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `visitor2022/visitor-detail!delete.action` | m2.html |

### `warehouse`（1）

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `warehouse/goods-use-apply-detail!delete.action` | m2.html |

### `xmyz`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `xmyz/recruit-teacher-detail!load.action` | m2.html | ALIVE | — | success, message, data |

### `yztcs`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `yztcs/mobile!load.action` | m2.html | ALIVE | — | success, message, data |

## 机器可读

- `endpoints.json` — 全部 683 个端点，含 `sources` / `kind` / `menus` / `files`
- `validation.json` — 360 个只读端点的实测响应结构
- `menu_tree.json` — 菜单树原始响应（130 节点）
- `desktop_endpoints.json` — 489 个桌面端端点，含来源 jsFile 与所属菜单名

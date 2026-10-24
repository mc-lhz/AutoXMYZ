# 厦门一中信息校园综合应用系统 API 清单

目标站：`https://xmyz.xmedu.cn`（Struts2 后端，三个前端共用同一会话）

| 前端 | 入口 | 技术栈 | 端点数 | 角色 |
|---|---|---|---|---|
| 桌面管理端 | `manager.html` | ExtJS 3.4，服务端驱动按需加载 | 489 | 门户「登录」按钮指向的正式入口 |
| 移动端新版 | `m2.html` | Vue 3 + Vant，hash 路由 | 2154 | 待办审批 + 4 项委托功能 |
| 移动端旧版 | `m.html` | Vue 2 + Vux，hash 路由 | 10 | 已被 m2 取代，m2 守卫失败时回落此处登录 |

合并去重后 **2623** 个唯一端点：只读 1192 / 写类 1431。端点层几乎不重叠（三方共有 0 个），因为三个前端各写各的 Action 名；功能层互补。

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

对 1176 个只读端点各发一次 GET + POST（`start=0&limit=1`，`id` 一律用不存在的 `-1`），限速 180ms，结果：

| 判定 | 数量 | 含义 |
|---|---|---|
| ALIVE | 1051 | 返回 2xx |
| FORBIDDEN | 1 | 401/403，账号无权 |
| GONE | 16 | 404，路由不存在 |
| REDIRECT | 71 | 302，典型是未绑定的单点登录 |
| ERROR | 37 | 连接异常或超时 |

`success:false` 且 `message` 是业务提示（如「合同申请或审批任务不存在」）也算 ALIVE——说明路由存在、鉴权通过，只是没有对应数据。

## 分页与信封

桌面端分页参数是 `start` + `limit`（`Config.js` 里 `LIMIT=60`），不是 m2 的 `page`/`pageSize`。响应根属性固定为：

```json
{"total": 12, "data": [ ... ], "success": true}
```

写入类响应则是 `{"success": false, "message": "..."}`。两者都叫 `success`，取值含义一致，但 `data` 可能缺失。

## 端点清单

> 只读端点带实测判定；写类端点仅登记，**本技能不封装任何写操作**。

### `activiti`（1144）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `academicAffairsOfficerApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovalComplete*`
    `academicDirectorApprovalComplete*`  `academicDirectorApprovedComplete*`
    `accountingApprovalComplete*`  `accountingApprovalComplete*`  `accountingApprovalComplete*`
    `activityDirectorApprovalComplete*`  `activityDirectorApprovalComplete*`
    `activityDirectorApprovalComplete*`  `activityDirectorApprovalComplete*`
    `adminCommentsComplete*`  `agreeComplete*`  `applicationData`  `approvalComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedNoticeComplete*`
    `approvedNoticeComplete*`  `approvedNoticeComplete*`  `approvedNoticeComplete*`
    `approvedNoticeComplete*`  `approvedNoticeComplete*`  `approvedNoticeComplete*`
    `approvedNoticeComplete*`  `approvedNoticeComplete*`  `approvedNoticeComplete*`
    `approvedNoticeComplete*`  `archivingComplete*`  `arrangeSchoolBusesComplete*`
    `assetManagerWarehousingComplete*`  `assetManagerWarehousingComplete*`
    `assetManagerWarehousingComplete*`  `assetManagerWarehousingComplete*`
    `assetsResponsibleApprovalComplete*`  `branchSecretaryApprovalComplete*`
    `branchSecretaryApprovalComplete*`  `branchSecretaryApprovalComplete*`
    `campusLeaderApprovalComplete*`  `campusLeaderApprovalComplete*`
    `campusPrincipalApprovalComplete*`  `campusPrincipalApprovalComplete*`
    `campusPrincipalApprovalComplete*`  `campusPrincipalApprovalComplete*`
    `campusPrincipalApprovalComplete*`  `campusUnionApprovalComplete*`  `captcha`
    `carbonCopyComplete*`  `carbonCopyComplete*`  `carbonCopyComplete*`  `carbonCopyComplete*`
    `carbonCopyComplete*`  `carbonCopyComplete*`  `carbonCopyComplete*`  `carbonCopyComplete*`
    `carbonCopyComplete*`  `checkUserExists`  `checkUserExists`  `checkUserExists`
    `checkUserExists`  `checkUserExists`  `checkUserExists`  `checkUserExists`
    `checkUserExists`  `checkUserExists`  `checkUserExists`  `checkUserExists`
    `circulationComplete*`  `classTeacherApprovalComplete*`  `classTeacherApprovalComplete*`
    `classTeacherApprovalComplete*`  `classTeacherApprovalComplete*`
    `classTeacherApprovalComplete*`  `classTeacherApprovalComplete*`
    `classTeacherApprovalComplete*`  `classTeacherApprovalComplete*`
    `classTeacherApprovedComplete*`  `classTeacherArrangementComplete*`
    `classTeacherOrDormitoryManagerApprovalComplete*`
    `classTeacherOrDormitoryManagerApprovalComplete*`
    `classTeacherOrDormitoryManagerApprovalComplete*`  `collectionComplete*`
    `completedComplete*`  `completedComplete*`  `completionNoticeComplete*`
    `completionNoticeComplete*`  `comprehensiveServiceCenterApprovalComplete*`
    `comprehensiveServiceCenterApprovalComplete*`  `confidentialityApprovalComplete*`
    `contactPersonApprovalComplete*`  `courseAdjustmentTeacherApprovalComplete*`
    `courseConstructionCenterApprovalComplete*`  `courseConstructionCenterApprovalComplete*`
    `courseConstructionCenterApprovalComplete*`  `courseConstructionCenterApprovalComplete*`
    `custodyApprovalComplete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `delete*`  `delete*`
    `departmentApprovalComplete*`  `departmentApprovalComplete*`  `departmentApprovalComplete*`
    `departmentApprovalComplete*`  `departmentContactCommentsComplete*`
    `departmentContactCommentsComplete*`  `departmentDirectorApprovalComplete*`
    `departmentHeadApprovalComplete*`  `departmentHeadApprovalComplete*`
    `departmentHeadApprovalComplete*`  `departmentLeaderApprovalComplete*`
    `departmentLeaderComplete*`  `departmentLeaderComplete*`  `departmentLeaderComplete*`
    `departmentLeaderComplete*`  `departmentLeaderComplete*`  `departmentLeaderComplete*`
    `departmentLeaderComplete*`  `departmentLeaderComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`  `deptLeaderApprovalComplete*`
    `deptLeaderApprovalComplete*`  `deptLeaderApprovedComplete*`  `deptLeaderComplete*`
    `deptLeaderComplete*`  `deputySecretaryApprovalComplete*`  `detailByOpenId`
    `disagreeComplete*`  `dispatchComplete*`  `distributeComplete*`  `distributeComplete*`
    `dormitoryManagementDirectorApprovalComplete*`  `dutyRoomComplete*`  `dutyRoomComplete*`
    `enterSchool*`  `enterSchool*`  `enterSchool*`  `enterSchool*`  `enterSchool*`
    `enterSchool*`  `enterSchool*`  `evaluationFeedbackComplete*`
    `financialAccountingApprovalComplete*`  `finishedComplete*`  `finishedComplete*`
    `generalAffairsApprovalComplete*`  `generalAffairsApprovalComplete*`
    `generalAffairsApprovalComplete*`  `generalAffairsApprovalComplete*`
    `generalAffairsApprovalComplete*`  `generalAffairsApprovalComplete*`
    `generalAffairsApprovalComplete*`  `generalAffairsApprovalComplete*`
    `generalAffairsApprovalComplete*`  `generalAffairsApprovalComplete*`
    `generalAffairsVehicleDispatchComplete*`  `getComboStore`  `getComboStore`
    `getInstructionsAndWord`  `getNextReceiptNumber`  `getNextReceiptNumber`
    `getNextReceiptNumber`  `getNextReceiptNumber`  `getNextReceiptNumber`
    `getNextReceiptNumber`  `getNextReceiptNumber`  `getNextReceiptNumber`
    `getNextReceiptNumber`  `getUserComboStore`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovalComplete*`
    `gradeTeacherApprovalComplete*`  `gradeTeacherApprovedComplete*`
    `gradeTeacherPendingLeaveApprovalTasks`  `groupApprovalComplete*`
    `groupAssetsResponsibleApprovalComplete*`  `groupPartySecretaryApprovalComplete*`
    `groupPersonnelApprovalComplete*`  `groupPrincipalApprovalComplete*`
    `groupPrincipalInChargeApprovalComplete*`  `groupSchoolAffairsDepartmentApprovalComplete*`
    `handlerFeedbackComplete*`  `handlerFeedbackComplete*`  `hasHandled`  `hasHandled`
    `historyContactPersons`  `informationCenterManagerApprovalComplete*`
    `informationReviewerApprovalComplete*`  `laboratoryDirectorApprovalComplete*`
    `lastApplicant`  `leaderInChargeApprovalComplete*`  `leaderInChargeApprovalComplete*`
    `leaderInChargeApprovalComplete*`  `leadingDepartmentCommentsComplete*`
    `leadingDepartmentCommentsComplete*`  `leaveNoticeComplete*`  `leaveNoticeComplete*`
    `leaveNoticeComplete*`  `leaveNoticeComplete*`  `leaveSchool*`  `leaveSchool*`
    `leaveSchool*`  `leaveSchool*`  `leaveSchool*`  `leaveSchool*`  `leaveSchool*`
    `legalApprovalComplete*`  `lessonPreparationTeamLeaderApprovalComplete*`
    `librarianApprovalComplete*`  `librarianApprovalComplete*`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`  `load`
    `load`  `materialExitDepartments`  `modifyApplication*`  `modifyApplication*`
    `modifyApplication*`  `modifyApplication*`  `modifyApplication*`
    `modifyApplicationComplete*`  `modifyComplete*`  `modifyRegistrationComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovalComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovalComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovalComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovalComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovalComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovalComplete*`
    `moralEducationApprovalComplete*`  `moralEducationApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `noticeComplete*`  `noticeComplete*`
    `noticeComplete*`  `noticeComplete*`  `noticeComplete*`  `noticeComplete*`
    `noticeComplete*`  `noticeComplete*`  `noticeComplete*`  `noticeComplete*`
    `noticeComplete*`  `noticeComplete*`  `noticeComplete*`  `noticeLeave*`  `noticeLeave*`
    `noticeLeaveComplete*`  `notifyComplete*`  `notifyComplete*`  `notifyComplete*`
    `notifyComplete*`  `notifyComplete*`  `notifyComplete*`  `notifyGradeTeacherComplete*`
    `notifyOfficeComplete*`  `notifyOfficeComplete*`  `notifyPrincipalComplete*`
    `notifyServiceComplete*`  `notifyWithSealComplete*`  `notifyWithSealComplete*`
    `notifyWithSealComplete*`  `notifyWithSealComplete*`  `notifyWithSealComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovalComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovalComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovalComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovalComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovalComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovalComplete*`
    `officeApprovalComplete*`  `officeApprovalComplete*`  `officeApprovedComplete*`
    `officeCommentsComplete*`  `officeCommentsComplete*`  `officeComplete*`  `officeComplete*`
    `officeComplete*`  `officeConfirmationApprovalComplete*`  `officeConfirmationComplete*`
    `officeDraftOpinionComplete*`  `officeProposedDraftOpinionComplete*`  `openDoor*`
    `partyBuildingSupervisionCenterApprovalComplete*`  `partyCommitteeLeaderApprovalComplete*`
    `partyCommitteeOfficeCommentsComplete*`  `partyCommitteeOfficeCommentsComplete*`
    `partyOfficeApprovalComplete*`  `partyOrganizationComplete*`
    `partySecretaryApprovalComplete*`  `personalTask`  `personnelApprovalComplete*`
    `perusalComplete*`  `perusalComplete*`  `perusalComplete*`  `perusalComplete*`
    `perusalComplete*`  `perusalComplete*`  `perusalComplete*`  `perusalComplete*`
    `perusalComplete*`  `perusalComplete*`  `perusalComplete*`  `preSubstituteComplete*`
    `preSubstituteComplete*`  `prepareLessonsLeaderApprovalComplete*`  `priceApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovalComplete*`  `principalApprovalComplete*`  `principalApprovalComplete*`
    `principalApprovedComplete*`  `principalComplete*`  `principalComplete*`
    `principalComplete*`  `principalComplete*`  `principalComplete*`  `principalComplete*`
    `principalComplete*`  `processTaskInstance`  `publicityDepartmentApprovalComplete*`
    `publicityDepartmentFilingComplete*`  `purchaseComplete*`  `purchaseComplete*`
    `purchaseComplete*`  `purchaseComplete*`  `purchaseComplete*`  `purchaseComplete*`
    `purchaseComplete*`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`
    `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`
    `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`  `read`
    `read`  `read`  `readByApplicant`  `readByApplicant`  `readByApplicant`  `readByApplicant`
    `readByApplicant`  `readByApplicant`  `readByApplicant`  `readByApplicant`
    `readByApplicant`  `readByApplicant`  `readByApplicant`  `readByApplicant`
    `readByApplicant`  `readByApplicant`  `readByApplicant`  `readByApplication`
    `readByApplication`  `readByApply`  `readByApply`  `readByApply`  `readByApproval*`
    `readByArrangementClassTeacher`  `readByBsdhcGoodsPurchase`  `readByClassTeacher`
    `readByGradeTeacher`  `readByJmzxGoodsPurchase`  `readByLeaveSchool`  `readByParent`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByPurchaseRequest`  `readByRegistration`  `readByRegistration`  `readByRegistration`
    `readByRegistration`  `readByRegistration`  `readByRegistration`  `readByRegistration`
    `readByRegistration`  `readByRegistration`  `readByRegistration`
    `readByReplaceClassTeacher`  `readBySchoolTermWeekId`  `readByTeacher`  `readByTeacher`
    `readByTeacher`  `readByUser`  `readByUser`  `readByUser`  `readByUser`  `readByUser`
    `readByUser`  `readByUser`  `readByUser`  `readByUser`  `readByUser`  `readByUser`
    `readByUser`  `readByUser`  `readByUser`  `readByUser`  `readByUser`  `readByView`
    `readByView`  `readByView`  `readByView`  `readByView`  `readByView`  `readByView`
    `readByView`  `readByView`  `readByView`  `readByView`  `receiveComplete*`
    `receiveNotificationComplete*`  `receptionComplete*`  `registration`  `registration`
    `registration`  `registration`  `registration`  `registration`  `registration`
    `replaceClassTeacherConfirmed`  `replyComplete*`  `report*`  `report*`  `report*`
    `report*`  `report*`  `report*`  `report*`  `report*`  `report*`  `report*`  `report*`
    `report*`  `report*`  `report*`  `report*`  `report*`  `report*`  `report*`  `report*`
    `report*`  `report*`  `report*`  `report*`  `report*`  `report*`  `report*`  `report*`
    `report*`  `report*`  `reportOutsideTraining`  `reportPrincipalComplete*`
    `researchGroupApprovalComplete*`  `researchGroupLeaderApprovalComplete*`
    `researchGroupLeaderApprovalComplete*`  `researchGroupLeaderApprovalComplete*`
    `researchGroupLeaderApprovalComplete*`  `researchGroupLeaderApprovalComplete*`
    `researchGroupLeaderApprovedComplete*`  `responsibleDepartmentApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderCommentsComplete*`  `responsibleLeaderCommentsComplete*`
    `responsibleLeaderComplete*`  `responsibleLeaderComplete*`  `responsibleLeaderComplete*`
    `responsiblePersonApprovalComplete*`  `resultQueryByOpenId`  `returnComplete*`
    `returnInitiatorComplete*`  `returnInitiatorComplete*`  `returnInitiatorComplete*`
    `returnInitiatorComplete*`  `returnInitiatorComplete*`  `returnInitiatorComplete*`  `save*`
    `save*`  `save*`  `save*`  `save*`  `save*`  `save*`  `save*`  `save*`  `save*`  `save*`
    `save*`  `save*`  `saveSignatureData*`  `schoolAdministrationCenterApprovalComplete*`
    `schoolAffairsDepartmentApprovalComplete*`  `schoolLeaderApprovalComplete*`
    `schoolLeaderApprovalComplete*`  `schoolLeaderApprovalComplete*`
    `schoolLeaderApprovalComplete*`  `schoolLeaderApprovalComplete*`
    `schoolLeaderApprovalComplete*`  `schoolLeaderApprovalComplete*`  `schoolLeaderComplete*`
    `schoolLeaderComplete*`  `schoolLeaderComplete*`  `schoolLeaderComplete*`
    `schoolLeaderComplete*`  `secretaryApprovalComplete*`  `secretaryApprovalComplete*`
    `secretaryApprovalComplete*`  `secretaryApprovedComplete*`  `secretaryComplete*`
    `secretaryComplete*`  `secretaryComplete*`  `secretaryComplete*`  `secretaryComplete*`
    `secretaryComplete*`  `secretaryComplete*`  `secretaryPrincipalApprovalComplete*`
    `secretaryPrincipalApprovalComplete*`  `secretaryPrincipalApprovalComplete*`
    `secretaryPrincipalComplete*`  `secretaryPrincipalComplete*`  `secretaryReviewComplete*`
    `securityOfficeApprovalComplete*`  `securityOfficeApprovalComplete*`
    `securityOfficeApprovalComplete*`  `serviceCenterReceiveComplete*`
    `sportsEquipmentRoomLeaderApprovalComplete*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflowByHcsyzx*`  `startYjsyzxWorkflow*`  `statistics`
    `studentGrowthCenterApprovalComplete*`  `studentGrowthCenterApprovalComplete*`
    `studentGrowthCenterApprovalComplete*`  `substituteArrangementComplete*`
    `substituteClassTeacherConfirmedComplete*`  `substituteComplete*`  `substituteComplete*`
    `substituteComplete*`  `substituteComplete*`  `substituteComplete*`  `substituteComplete*`
    `taskInstance`  `teacherDevelopmentCenterApprovalComplete*`
    `teacherDevelopmentCenterApprovalComplete*`  `teacherDevelopmentCenterApprovalComplete*`
    `teacherDevelopmentCenterApprovalComplete*`  `teachingDepartmentApprovalComplete*`
    `teachingResearchOfficeApprovalComplete*`  `teachingServiceCenterApprovalComplete*`
    `unfinishedTaskInstance`  `unionApprovalComplete*`  `unionApprovedComplete*`
    `unionPresidentApprovalComplete*`  `unionPresidentApprovalComplete*`  `updateApplication*`
    `updateDraftOpinionComplete*`  `usageFeedbackComplete*`
    `vehicleDispatchingApprovalComplete*`  `vehicleDispatchingComplete*`  `verifyContactPerson`
    `vicePrincipalApprovalComplete*`  `vicePrincipalApprovalComplete*`
    `vicePrincipalApprovalComplete*`  `vicePrincipalApprovalComplete*`
    `vicePrincipalApprovalComplete*`  `vicePrincipalApprovalComplete*`
    `vicePrincipalApprovalComplete*`  `vicePrincipalApprovalComplete*`
    `vicePrincipalApprovedComplete*`  `viceUnionPresidentApprovalComplete*`
```
`*` 后缀 = 写类。共 1144 个（读 297 / 写 847）。

### `edu`（187）

**只读 73**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `edu/attendance!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/class!getCampusLearnPhaseTree.action` | 桌面端+m2.html | ALIVE | 4 | json_list |
| `edu/class!loadTreeByClassTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `edu/class!loadTreeByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/class!loadTreeBySubjectTeacher.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `edu/class-work!findWorkByStudent.action` | 桌面端 | REDIRECT | — | empty |
| `edu/evaluation!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/grade!loadTree.action` | 桌面端 | REDIRECT | — | empty |
| `edu/grade!loadTreeByGradeTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!export.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!exportByClassTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!exportByGradeTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!read.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!readByClassTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!readByGradeTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!readByStudent.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record!readClassByStudent.action` | 桌面端 | REDIRECT | — | empty |
| `edu/growth-record-detail!detailJosn.action` | 桌面端 | REDIRECT | — | empty |
| `edu/homework-complete-time!exportTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/homework-complete-time!getTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/match-awards!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/match-awards-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module!loadTree.action` | 桌面端 | ALIVE | 16 | json_list |
| `edu/module!loadTreeByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module!loadTreeByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
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
| `edu/module-score!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/module-score!round.action` | 桌面端 | ERROR | — | — |
| `edu/notice!detailJosn.action` | 桌面端 | REDIRECT | — | empty |
| `edu/notice-grid!findClassReadByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/notice-grid!findGradeReadByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/notice-grid!findReadByGrade.action` | 桌面端 | REDIRECT | — | empty |
| `edu/notice-grid!findReadByParent.action` | 桌面端 | REDIRECT | — | empty |
| `edu/notice-grid!findReadByStudent.action` | 桌面端 | REDIRECT | — | empty |
| `edu/parent!loadClassParent.action` | 桌面端+m2.html | REDIRECT | — | empty |
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
| `edu/physical-examination!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/school-term!getComboStore.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `edu/school-year!getComboStore.action` | 桌面端+m2.html | ALIVE | 1 | data, success |
| `edu/speciality!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/speciality!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/student!getActivityRecord.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/student!getComboStore.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `edu/student!getTreeByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `edu/student!loadClassStudent.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `edu/student!loadDormitoryStudent.action` | 桌面端 | ALIVE | 0 | json_list |
| `edu/student!readBasic.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `edu/student!verifyStudent.action` | 桌面端 | ALIVE | — | repeatList, studentIdList, notFoundList |
| `edu/teacher!getComboStore.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `edu/teacher!readSimple.action` | 桌面端+m2.html | REDIRECT | — | empty |

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
| `edu/match-awards!create.action` | 桌面端 |
| `edu/match-awards!destroy.action` | 桌面端 |
| `edu/match-awards!imp.action` | 桌面端 |
| `edu/match-awards!update.action` | 桌面端 |
| `edu/match-awards-detail!delteAttachment.action` | 桌面端 |
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

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `delete*`  `exportRealTable`  `findSchoolTimetableByAmOrPmAndItem`
    `getCampusGradeTree`  `getCampusGradeTree`  `getCampusGradeTreeByClassOrGradeTeacher`
    `getCampusTree`  `getClassmate`  `getComboStore`  `getComboStore`  `getComboStore`
    `getComboStore`  `getComboStore`  `getComboStore`  `getComboStore`  `getComboStore`
    `getComboStoreByClassTeacher`  `getComboStoreByClassTeacher`  `getComboStoreByGrade`
    `getComboStoreByGradeTeacher`  `getEntity`  `getGradeClassComboStoreBySubjectTeacher`
    `getGradeTreeByGradeTeacher`  `getGradeTreeByGradeTeacher`  `getGroupTree`  `getGroupTree`
    `getGroupTree`  `getGroupTree`  `getGroupTree`  `getGroupTreeByTeamLeader`
    `getLearnPhaseGradeTree`  `getNotVerifyComboStore`  `getSubstituteTeacher`  `getTable`
    `getTeacherListBySchoolTermClass`  `getTeacherTree`  `getTeacherWorkDayTotal`  `getTree`
    `getTree`  `getTreeByClassTeacher`  `init`  `input*`  `input*`  `inputByStudentOrParent*`
    `load`  `loadByStudent`  `read`  `read`  `read`  `readBaseByClassTeacher`
    `readBasicByClassId`  `readByClassTeacher`  `readByClassTeacher`  `readByClassTeacher`
    `readByGradeTeacher`  `readByGradeTeacher`  `readBySubmitter`  `readSimple`  `save*`
    `save*`  `save*`  `save*`  `saveByStudentOrParent*`  `search`  `update*`
    `updateByClassTeacher*`  `updateByClassTeacher*`  `updateByGradeTeacher*`
    `updateByGradeTeacher*`  `updater*`  `uploadPhotoByStudent*`
```
`*` 后缀 = 写类。共 72 个（读 55 / 写 17）。

### `community`（111）

**只读 62**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `community/attendance!action.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!buildMessageGridStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!generatedMessage.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!readAttendanceMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/attendance!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!exportByLeader.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getAllComboStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getComboStore.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getComboStoreByLeader.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getComboStoreByMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!getComboStoreByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!loadTree.action` | 桌面端 | REDIRECT | — | empty |
| `community/community!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/community!readByLeader.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!readByMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!readByRegister.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!readByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community!sendMessage.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/community-type!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/evaluate-item!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluate-item!getComboStoreByOwn.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluation!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluation!exportByLeader.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluation!initialization.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/evaluation!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/evaluation!readByLeader.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/exam-score!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/exam-score!stateByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/lesson!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/member!export.action` | 桌面端 | ERROR | — | — |
| `community/member!exportAllMember.action` | 桌面端 | ALIVE | — | text |
| `community/member!exportByMember.action` | 桌面端 | ALIVE | — | text |
| `community/member!exportMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!grouping.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!loadParentTree.action` | 桌面端 | REDIRECT | — | empty |
| `community/member!loadStudentTree.action` | 桌面端 | REDIRECT | — | empty |
| `community/member!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/member!register.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member!reportrAttendanceTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!exportByAll.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!readByAll.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/member-evaluate!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-evaluate!readByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/member-group!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `community/member-group!getComboStoreByOwn.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/notice!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/notice!read.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/notice!readByMember.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/notice-entity!read.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/property-borrow!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/property-borrow!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/property-borrow!read.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/property-borrow!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/reply!read.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `community/subject!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `community/work!download.action` | 桌面端 | ALIVE | — | text |
| `community/work!load.action` | 桌面端 | ALIVE | 0 | data, success, message |

**写类 49**（不封装）

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
| `community/member-evaluate!evaluate.action` | 桌面端 |
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

### `elective`（110）

**只读 58**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `elective/activity-record!downloadAttachment.action` | 桌面端 | ERROR | — | — |
| `elective/activity-record!downloadAttachmentByCourseTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/activity-record!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/activity-record!exportByCourseTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/activity-record!exportByTeacher.action` | 桌面端 | GONE | — | html |
| `elective/activity-record!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `elective/activity-record!readByCourseTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/activity-record!readByTeacher.action` | 桌面端 | GONE | — | html |
| `elective/activity-record!readByTeacherOrPresident.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/activity-record!reportRollBook.action` | 桌面端 | GONE | — | html |
| `elective/attendance!export.action` | 桌面端 | ERROR | — | — |
| `elective/attendance!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!exportByGradeTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/attendance!read.action` | 桌面端+m2.html | ALIVE | 1 | total, data, success |
| `elective/attendance!readByClassTeacher.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/attendance!readByGradeTeacher.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/attendance!readByStudentOrParent.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/attendance!readByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!export.action` | 桌面端 | REDIRECT | — | empty |
| `elective/course!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective/course!getComboStoreByElective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!getComboStoreByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!getComboStoreByTeacherOrPresident.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!loadTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/course!loadTreeByAdvance.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!loadTreeByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/course!readByStudentOrParent.action` | 桌面端+m2.html | ALIVE | — | success, refresh, message |
| `elective/elective!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective/elective!getComboStoreByAdvance.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStoreByClassTeacher.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStoreByGradeOrClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStoreByStudent.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/elective!getComboStoreByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective!getGradeClassTree.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/elective!getGradeClassTreeByClassTeacher.action` | 桌面端 | ALIVE | 0 | json_list |
| `elective/elective-result!elective.action` | 桌面端+m2.html | ALIVE | — | success, refresh, message |
| `elective/elective-result!export.action` | 桌面端 | REDIRECT | — | empty |
| `elective/elective-result!exportByAdvance.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!exportByClassTeacher.action` | 桌面端 | REDIRECT | — | empty |
| `elective/elective-result!exportByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!exportPacking.action` | 桌面端 | REDIRECT | — | empty |
| `elective/elective-result!initProcessGrade.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!read.action` | 桌面端 | REDIRECT | — | empty |
| `elective/elective-result!readByAdvance.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/elective-result!readByClassTeacher.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `elective/elective-result!readByTeacher.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `elective/elective-result!reportClassHourRegistration.action` | 桌面端 | ERROR | — | — |
| `elective/elective-result!reportClassHourRegistrationExcel.action` | 桌面端 | ERROR | — | — |
| `elective/elective-result!reportRollBook.action` | 桌面端 | ERROR | — | — |
| `elective/multiple-course!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-course!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `elective/multiple-course!getComboStoreByElective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-course!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-course-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/multiple-result!elective.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective/wish!getStudentWish.action` | 桌面端 | ALIVE | 0 | data, success, message |

**写类 38**（不封装）

| 端点 | 来源 |
|---|---|
| `elective/activity-record!create.action` | 桌面端 |
| `elective/activity-record!createByCourseTeacher.action` | 桌面端 |
| `elective/activity-record!createByTeacherOrPresident.action` | 桌面端 |
| `elective/activity-record!delteActivityPhotos.action` | 桌面端 |
| `elective/activity-record!destroy.action` | 桌面端 |
| `elective/activity-record!imp.action` | 桌面端 |
| `elective/activity-record!impByCourseTeacher.action` | 桌面端 |
| `elective/activity-record!update.action` | 桌面端 |
| `elective/activity-record!uploadActivityPhotos.action` | 桌面端 |
| `elective/attendance!create.action` | 桌面端 |
| `elective/attendance!destroy.action` | 桌面端 |
| `elective/attendance!imp.action` | 桌面端 |
| `elective/attendance!update.action` | 桌面端 |
| `elective/course!create.action` | 桌面端 |
| `elective/course!destroy.action` | 桌面端 |
| `elective/course!imp.action` | 桌面端 |
| `elective/course!update.action` | 桌面端 |
| `elective/course-detail!directSave.action` | 桌面端 |
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
| `elective/multiple-result!lockElective.action` | 桌面端 |
| `elective/wish!saveWish.action` | 桌面端 |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `delete*`  `delete*`  `getAll`  `getComboStoreByAdvance`
    `getComboStoreByStudentOrParent`  `getTree`  `getTreeByElective`  `load`  `load`  `read`
    `readByDeclare`  `save*`  `save*`
```
`*` 后缀 = 写类。共 14 个（读 9 / 写 5）。

### `archive`（89）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `academicDirectorApprovalComplete*`  `approve*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `completion`  `copy*`
    `delete*`  `delete*`  `delete*`  `deleteDraft*`  `detail`  `detail`  `getComboStore`
    `history`  `input*`  `input*`  `input*`  `input*`  `load`  `load`  `load`  `load`  `load`
    `modifyComplete*`  `modifyComplete*`  `modifyComplete*`  `modifyComplete*`
    `modifyComplete*`  `moralEducationApprovalComplete*`  `myOpen`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notifyComplete*`  `notifyComplete*`  `notifyComplete*`
    `notifyComplete*`  `notifyComplete*`  `read`  `read`  `read`  `read`  `readApproved`
    `readByParticipant`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByTeacher`  `readByTeacher`  `readByTeacher`  `readMine`  `readPending`  `release*`
    `researchGroupLeaderApprovalComplete*`  `researchGroupLeaderApprovalComplete*`
    `researchGroupLeaderApprovalComplete*`  `researchGroupLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `responsibleLeaderApprovalComplete*`
    `responsibleLeaderApprovalComplete*`  `returnRecord*`  `save*`  `save*`  `saveDraft*`
    `school`  `start*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `stat`  `statCreditHours`  `statCreditHoursByTeacher`  `submit*`
    `teacher`  `teacher`  `teacherDevelopmentCenterApprovalComplete*`
    `teacherDevelopmentCenterApprovalComplete*`  `teacherDevelopmentCenterApprovalComplete*`
    `teachingResearchOfficeApprovalComplete*`  `toDraft*`  `validate`  `withdraw*`
```
`*` 后缀 = 写类。共 89 个（读 32 / 写 57）。

### `fund`（88）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `approvedComplete*`  `approvedComplete*`  `approvedComplete*`  `approvedComplete*`
    `approvedComplete*`  `approvedComplete*`  `approvedNoticeComplete*`
    `approvedNoticeComplete*`  `contractAdministratorApprovalComplete*`  `delete*`  `delete*`
    `delete*`  `delete*`  `delete*`  `delete*`  `enterProcurementAgentInformationComplete*`
    `enterSupplierInformationComplete*`  `executivePrincipalApprovalComplete*`
    `executivePrincipalApprovalComplete*`  `executivePrincipalApprovalComplete*`
    `financialDirectorApprovalComplete*`  `financialDirectorApprovalComplete*`
    `financialDirectorApprovalComplete*`  `findApprovedItems`
    `getAcceptanceTreeByProcurementLeader`  `getTree`  `getTreeByProcurementLeader`
    `getTreeByProcurementLeader`  `getTreeByProcurementLeader`  `getYearTree`
    `legalPersonApprovalComplete*`  `load`  `load`  `load`  `load`  `load`  `load`
    `mainCampusPrincipalApprovalComplete*`  `mainCampusPrincipalApprovalComplete*`
    `memberApprovalComplete*`  `memberApprovalComplete*`  `memberProcurementCommentsComplete*`
    `modifyApplication*`  `modifyApplication*`  `modifyApplication*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `notApprovedComplete*`
    `notApprovedComplete*`  `notApprovedComplete*`  `peerApprovalComplete*`
    `procurementExecutionMethodApprovalComplete*`
    `procurementLeadingGroupLeaderApprovalComplete*`  `procurementSupervisorApprovalComplete*`
    `procurementSupervisorApprovalComplete*`  `projectLeaderApprovalComplete*`
    `projectLeaderApprovalComplete*`  `projectLeaderApprovalComplete*`  `read`
    `readByApplicant`  `readByApplicant`  `readByApplicant`  `readByApplicant`
    `readByApplicant`  `readByApplicant`  `readByContractReviewId`  `readByParticipate`
    `readByParticipate`  `readByParticipate`  `readByParticipate`  `readByParticipate`
    `readByProcurementExecutionId`  `readByProjectProcurementId`
    `recordProcurementOutcomeComplete*`  `report*`  `report*`  `report*`  `report*`  `report*`
    `settlementQuota*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`  `startWorkflow*`
    `startWorkflow*`  `startWorkflow*`  `unplannedStartWorkflow`
```
`*` 后缀 = 写类。共 88 个（读 29 / 写 59）。

### `account`（39）

**只读 11**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `account/dept!loadTreeByUser.action` | 桌面端 | REDIRECT | — | empty |
| `account/dept!loadUserTree.action` | 桌面端 | REDIRECT | — | empty |
| `account/user!calculateTotal.action` | 桌面端 | REDIRECT | — | empty |
| `account/user!getCustomUser.action` | 桌面端+m2.html | ALIVE | 0 | total |
| `account/user!readSimple.action` | 桌面端 | GONE | — | html |
| `account/user!readSimpleUser.action` | 桌面端 | REDIRECT | — | empty |
| `account/user!readSimpleUserAndTeacher.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `account/user!readStudentAndTeacherByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `account/user!readTeacherByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `account/user!simpleStatus.action` | m.html | ALIVE | — | success, loggedIn, principalSize |
| `account/user!status.action` | m2.html+m.html | ALIVE | — | success, loggedIn, principalSize |

**写类 4**（不封装）

| 端点 | 来源 |
|---|---|
| `account/dept!addUserDept.action` | 桌面端 |
| `account/dept!saveSelectedUser.action` | 桌面端 |
| `account/user!updateMobilePhone.action` | 桌面端 |
| `account/user!uploadUserPic.action` | 桌面端 |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `accessSituation`  `detail`  `forgotPassword*`  `getAccessStat`  `getCampusTree`
    `getComboStore`  `getComboStore`  `getMobilePhoneUser`  `getSharedOrOwnTree`
    `getUserComboStore`  `getUserNames`  `hongtuQrCode`  `input*`
    `inputStudentByClassTeacher*`  `inputStudentByParent*`  `load`  `readByContact`
    `readByStudentOrParent`  `resetPassword*`  `save*`  `updateFaceFile*`
    `updateFaceFileByClassTeacher*`  `updateStudentFaceFileByParent*`  `uploadUserPic*`
```
`*` 后缀 = 写类。共 24 个（读 14 / 写 10）。

### `message`（37）

**只读 19**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `message/category!getSubCategory.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |
| `message/message!html.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `message/message-grid!findReadByCategory.action` | 桌面端 | REDIRECT | — | empty |
| `message/message-grid!findReadByParent.action` | 桌面端 | REDIRECT | — | empty |
| `message/message-grid!findReadByStudent.action` | 桌面端 | REDIRECT | — | empty |
| `message/message-grid!readByCategory.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `message/message-type!getDisplay.action` | 桌面端 | ALIVE | 2 | json_list |
| `message/recipient!exportByShortMessage.action` | 桌面端 | REDIRECT | — | empty |
| `message/recipient!readByShortMessage.action` | 桌面端 | REDIRECT | — | empty |
| `message/recipient!readNotReply.action` | 桌面端 | REDIRECT | — | empty |
| `message/recipient!statInfo.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!compressDownloadHasReturned.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!exportHasReturned.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!exportOutbox.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!inbox.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!outbox.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!readDialog.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message!readHasReturned.action` | 桌面端 | REDIRECT | — | empty |
| `message/short-message-type!loadTree.action` | 桌面端 | REDIRECT | — | empty |

**写类 12**（不封装）

| 端点 | 来源 |
|---|---|
| `message/message-grid!setRead.action` | 桌面端 |
| `message/recipient!batchUpdateRead.action` | 桌面端+m2.html |
| `message/recipient!batchUpdateSign.action` | 桌面端 |
| `message/recipient!markAsUnread.action` | 桌面端 |
| `message/recipient!update.action` | 桌面端 |
| `message/short-message!destroy.action` | 桌面端+m2.html |
| `message/short-message!sendSms.action` | 桌面端 |
| `message/short-message!update.action` | 桌面端 |
| `message/short-message-detail!resend.action` | 桌面端 |
| `message/short-message-detail!send.action` | 桌面端 |
| `message/short-message-type!add.action` | 桌面端 |
| `message/short-message-type!remove.action` | 桌面端 |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `destroy*`  `getGrantedTree`  `input*`  `load`  `readByAuthor`  `save*`
```
`*` 后缀 = 写类。共 6 个（读 3 / 写 3）。

### `logistics`（34）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `accountingApprovalComplete*`  `approvedComplete*`  `batchSave*`
    `campusPrincipalApprovalComplete*`  `captcha`  `delete*`  `delete*`  `delete*`
    `getYearCampusTree`  `getYearCampusTree`  `identifyFundingSourcesComplete*`  `load`  `load`
    `load`  `notApprovedComplete*`  `principalApprovalComplete*`  `read`  `read`  `read`
    `readByApply`  `readByManager`  `readByManager`  `readByOperator`  `readByParticipate`
    `report*`  `report*`  `save*`  `save*`  `schoolFundsApprovalComplete*`  `startWorkflow*`
    `stat`  `statBfxx`  `superiorFundsApprovalComplete*`  `verify`
```
`*` 后缀 = 写类。共 34 个（读 17 / 写 17）。

### `office`（32）

**只读 4**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `office/calendar!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `office/calendar!gridDestroy.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `office/calendar!gridRead.action` | 桌面端 | ALIVE | 0 | total, data, success |
| `office/calendar!read.action` | 桌面端 | ALIVE | 0 | data, success, message |

**写类 6**（不封装）

| 端点 | 来源 |
|---|---|
| `office/calendar!create.action` | 桌面端 |
| `office/calendar!destroy.action` | 桌面端 |
| `office/calendar!gridCreate.action` | 桌面端 |
| `office/calendar!gridUpdate.action` | 桌面端 |
| `office/calendar!imp.action` | 桌面端 |
| `office/calendar!update.action` | 桌面端 |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `batchUpdateRead*`  `clickConfirm*`  `compressDownload`  `delete*`  `delete*`
    `exportFixedField`  `load`  `load`  `publishedStatus*`  `read`  `read`  `readAndload`
    `readByPublisher`  `readByTeacher`  `readByUser`  `readView`  `reportNotificationSignature`
    `save*`  `save*`  `save*`  `send`  `togglePublished`
```
`*` 后缀 = 写类。共 22 个（读 14 / 写 8）。

### `quality`（30）

**只读 16**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `quality/quality!downloadAttachment.action` | 桌面端 | ERROR | — | — |
| `quality/quality!export.action` | 桌面端 | REDIRECT | — | empty |
| `quality/quality!exportByAudit.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!exportByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!read.action` | 桌面端 | REDIRECT | — | empty |
| `quality/quality!readByAudit.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!readByClassTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-category!getAuditPersonNames.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-score-stat!export.action` | 桌面端 | ERROR | — | — |
| `quality/quality-score-stat!exportByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/quality-score-stat!read.action` | 桌面端 | ERROR | — | — |
| `quality/quality-score-stat!readByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `quality/student-description-detail!loadByStudentOrParnet.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |

**写类 14**（不封装）

| 端点 | 来源 |
|---|---|
| `quality/quality!create.action` | 桌面端 |
| `quality/quality!delteAttachment.action` | 桌面端 |
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
| `quality/student-description-detail!saveByStudentOrParnet.action` | 桌面端+m2.html |

### `dormitory`（29）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `dormitory/dormitory!getTreeByManager.action` | 桌面端 | ALIVE | 0 | data, success, message |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `approvedComplete*`  `batchSave*`  `classTeacherApprovalComplete*`  `delete*`  `delete*`
    `dormitoryManagementApprovalComplete*`  `getCampusItemCategoryTree`  `getComboStore`
    `getComboStore`  `getComboStore`  `getComboStore`  `getGroupTree`  `getGroupTreeByManager`
    `getStudentComboStoreByDormitoryId`  `getTreeNodeByManager`
    `gradeTeacherApprovalComplete*`  `load`  `load`  `notApprovedComplete*`  `noticeComplete*`
    `read`  `readByApplicant`  `readByDormitoryId`  `readByManager`  `readByOperator`
    `readByParticipate`  `readByStudentOrParent`  `startWorkflowJmzx*`
```
`*` 后缀 = 写类。共 28 个（读 18 / 写 10）。

### `purchase`（28）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `approvedComplete*`  `approvedNoticeComplete*`  `campusPrincipalApprovalComplete*`
    `collectionComplete*`  `comprehensiveServiceCenterApprovalComplete*`  `delete*`  `delete*`
    `deptLeaderApprovalComplete*`  `financialDirectorApprovalComplete*`
    `financialPrincipalApprovalComplete*`  `getStatGroupTree`  `getTree`
    `legalPersonApprovalComplete*`  `load`  `load`  `notApprovedComplete*`
    `provideApprovalFormApprovalComplete*`  `purchaseComplete*`  `readByApplicant`
    `readByParticipate`  `readByPurchaseRequest`  `readByPurchaseRequest`  `readByTeacher`
    `reimburseComplete*`  `report*`  `save*`  `startWorkflow*`  `stat`
```
`*` 后缀 = 写类。共 28 个（读 10 / 写 18）。

### `m3`（27）

**只读 11**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `/m3/message!list.action` | m.html | ALIVE | 1 | json_list |
| `m3/category.action` |  | — | — | — |
| `m3/recipient-detail.action` |  | — | — | — |
| `m3/shake-attendance/attendance-detail.action` |  | — | — | — |
| `m3/shake-attendance/daily-attendance-detail.action` |  | — | — | — |
| `m3/short-message-detail.action` |  | — | — | — |
| `m3/weixin/bind-user!checkBind.action` | m2.html+m.html | REDIRECT | — | empty |
| `m3/weixin/bind-user!existsWeixinUserId.action` | m2.html+m.html | ALIVE | — | text |
| `m3/weixin/login!getBindingUserList.action` | m2.html+m.html | ALIVE | 0 | data, success, message |
| `m3/weixin/login!loginSelectUser.action` | m2.html+m.html | ALIVE | — | success |
| `m3/weixin/login.action` |  | — | — | — |

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `m3/weixin/bind-user!bind.action` | m2.html+m.html |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `checkIp`  `checkIp`  `delete*`  `detail`  `getForward`  `getGroupTwoMenu`  `getMainMenu`
    `inbox`  `list`  `listTree`  `locationAttendance`  `outbox`  `send`  `sign*`
    `timePeriodAttendance`
```
`*` 后缀 = 写类。共 15 个（读 13 / 写 2）。

### `system`（26）

**只读 9**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `system/attachment!download.action` | 桌面端 | ALIVE | — | empty |
| `system/attachment!readByIds.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `system/attachment!rotate.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `system/attachment!send.action` | 桌面端+m2.html+m.html | ALIVE | — | empty |
| `system/attachment!toHtml.action` | 桌面端+m2.html | ALIVE | — | empty |
| `system/dict!getComboStore.action` | 桌面端+m2.html | REDIRECT | — | empty |
| `system/parameter!getParameterValue.action` | m2.html+m.html | ALIVE | — | text |
| `system/system!currentTime.action` | 桌面端+m2.html | ALIVE | — | text |
| `system/ueditor-plus.action` |  | — | — | — |

**写类 4**（不封装）

| 端点 | 来源 |
|---|---|
| `system/attachment!create.action` | 桌面端 |
| `system/attachment!destroy.action` | 桌面端 |
| `system/attachment!update.action` | 桌面端 |
| `system/attachment!upload.action` | 桌面端 |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `compressDownload`  `download`  `getCampusTree`  `getComboStore`  `getComboStoreCacheable`
    `getElectiveTreeByAuthorized`  `getElectiveTreeByManager`  `getGroupTree`  `log`
    `openDoor*`  `securityUpload`  `send`  `upload*`
```
`*` 后缀 = 写类。共 13 个（读 11 / 写 2）。

### `moral`（26）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `moral/student-check!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `delete*`  `getBasicInfo`  `getEntity`  `getEntity`  `getEntity`  `load`  `load`
    `load`  `load`  `read`  `read`  `read`  `read`  `readByClassTeacher`  `readByGradeTeacher`
    `readByParticipate`  `readByRegister`  `readBySubmitter`  `readBySubmitter`
    `readByTeacher`  `save*`  `save*`  `save*`  `save*`
```
`*` 后缀 = 写类。共 25 个（读 19 / 写 6）。

### `teaching-research`（23）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `approvedComplete*`  `approvedComplete*`  `delete*`  `delete*`  `load`  `load`
    `notApprovedComplete*`  `notApprovedComplete*`  `noticeComplete*`  `noticeComplete*`
    `read`  `read`  `read`  `readByParticipate`  `readByParticipate`  `readByTeacher`
    `readByTeacher`  `readByTeacher`  `save*`  `startWorkflow*`  `startWorkflow*`
    `teachingResearchGroupLeaderApprovalComplete*`
    `teachingResearchGroupLeaderApprovalComplete*`
```
`*` 后缀 = 写类。共 23 个（读 10 / 写 13）。

### `print`（23）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `academicDirectorApprovalComplete*`  `acceptanceComplete*`  `approvedComplete*`
    `completedComplete*`  `delete*`  `delete*`  `deptLeaderApprovalComplete*`
    `generalAffairsApprovalComplete*`  `getComboStore`  `input*`  `load`
    `notApprovedComplete*`  `printClerkApprovalComplete*`  `read`  `readByApplicant`
    `readByApplication`  `readByParticipate`  `researchGroupLeaderApprovalComplete*`  `save*`
    `startWorkflow*`  `startWorkflowByCjkjxx*`  `startWorkflowByYfzx*`  `startWorkflowByYs*`
```
`*` 后缀 = 写类。共 23 个（读 6 / 写 17）。

### `student-attendance`（22）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `checkRegister`  `delete*`  `delete*`  `getComboStore`  `getComboStore`
    `getRegisterOptions`  `load`  `load`  `read`  `read`  `readByClassIdAndDate`
    `readByClassTeacher`  `readByClassTeacher`  `readByGradeTeacher`  `readByGradeTeacher`
    `readByLeaderDept`  `readByRegister`  `readByStudentOrParent`  `readUnregistered`
    `readUnregisteredByGradeTeacher`  `save*`  `saveRegister*`
```
`*` 后缀 = 写类。共 22 个（读 18 / 写 4）。

### `holistic-education`（21）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `allStudentScore`  `classRankingStat`  `delete*`  `domainStat`  `getComboStore`  `getTree`
    `read`  `read`  `readByClassTeacher`  `readByGradeTeacher`  `readByStudentId`
    `readByStudentOrParent`  `readByUser`  `save*`  `scoreSummaryStat`  `studentRankingStat`
    `studentScoreStatByStudentId`  `studentScoreStatByStudentOrParent`
    `surpassStatByStudentId`  `surpassStatByStudentOrParent`  `teacherRankingStat`
```
`*` 后缀 = 写类。共 21 个（读 19 / 写 2）。

### `shake-attendance`（19）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `delete*`  `findNotAttendance`  `getAttendancePosition`  `getComboStore`
    `getComboStore`  `getDailyAttendanceOverallTable`  `getMyMonthStat`  `getUserTimePeriod`
    `input*`  `managementUsers`  `manuallyLeave*`  `manuallySign*`  `permissions`  `read`
    `read`  `readByUser`  `save*`  `update*`
```
`*` 后缀 = 写类。共 19 个（读 12 / 写 7）。

### `volunteer`（19）

**只读 10**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `volunteer/activity!readBySign.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity-registration!exportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity-registration!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity-registration!registration.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity-registration!unregistration.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/activity2!readByRegistration.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/aimunc-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/nhsdlc-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/survey-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `volunteer/volunteer-registration-detail!load.action` | 桌面端 | ALIVE | 0 | data, success, message |

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

### `award`（18）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `academicDirectorApprovalComplete*`  `delete*`  `delete*`  `getTree`  `input*`  `load`
    `load`  `moralEducationApprovalComplete*`  `read`  `readByAdvisor`  `readByClassTeacher`
    `readByGradeTeacher`  `readByParticipate`  `readByRegister`  `readByTeacher`
    `researchGroupLeaderApprovalComplete*`  `save*`  `startWorkflow*`
```
`*` 后缀 = 写类。共 18 个（读 10 / 写 8）。

### `supervision`（18）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `campusSupervisorSummaryComplete*`  `complete*`  `delete*`  `delete*`  `getTree`
    `groupSupervisorReviewComplete*`  `indicatorFeedbackComplete*`  `load`  `load`  `read`
    `read`  `read`  `readByFeedbackPerson`  `readByParticipate`  `readByResponsiblePerson`
    `readByUser`  `selectFeedbackPersonnelComplete*`  `startWorkflow*`
```
`*` 后缀 = 写类。共 18 个（读 10 / 写 8）。

### `health`（17）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `compressDownload`  `delete*`  `getSubmittedDateList`  `getSubmittedStudentIdList`
    `getTeacherSubmitStatus`  `list`  `listByClassId`  `load`  `load`  `load`
    `loadLastCohabitant`  `read`  `readByCreator`  `reminderUnsubmittedStudent`
    `reminderUnsubmittedTeacher`  `save*`  `save*`
```
`*` 后缀 = 写类。共 17 个（读 14 / 写 3）。

### `venue`（17）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `adminEvaluationComplete*`  `approvedComplete*`  `calendar`  `delete*`
    `evaluationFeedbackComplete*`  `getAllowApplicationTree`  `getManagerOrServiceTree`
    `getTree`  `load`  `managerApprovalComplete*`  `notApprovedComplete*`
    `notifyNoticeComplete*`  `readByApplicant`  `readByParticipate`  `serviceNoticeComplete*`
    `startWorkflow*`  `usageFeedbackComplete*`
```
`*` 后缀 = 写类。共 17 个（读 7 / 写 10）。

### `yfzx`（16）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `cancelRegistration*`  `captcha`  `forgotPassword*`  `formalRegistration`  `getComboStore`
    `getRecruitStudentComboStore`  `load`  `load`  `login`  `login`  `logout`  `logout`
    `register`  `report*`  `save*`  `save*`
```
`*` 后缀 = 写类。共 16 个（读 11 / 写 5）。

### `junior-quality`（14）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `batchUpdatePeerReviewer*`  `circularPeerReviewer*`  `getStudentGroupByGroupLeader`
    `getStudentTreeByClassId`  `getTreeByClassTeacher`  `getTreeByStudent`
    `getTreeByStudentId`  `getTreeByStudentOrParent`  `initializtion`  `listByClass`
    `overallQualityEvaluationByStudent`  `prepareOverallQualityEvaluationDownload`
    `saveSelfScore*`  `update*`
```
`*` 后缀 = 写类。共 14 个（读 10 / 写 4）。

### `visitor`（14）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `appointment`  `captcha`  `delete*`  `detail`  `historyInterviewee`  `intervieweeApproval*`
    `load`  `registration`  `resultQuery`  `resultQueryByOpenId`  `securityOfficeApproval*`
    `securityOfficeDirectorApproval*`  `verifyUser`  `visitNotice`
```
`*` 后缀 = 写类。共 14 个（读 10 / 写 4）。

### `warehouse`（14）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `approvedComplete*`  `delete*`  `deptLeaderApprovalComplete*`
    `generalAffairsApprovalComplete*`  `getComboStore`  `load`  `notApprovedComplete*`
    `noticeComplete*`  `read`  `readByParticipate`  `readByUser`  `startWorkflow*`
    `startWorkflowByYfzx*`  `warehouseManagerApprovalComplete*`
```
`*` 后缀 = 写类。共 14 个（读 5 / 写 9）。

### `service`（13）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `getFeedbackAndWord`  `getStateComboStore`  `getTree`  `load`  `read`
    `readByApplicant`  `readByServiceUnit`  `responseComplete*`  `serviceComplete*`
    `serviceCompletedComplete*`  `serviceCompletedNoticeComplete*`  `startWorkflow*`
```
`*` 后缀 = 写类。共 13 个（读 7 / 写 6）。

### `evaluation`（13）

**只读 4**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `evaluation/evaluation!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `evaluation/evaluation!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-item!getEvaluationForm.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `evaluation/evaluation-result!evaluation.action` | 桌面端+m2.html | ALIVE | 0 | data, success, message |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getEvaluationVantForm`  `getTree`  `getTreeByStudent`  `readEvaluationStudent`
    `readEvaluationStudentByClassTeacher`  `readEvaluationStudentByGradeTeacher`
    `studentEvaluationStat`  `studentEvaluationStatByClassTeacher`
    `studentEvaluationStatByGradeTeacher`
```
`*` 后缀 = 写类。共 9 个（读 9 / 写 0）。

### `psychological`（13）

**只读 7**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `psychological/appointment!export.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `psychological/appointment!read.action` | 桌面端 | ALIVE | 1 | total, data, success |
| `psychological/appointment!readByRequest.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `psychological/appointment!readByTeacher.action` | 桌面端 | ALIVE | 0 | data, success, message |
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

### `duty`（12）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `getOnDutyArrangeTable`  `load`  `load`  `read`  `read`  `readByDutyOfficer`
    `readByTeacher`  `save*`  `save*`  `signIn*`  `signOut*`
```
`*` 后缀 = 写类。共 12 个（读 7 / 写 5）。

### `select-subject`（12）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `confirm*`  `getCombinationComboStore`  `getComboStore`  `getComboStoreByStudentOrParent`
    `loadId`  `read`  `read`  `readByClassTeacher`  `readByClassTeacher`  `report*`  `save*`
    `saveById*`
```
`*` 后缀 = 写类。共 12 个（读 8 / 写 4）。

### `experimental-class`（11）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `captcha`  `forgotPassword*`  `getRecruitStudentComboStore`  `load`  `login`  `logout`
    `register`  `report*`  `save*`  `updateReadNotice*`  `updateReadQa*`
```
`*` 后缀 = 写类。共 11 个（读 6 / 写 5）。

### `class-evaluation`（11）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `getCampusItemCategoryTree`  `load`  `read`  `readByClassTeacher`
    `readByOperator`  `readByStudentOrParent`  `save*`  `saveEvaluationItemClass*`
    `saveEvaluationItemScoreTree*`  `statScore`
```
`*` 后缀 = 写类。共 11 个（读 7 / 写 4）。

### `school-sports-day`（11）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `cancelSubmission*`  `findClassGroup`  `getClassComboStore`  `getComboStore`
    `getComboStore`  `getSubmissionStatus`  `read`  `registrationByGroupItme`
    `registrationByStudent`  `registrationValidate`  `submission`
```
`*` 后缀 = 写类。共 11 个（读 10 / 写 1）。

### `experiment`（10）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `approvedComplete*`  `delete*`  `laboratoryAssistantApprovalComplete*`
    `laboratoryLeadersApprovalComplete*`  `load`  `notApprovedComplete*`  `readByExperimental`
    `readByExperimental`  `readByParticipate`  `readByUser`
```
`*` 后缀 = 写类。共 10 个（读 5 / 写 5）。

### `jmzx`（10）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getRecruitComboStore`  `getTeacherRecruitComboStore`  `load`  `load`  `login`  `login`
    `logout`  `logout`  `save*`  `save*`
```
`*` 后缀 = 写类。共 10 个（读 8 / 写 2）。

### `cjtcs`（9）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `autograph*`  `getRecruitStudentComboStore`  `load`  `login`  `logout`  `report*`
    `reportAdmissionTicket`  `save*`  `uploadIdPhoto*`
```
`*` 后缀 = 写类。共 9 个（读 5 / 写 4）。

### `evening-study`（9）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `attendanceSituation`  `completeRegistration*`  `getComboStore`  `getTable`
    `readByEveningStudyInspectionId`  `readByGradeTeacher`  `readByTeacher`  `readByTeacher`
    `update*`
```
`*` 后缀 = 写类。共 9 个（读 7 / 写 2）。

### `yztcs`（9）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `autograph*`  `getRecruitStudentComboStore`  `load`  `login`  `logout`  `material`
    `report*`  `reportAdmissionTicket`  `save*`
```
`*` 后缀 = 写类。共 9 个（读 6 / 写 3）。

### `exam`（9）

**只读 6**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `exam/answer!statByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/online-exam!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `exam/online-exam!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/question!readByExam.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/question!result.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `exam/question-bank!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |

**写类 3**（不封装）

| 端点 | 来源 |
|---|---|
| `exam/answer!emptyByStudent.action` | 桌面端 |
| `exam/answer!saveAnswer.action` | 桌面端 |
| `exam/question!destroy.action` | 桌面端 |

### `tour-class`（9）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `getComboStore`  `load`  `read`  `readByClassTeacher`  `readByTeacher`
    `readByTourClassTeacher`  `save*`  `saveMultiple*`
```
`*` 后缀 = 写类。共 9 个（读 6 / 写 3）。

### `civilization-office`（8）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `checkResultsStat`  `checked`  `getCheckItemGroupTree`  `getSchoolYearGroupTree`  `read`
    `readCheckRecord`  `readNotChecked`  `saveCheckRegistration*`
```
`*` 后缀 = 写类。共 8 个（读 7 / 写 1）。

### `hcsytcs`（8）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `autograph*`  `getRecruitStudentComboStore`  `load`  `login`  `logout`  `report*`
    `reportAdmissionTicket`  `save*`
```
`*` 后缀 = 写类。共 8 个（读 5 / 写 3）。

### `jmzxtcs`（8）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `autograph*`  `getRecruitStudentComboStore`  `load`  `login`  `logout`  `report*`
    `reportAdmissionTicket`  `save*`
```
`*` 后缀 = 写类。共 8 个（读 5 / 写 3）。

### `alumni-card`（8）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `detail`  `getMessages`  `getMyCard`  `load`  `loadTask`  `readMy`  `save*`  `verify`
```
`*` 后缀 = 写类。共 8 个（读 7 / 写 1）。

### `note`（8）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `delete*`  `likeNote`  `load`  `read`  `readByUser`  `save*`  `save*`
```
`*` 后缀 = 写类。共 8 个（读 4 / 写 4）。

### `xmyz`（8）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `captcha`  `forgotPassword*`  `getComboStore`  `load`  `login`  `logout`  `register`
    `save*`
```
`*` 后缀 = 写类。共 8 个（读 6 / 写 2）。

### `alumnus`（7）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `captcha`  `detail`  `findAlumnus`  `getClassAlumnusList`  `getClassDetail`
    `loadGradeClassTree`  `save*`
```
`*` 后缀 = 写类。共 7 个（读 6 / 写 1）。

### `student-ordering`（7）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `cancelOrder*`  `cancelOrder*`  `findCancelOrder`  `findOrderFood`  `getTree`  `order`
    `removeCancelOrder*`
```
`*` 后缀 = 写类。共 7 个（读 4 / 写 3）。

### `yhzs`（6）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getRecruitStudentComboStore`  `load`  `login`  `logout`  `report*`  `save*`
```
`*` 后缀 = 写类。共 6 个（读 4 / 写 2）。

### `base`（6）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `getTree`  `getTree`  `load`  `read`  `save*`
```
`*` 后缀 = 写类。共 6 个（读 4 / 写 2）。

### `enroll`（6）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getGradeGroupTree`  `getRecruitStudentComboStore`  `load`  `login`  `logout`  `save*`
```
`*` 后缀 = 写类。共 6 个（读 5 / 写 1）。

### `face`（6）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `load`  `load`  `read`  `readByOperator`  `save*`
```
`*` 后缀 = 写类。共 6 个（读 4 / 写 2）。

### `homework-announcement`（6）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `getEntity`  `load`  `load`  `readByTeamLeader`  `save*`
```
`*` 后缀 = 写类。共 6 个（读 4 / 写 2）。

### `library`（6）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `borrow*`  `confirmReturnJournal*`  `readBorrowed`  `readReturning`  `returnJournal*`
    `search`
```
`*` 后缀 = 写类。共 6 个（读 3 / 写 3）。

### `score`（6）

**只读 6**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `score/score!exportParentScoreTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!exportStudentScoreTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!getStudentOrParentScoreAnalysisOption.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!getSubjectAndTotalScoreTypeTreeByStudentOrPanel.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!readParentScoreTable.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `score/score!readStudentScoreTable.action` | 桌面端 | ALIVE | 0 | data, success, message |

### `transcript`（6）

**只读 6**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `transcript/transcript!getTranscriptByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!getTranscriptByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!readByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!readByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!transcriptExportByParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `transcript/transcript!transcriptExportByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |

### `recruit`（5）

**只读 2**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `recruit/admission-school.action` |  | — | — | — |
| `recruit/physical-examination-form-detail.action` |  | — | — | — |

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `auditResults`  `auditResults`  `getWishSchoolComboStore`
```
`*` 后缀 = 写类。共 3 个（读 3 / 写 0）。

### `school-assets`（5）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `checkAssetNumberRepeat`  `delete*`  `load`  `read`  `save*`
```
`*` 后缀 = 写类。共 5 个（读 3 / 写 2）。

### `share`（5）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getHistoryHousePropertyJsonByObligee`  `getHousePropertyCertificateNumber`
    `getHousePropertyDetail`  `getHousePropertyJsonByObligee`  `getHouseholdRegistration`
```
`*` 后缀 = 写类。共 5 个（读 5 / 写 0）。

### `work-card`（5）

**只读 4**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `work-card/work!getWorkCardRecordWork.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `work-card/work-card!getComboStore.action` | 桌面端 | ALIVE | 1 | data, success |
| `work-card/work-card!getComboStoreByStudentOrParent.action` | 桌面端 | ALIVE | 0 | data, success, message |
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
| `elective-evaluation/elective-evaluation!getComboStoreByStudent.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `elective-evaluation/evaluation-feedback-detail!load.action` | 桌面端 | ALIVE | — | success, message |

**写类 1**（不封装）

| 端点 | 来源 |
|---|---|
| `elective-evaluation/evaluation-feedback-detail!save.action` | 桌面端 |

### `security`（4）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `read`  `save*`  `save*`
```
`*` 后缀 = 写类。共 4 个（读 1 / 写 3）。

### `zz`（4）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `detail`  `getArchive`  `getGroupTree`  `score`
```
`*` 后缀 = 写类。共 4 个（读 4 / 写 0）。

### `form`（3）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `captcha`  `load`  `loadGrade`
```
`*` 后缀 = 写类。共 3 个（读 3 / 写 0）。

### `admin-evaluation`（3）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `evaluation`  `getEvaluationJson`  `getSchoolTermTreeByEvaluation`
```
`*` 后缀 = 写类。共 3 个（读 3 / 写 0）。

### `general-affairs`（3）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `read`  `save*`
```
`*` 后缀 = 写类。共 3 个（读 1 / 写 2）。

### `visitor-grid`（3）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `enterSchool*`  `leaveSchool*`  `list`
```
`*` 后缀 = 写类。共 3 个（读 1 / 写 2）。

### `visitor2022`（3）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`  `readByInterviewee`  `readByParticipate`
```
`*` 后缀 = 写类。共 3 个（读 2 / 写 1）。

### `vote`（3）

**只读 3**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `vote/question!getForm.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `vote/question!getStudentHomePageForm.action` | 桌面端 | ALIVE | 0 | data, success, message |
| `vote/result!vote.action` | 桌面端 | ALIVE | 0 | data, success, message |

### `development-evaluation`（2）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getTree`  `readByTeacher`
```
`*` 后缀 = 写类。共 2 个（读 2 / 写 0）。

### `property`（2）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getBorrowedBySchoolPropertyDeptGroup`  `input*`
```
`*` 后缀 = 写类。共 2 个（读 1 / 写 1）。

### `weixin`（2）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `getJsapiSignature`  `getOpenId`
```
`*` 后缀 = 写类。共 2 个（读 2 / 写 0）。

### `-detail`（1）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `delete*`
```
`*` 后缀 = 写类。共 1 个（读 0 / 写 1）。

### `2024`（1）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `viewPdf`
```
`*` 后缀 = 写类。共 1 个（读 1 / 写 0）。

### `online-exam`（1）

**只读 1**

| 端点 | 来源 | 实测 | 行数 | 顶层字段 |
|---|---|---|---|---|
| `online-exam/exam-situation!readAllExamSituation.action` | 桌面端 | ALIVE | 0 | data, success, message |

### `specialty`（1）

m2 专属（新版 bundle 静态提取，能力面以运行时权限为准）：

```
m2: `load`
```
`*` 后缀 = 写类。共 1 个（读 1 / 写 0）。

## 机器可读

- `endpoints.json` — 全部 2623 个端点，含 `sources` / `kind` / `menus` / `files`
- `validation.json` — 1176 个只读端点的实测响应结构
- `menu_tree.json` — 菜单树原始响应（130 节点）
- `desktop_endpoints.json` — 489 个桌面端端点，含来源 jsFile 与所属菜单名

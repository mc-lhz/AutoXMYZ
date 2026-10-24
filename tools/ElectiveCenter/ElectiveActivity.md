# ElectiveActivity — 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

⚠️ GONE（2026-10-24 冒烟实测 404）：`readByTeacher` / `exportByTeacher`
两个教师向路由已下线（服务端 404 页面），调用会得到
`{"success": false, "_status: 404"}`——教师账号也不可用，属于注册表中
16 条 GONE 之列。

| 方法 | 端点 | HTTP |
|---|---|---|
| `createActivityRecord` | `elective/activity-record!create.action` | POST |
| `createByCourseTeacherActivityRecord` | `elective/activity-record!createByCourseTeacher.action` | POST |
| `createByTeacherOrPresidentActivityRecord` | `elective/activity-record!createByTeacherOrPresident.action` | POST |
| `delteActivityPhotosActivityRecord` | `elective/activity-record!delteActivityPhotos.action` | POST |
| `destroyActivityRecord` | `elective/activity-record!destroy.action` | POST |
| `downloadAttachmentActivityRecord` | `elective/activity-record!downloadAttachment.action` | GET |
| `downloadAttachmentByCourseTeacherActivityRecord` | `elective/activity-record!downloadAttachmentByCourseTeacher.action` | GET |
| `exportActivityRecord` | `elective/activity-record!export.action` | GET |
| `exportActivityRecordByCourseTeacher` | `elective/activity-record!exportByCourseTeacher.action` | GET |
| `exportActivityRecordByTeacher` | `elective/activity-record!exportByTeacher.action` | GET |
| `importActivityRecord` | `elective/activity-record!imp.action` | POST |
| `impByCourseTeacherActivityRecord` | `elective/activity-record!impByCourseTeacher.action` | POST |
| `readActivityRecord` | `elective/activity-record!read.action` | GET |
| `readActivityRecordByCourseTeacher` | `elective/activity-record!readByCourseTeacher.action` | GET |
| `readActivityRecordByTeacher` | `elective/activity-record!readByTeacher.action` | GET |
| `readActivityRecordByTeacherOrPresident` | `elective/activity-record!readByTeacherOrPresident.action` | GET |
| `reportRollBookActivityRecord` | `elective/activity-record!reportRollBook.action` | POST |
| `updateActivityRecord` | `elective/activity-record!update.action` | POST |
| `uploadActivityPhotosActivityRecord` | `elective/activity-record!uploadActivityPhotos.action` | POST |

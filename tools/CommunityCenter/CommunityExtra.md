# CommunityExtra — 社团补齐：考试成绩查看、报名、出勤、课程下拉

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `exportElectiveAttendance` | `community/attendance!exportByStudent.action` | GET |
| `readCommunityByRegister` | `community/community!readByRegister.action` | GET |
| `exportCommunityExamScore` | `community/exam-score!exportByStudent.action` | GET |
| `importCommunityExamScore` | `community/exam-score!imp.action` | POST |
| `stateByStudentCommunityExamScore` | `community/exam-score!stateByStudent.action` | GET |
| `getComboStoreLesson` | `community/lesson!getComboStore.action` | GET |

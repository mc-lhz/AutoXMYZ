# ElectiveAttendance — 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `createElectiveAttendance` | `elective/attendance!create.action` | POST |
| `destroyElectiveAttendance` | `elective/attendance!destroy.action` | POST |
| `exportElectiveAttendance` | `elective/attendance!export.action` | GET |
| `exportElectiveAttendanceByClassTeacher` | `elective/attendance!exportByClassTeacher.action` | GET |
| `exportElectiveAttendanceByGradeTeacher` | `elective/attendance!exportByGradeTeacher.action` | GET |
| `exportElectiveAttendanceByStudentOrParent` | `elective/attendance!exportByStudentOrParent.action` | GET |
| `exportElectiveAttendanceByTeacher` | `elective/attendance!exportByTeacher.action` | GET |
| `importElectiveAttendance` | `elective/attendance!imp.action` | POST |
| `readElectiveAttendance` | `elective/attendance!read.action` | GET |
| `readElectiveAttendanceByClassTeacher` | `elective/attendance!readByClassTeacher.action` | GET |
| `readElectiveAttendanceByGradeTeacher` | `elective/attendance!readByGradeTeacher.action` | GET |
| `readElectiveAttendanceByStudentOrParent` | `elective/attendance!readByStudentOrParent.action` | GET |
| `readElectiveAttendanceByTeacher` | `elective/attendance!readByTeacher.action` | GET |
| `updateElectiveAttendance` | `elective/attendance!update.action` | POST |

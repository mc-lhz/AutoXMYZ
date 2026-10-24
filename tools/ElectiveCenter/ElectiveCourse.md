# ElectiveCourse — 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `createElectiveCourse` | `elective/course!create.action` | POST |
| `destroyElectiveCourse` | `elective/course!destroy.action` | POST |
| `exportElectiveCourse` | `elective/course!export.action` | GET |
| `getComboStoreByElectiveElectiveCourse` | `elective/course!getComboStoreByElective.action` | GET |
| `getComboStoreByTeacherElectiveCourse` | `elective/course!getComboStoreByTeacher.action` | GET |
| `getComboStoreByTeacherOrPresidentElectiveCourse` | `elective/course!getComboStoreByTeacherOrPresident.action` | GET |
| `importElectiveCourse` | `elective/course!imp.action` | POST |
| `loadTreeElectiveCourse` | `elective/course!loadTree.action` | GET |
| `loadTreeByAdvanceElectiveCourse` | `elective/course!loadTreeByAdvance.action` | GET |
| `loadTreeByTeacherElectiveCourse` | `elective/course!loadTreeByTeacher.action` | GET |
| `readElectiveCourseByStudentOrParent` | `elective/course!readByStudentOrParent.action` | GET |
| `updateElectiveCourse` | `elective/course!update.action` | POST |
| `directSaveElectiveCourseDetail` | `elective/course-detail!directSave.action` | POST |
| `getComboStoreElective` | `elective/elective!getComboStore.action` | GET |
| `getComboStoreByAdvanceElective` | `elective/elective!getComboStoreByAdvance.action` | GET |
| `getComboStoreByClassTeacherElective` | `elective/elective!getComboStoreByClassTeacher.action` | GET |
| `getComboStoreByGradeOrClassTeacherElective` | `elective/elective!getComboStoreByGradeOrClassTeacher.action` | GET |
| `getComboStoreByStudentElective` | `elective/elective!getComboStoreByStudent.action` | GET |
| `getComboStoreByTeacherElective` | `elective/elective!getComboStoreByTeacher.action` | GET |
| `getGradeClassTreeElective` | `elective/elective!getGradeClassTree.action` | GET |
| `getGradeClassTreeByClassTeacherElective` | `elective/elective!getGradeClassTreeByClassTeacher.action` | GET |
| `getStudentWishWish` | `elective/wish!getStudentWish.action` | GET |
| `saveWishWish` | `elective/wish!saveWish.action` | POST |

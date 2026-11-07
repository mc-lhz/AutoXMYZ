# ElectiveResult — 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `batchAddElectiveResult` | `elective/elective-result!batchAdd.action` | POST |
| `batchPackingExportElectiveResult` | `elective/elective-result!batchPackingExport.action` | POST |
| `createElectiveResult` | `elective/elective-result!create.action` | POST |
| `createByAdvanceElectiveResult` | `elective/elective-result!createByAdvance.action` | POST |
| `destroyElectiveResult` | `elective/elective-result!destroy.action` | POST |
| `destroyByAdvanceElectiveResult` | `elective/elective-result!destroyByAdvance.action` | POST |
| `destroyByClassTeacherElectiveResult` | `elective/elective-result!destroyByClassTeacher.action` | POST |
| `electiveElectiveResult` | `elective/elective-result!elective.action` | POST |
| `exportElectiveResult` | `elective/elective-result!export.action` | GET |
| `exportElectiveResultByAdvance` | `elective/elective-result!exportByAdvance.action` | GET |
| `exportElectiveResultByClassTeacher` | `elective/elective-result!exportByClassTeacher.action` | GET |
| `exportElectiveResultByTeacher` | `elective/elective-result!exportByTeacher.action` | GET |
| `exportPackingElectiveResult` | `elective/elective-result!exportPacking.action` | GET |
| `importElectiveResult` | `elective/elective-result!imp.action` | POST |
| `initProcessGradeElectiveResult` | `elective/elective-result!initProcessGrade.action` | POST |
| `readElectiveResultByAdvance` | `elective/elective-result!readByAdvance.action` | GET |
| `readElectiveResultByClassTeacher` | `elective/elective-result!readByClassTeacher.action` | GET |
| `readElectiveResultByTeacher` | `elective/elective-result!readByTeacher.action` | GET |
| `reportClassHourRegistrationElectiveResult` | `elective/elective-result!reportClassHourRegistration.action` | POST |
| `reportClassHourRegistrationExcelElectiveResult` | `elective/elective-result!reportClassHourRegistrationExcel.action` | POST |
| `reportRollBookElectiveResult` | `elective/elective-result!reportRollBook.action` | POST |
| `updateElectiveResult` | `elective/elective-result!update.action` | POST |
| `updateByAdvanceElectiveResult` | `elective/elective-result!updateByAdvance.action` | POST |
| `updateByClassTeacherElectiveResult` | `elective/elective-result!updateByClassTeacher.action` | POST |
| `updateByTeacherElectiveResult` | `elective/elective-result!updateByTeacher.action` | POST |
| `createMultipleCourse` | `elective/multiple-course!create.action` | POST |
| `destroyMultipleCourse` | `elective/multiple-course!destroy.action` | POST |
| `exportMultipleCourse` | `elective/multiple-course!export.action` | GET |
| `getComboStoreByElectiveMultipleCourse` | `elective/multiple-course!getComboStoreByElective.action` | GET |
| `importMultipleCourse` | `elective/multiple-course!imp.action` | POST |
| `readMultipleCourse` | `elective/multiple-course!readByStudent.action` | GET |
| `updateMultipleCourse` | `elective/multiple-course!update.action` | POST |
| `loadMultipleCourseDetail` | `elective/multiple-course-detail!load.action` | GET |
| `cancelElectiveMultipleResult` | `elective/multiple-result!cancelElective.action` | POST |
| `electiveMultipleResult` | `elective/multiple-result!elective.action` | POST |
| `lockElectiveMultipleResult` | `elective/multiple-result!lockElective.action` | POST |

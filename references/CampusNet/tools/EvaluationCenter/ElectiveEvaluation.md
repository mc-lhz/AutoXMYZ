# ElectiveEvaluation — 教师评测反馈 + 校本课程评测

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `getComboStoreElectiveEvaluation` | `elective-evaluation/elective-evaluation!getComboStore.action` | GET |
| `getComboStoreByStudentElectiveEvaluation` | `elective-evaluation/elective-evaluation!getComboStoreByStudent.action` | GET |
| `loadElectiveEvaluationFeedback` | `elective-evaluation/evaluation-feedback-detail!load.action` | GET |
| `saveElectiveEvaluationFeedback` | `elective-evaluation/evaluation-feedback-detail!save.action` | POST |

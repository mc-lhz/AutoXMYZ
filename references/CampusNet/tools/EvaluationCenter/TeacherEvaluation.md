# TeacherEvaluation — 教师评测反馈 + 校本课程评测

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `getComboStoreTeacherEvaluation` | `evaluation/evaluation!getComboStore.action` | GET |
| `getComboStoreByStudentTeacherEvaluation` | `evaluation/evaluation!getComboStoreByStudent.action` | GET |
| `getEvaluationFormEvaluationItem` | `evaluation/evaluation-item!getEvaluationForm.action` | GET |
| `evaluationEvaluationResult` | `evaluation/evaluation-result!evaluation.action` | POST |

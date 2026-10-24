# ExamPractice — 会考练习 / 在线考试

菜单：《会考练习》/考试 与 《在线考试》/我的考试。信息技术会考的练习/答题/统计。

## 方法

| 方法 | 端点 | 写 | 说明 |
|---|---|---|---|
| `getMyOnlineExamCombo()` | `exam/online-exam!getComboStoreByStudent` | | 我的考试下拉 |
| `getOnlineExamCombo(**kw)` | `exam/online-exam!getComboStore` | | 全量下拉，可传 examId 过滤 |
| `getQuestionBankCombo(**kw)` | `exam/question-bank!getComboStore` | | 题库下拉，可传 examId 过滤 |
| `getExamQuestions(examId, questionBankId, pageSize)` | `exam/question!readByExam` | | 题目列表 |
| `getExamResult(examId, questionBankId, pageSize)` | `exam/question!result` | | 逐题结果 |
| `getMyAnswerStats(examId)` | `exam/answer!statByStudent` | | 按题库统计 |
| `saveExamAnswer(record)` | `exam/answer!saveAnswer` | ✓ | 保存本人答案 |
| `emptyMyAnswers(examId, questionBankId)` | `exam/answer!emptyByStudent` | ✓ | 清空本套重做 |
| `getMyExamSituations(**kw)` | `online-exam/exam-situation!readAllExamSituation` | | 在线考试·我的考试情况 |

## 实测契约

- **`statByStudent` 忽略 questionBankId**：一次返回整场考试全部题库统计
  （每行带 questionBankName），别循环调用
- **`result` 必须 examId + questionBankId 成对**，缺任一报「id不能为空」
- 计分：一次答对 2 分，更正一次后答对 1 分，其余 0 分
- `question!destroy`（教师删题）**不封装**

## 实测样例（2026-10-24）

高二信息技术会考练习（examId=8aee8dc7…4090e）：16 题库共 576 题；
本人已在「选择题（python部分）」完成 43 题（一次对 38 + 更正对 5，0 错，80.5 分）。

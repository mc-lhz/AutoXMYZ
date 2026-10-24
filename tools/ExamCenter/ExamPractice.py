"""考试域 mixin：会考练习（信息技术会考）与在线考试。

契约要点（2026-10-24 实测）：
  - `answer!statByStudent` 的 questionBankId 参数**被服务端忽略**：一次调用即返回
    整场考试全部题库的统计（每行自带 questionBankName），无需逐题库循环。
  - `question!result` 需要 examId + questionBankId（缺任一报「id不能为空」）。
  - 计分规则（页面答题说明）：一次答对得 2 分，更正一次后答对得 1 分，其余不得分。
  - `question!destroy` 为教师删题功能，**本技能不封装**。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ExamPracticeMixin(object):
    """会考练习 / 在线考试 mixin（由 XMYZClient 组合）。"""

    def getMyOnlineExamCombo(self, **kw):
        """我的考试下拉。GET /exam/online-exam!getComboStoreByStudent.action"""
        return self.get("/exam/online-exam!getComboStoreByStudent.action", dict(kw))

    def getOnlineExamCombo(self, **kw):
        """全量考试下拉（可传 examId 过滤该场关联考试）。
        GET /exam/online-exam!getComboStore.action"""
        return self.get("/exam/online-exam!getComboStore.action", dict(kw))

    def getQuestionBankCombo(self, **kw):
        """题库下拉（可传 examId 过滤该场挂载的题库）。
        GET /exam/question-bank!getComboStore.action"""
        return self.get("/exam/question-bank!getComboStore.action", dict(kw))

    def getExamQuestions(self, examId, questionBankId, pageSize=20, **kw):
        """题目列表。GET /exam/question!readByExam.action"""
        p = {"examId": examId, "questionBankId": questionBankId,
             "pageSize": pageSize}
        p.update(kw)
        return self.get("/exam/question!readByExam.action", p)

    def getExamResult(self, examId, questionBankId, pageSize=20, **kw):
        """答题结果（逐题）。GET /exam/question!result.action
        ⚠️ examId 与 questionBankId 缺一不可，否则报「id不能为空」。"""
        p = {"examId": examId, "questionBankId": questionBankId,
             "pageSize": pageSize}
        p.update(kw)
        return self.get("/exam/question!result.action", p)

    def getMyAnswerStats(self, examId, **kw):
        """我的答题统计（按题库分行，行内 questionBankName）。
        GET /exam/answer!statByStudent.action
        ⚠️ questionBankId 会被服务端忽略——一次调用返回整场考试全部题库。"""
        p = {"examId": examId}
        p.update(kw)
        return self.get("/exam/answer!statByStudent.action", p)

    def saveExamAnswer(self, record, **kw):
        """保存本人答案（写）。POST /exam/answer!saveAnswer.action
        `record` 为单条答题记录 dict，字段以页面提交为准（原样透传，
        建议先 GET 一题对照字段再构造）。"""
        return self.post("/exam/answer!saveAnswer.action", dict(record), **kw)

    def emptyMyAnswers(self, examId, questionBankId, **kw):
        """清空本人在某套题的作答（写，用于重做）。POST /exam/answer!emptyByStudent.action
        只清本人数据；调用前确认 examId/questionBankId 成对。"""
        p = {"examId": examId, "questionBankId": questionBankId}
        p.update(kw)
        return self.post("/exam/answer!emptyByStudent.action", p, **kw)

    def getMyExamSituations(self, **kw):
        """在线考试·我的考试情况。GET /online-exam/exam-situation!readAllExamSituation.action"""
        return self.get("/online-exam/exam-situation!readAllExamSituation.action", dict(kw))

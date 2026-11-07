"""TeacherEvaluation —— 教师评测反馈 + 校本课程评测（4 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TeacherEvaluationMixin(object):
    """TeacherEvaluationMixin mixin（由 XMYZClient 组合）。"""

    def getComboStoreTeacherEvaluation(self, **kw):
        """evaluation/evaluation!getComboStore.action （教师评测反馈）"""
        return self.get('/evaluation/evaluation!getComboStore.action', dict(kw))

    def getComboStoreByStudentTeacherEvaluation(self, **kw):
        """evaluation/evaluation!getComboStoreByStudent.action （教师评测反馈）"""
        return self.get('/evaluation/evaluation!getComboStoreByStudent.action', dict(kw))

    def getEvaluationFormEvaluationItem(self, **kw):
        """evaluation/evaluation-item!getEvaluationForm.action （教师评测反馈）"""
        return self.get('/evaluation/evaluation-item!getEvaluationForm.action', dict(kw))

    def evaluationEvaluationResult(self, **kw):
        """evaluation/evaluation-result!evaluation.action （教师评测反馈）"""
        return self.post('/evaluation/evaluation-result!evaluation.action', dict(kw))

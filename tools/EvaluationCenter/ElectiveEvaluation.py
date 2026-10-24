"""ElectiveEvaluation —— 教师评测反馈 + 校本课程评测（4 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ElectiveEvaluationMixin(object):
    """ElectiveEvaluationMixin mixin（由 XMYZClient 组合）。"""

    def getComboStoreElectiveEvaluation(self, **kw):
        """elective-evaluation/elective-evaluation!getComboStore.action （校本课程评测）"""
        return self.get('/elective-evaluation/elective-evaluation!getComboStore.action', dict(kw))

    def getComboStoreByStudentElectiveEvaluation(self, **kw):
        """elective-evaluation/elective-evaluation!getComboStoreByStudent.action （校本课程评测）"""
        return self.get('/elective-evaluation/elective-evaluation!getComboStoreByStudent.action', dict(kw))

    def loadElectiveEvaluationFeedback(self, **kw):
        """elective-evaluation/evaluation-feedback-detail!load.action （校本课程评测）"""
        return self.get('/elective-evaluation/evaluation-feedback-detail!load.action', dict(kw))

    def saveElectiveEvaluationFeedback(self, **kw):
        """elective-evaluation/evaluation-feedback-detail!save.action （校本课程评测）"""
        return self.post('/elective-evaluation/evaluation-feedback-detail!save.action', dict(kw))

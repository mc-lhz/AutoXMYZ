"""ScoreExtras —— 成绩扩展：成绩单家长/导出变体、成绩分析选项（6 个端点）。

学生向零引用端点收口（2026-10-25 全量终检）。
参数 **kw 透传（GET query / POST form）。详见同名 md。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ScoreExtrasMixin(object):
    """ScoreExtras mixin（由 XMYZClient 组合）。"""

    def getStudentOrParentScoreAnalysisOptionScore(self, **kw):
        """score/score!getStudentOrParentScoreAnalysisOption.action"""
        return self.get('/score/score!getStudentOrParentScoreAnalysisOption.action', dict(kw))

    def getSubjectAndTotalScoreTypeTreeByStudentOrPanelScore(self, **kw):
        """score/score!getSubjectAndTotalScoreTypeTreeByStudentOrPanel.action"""
        return self.get('/score/score!getSubjectAndTotalScoreTypeTreeByStudentOrPanel.action', dict(kw))

    def getTranscriptByParentTranscript(self, **kw):
        """transcript/transcript!getTranscriptByParent.action"""
        return self.get('/transcript/transcript!getTranscriptByParent.action', dict(kw))

    def readTranscriptByParent(self, **kw):
        """transcript/transcript!readByParent.action"""
        return self.get('/transcript/transcript!readByParent.action', dict(kw))

    def transcriptExportByParentTranscript(self, **kw):
        """transcript/transcript!transcriptExportByParent.action"""
        return self.get('/transcript/transcript!transcriptExportByParent.action', dict(kw))

    def transcriptExportByStudentTranscript(self, **kw):
        """transcript/transcript!transcriptExportByStudent.action"""
        return self.get('/transcript/transcript!transcriptExportByStudent.action', dict(kw))

"""QualityExtras —— 综评扩展：quality/holistic-education/junior-quality/evaluation 学生变体（19 个端点）。

学生向零引用端点收口（2026-10-25 全量终检）。
参数 **kw 透传（GET query / POST form）。详见同名 md。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class QualityExtrasMixin(object):
    """QualityExtras mixin（由 XMYZClient 组合）。"""

    def getTreeByStudentEvaluation(self, **kw):
        """evaluation/evaluation!getTreeByStudent.action"""
        return self.get('/evaluation/evaluation!getTreeByStudent.action', dict(kw))

    def readEvaluationResultEvaluationStudent(self, **kw):
        """evaluation/evaluation-result!readEvaluationStudent.action"""
        return self.get('/evaluation/evaluation-result!readEvaluationStudent.action', dict(kw))

    def readScoreRecordByStudentId(self, **kw):
        """holistic-education/score-record!readByStudentId.action"""
        return self.get('/holistic-education/score-record!readByStudentId.action', dict(kw))

    def readByStudentOrParentScoreRecord(self, **kw):
        """holistic-education/score-record!readByStudentOrParent.action"""
        return self.get('/holistic-education/score-record!readByStudentOrParent.action', dict(kw))

    def studentScoreStatByStudentIdScoreRecord(self, **kw):
        """holistic-education/score-record!studentScoreStatByStudentId.action"""
        return self.get('/holistic-education/score-record!studentScoreStatByStudentId.action', dict(kw))

    def studentScoreStatByStudentOrParentScoreRecord(self, **kw):
        """holistic-education/score-record!studentScoreStatByStudentOrParent.action"""
        return self.get('/holistic-education/score-record!studentScoreStatByStudentOrParent.action', dict(kw))

    def surpassStatByStudentIdScoreRecord(self, **kw):
        """holistic-education/score-record!surpassStatByStudentId.action"""
        return self.get('/holistic-education/score-record!surpassStatByStudentId.action', dict(kw))

    def surpassStatByStudentOrParentScoreRecord(self, **kw):
        """holistic-education/score-record!surpassStatByStudentOrParent.action"""
        return self.get('/holistic-education/score-record!surpassStatByStudentOrParent.action', dict(kw))

    def getTreeByStudentIdEvaluation(self, **kw):
        """junior-quality/evaluation!getTreeByStudentId.action"""
        return self.get('/junior-quality/evaluation!getTreeByStudentId.action', dict(kw))

    def getTreeByStudentOrParentEvaluation(self, **kw):
        """junior-quality/evaluation!getTreeByStudentOrParent.action"""
        return self.get('/junior-quality/evaluation!getTreeByStudentOrParent.action', dict(kw))

    def getTreeByStudentEvaluationScore(self, **kw):
        """junior-quality/evaluation-score!getTreeByStudent.action"""
        return self.get('/junior-quality/evaluation-score!getTreeByStudent.action', dict(kw))

    def overallQualityEvaluationByStudentEvaluationYearScore(self, **kw):
        """junior-quality/evaluation-year-score!overallQualityEvaluationByStudent.action"""
        return self.get('/junior-quality/evaluation-year-score!overallQualityEvaluationByStudent.action', dict(kw))

    def exportQualityByStudentOrParent(self, **kw):
        """quality/quality!exportByStudentOrParent.action"""
        return self.get('/quality/quality!exportByStudentOrParent.action', dict(kw))

    def readByStudentOrParentQuality(self, **kw):
        """quality/quality!readByStudentOrParent.action"""
        return self.get('/quality/quality!readByStudentOrParent.action', dict(kw))

    def saveQualityDetailByStudentOrParnet(self, **kw):
        """quality/quality-detail!saveByStudentOrParnet.action"""
        return self.post('/quality/quality-detail!saveByStudentOrParnet.action', dict(kw))

    def exportQualityScoreStatByStudentOrParent(self, **kw):
        """quality/quality-score-stat!exportByStudentOrParent.action"""
        return self.get('/quality/quality-score-stat!exportByStudentOrParent.action', dict(kw))

    def readByStudentOrParentQualityScoreStat(self, **kw):
        """quality/quality-score-stat!readByStudentOrParent.action"""
        return self.get('/quality/quality-score-stat!readByStudentOrParent.action', dict(kw))

    def loadByStudentOrParnetStudentDescriptionDetail(self, **kw):
        """quality/student-description-detail!loadByStudentOrParnet.action"""
        return self.get('/quality/student-description-detail!loadByStudentOrParnet.action', dict(kw))

    def saveStudentDescriptionDetailByStudentOrParnet(self, **kw):
        """quality/student-description-detail!saveByStudentOrParnet.action"""
        return self.post('/quality/student-description-detail!saveByStudentOrParnet.action', dict(kw))

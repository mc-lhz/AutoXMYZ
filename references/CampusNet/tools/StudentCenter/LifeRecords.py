"""LifeRecords —— 生活记录：考勤/宿舍量化/文明班级/学生检查/健康/校产借出/家长访客/选课批次（15 个端点）。

学生向零引用端点收口（2026-10-25 全量终检）。
参数 **kw 透传（GET query / POST form）。详见同名 md。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LifeRecordsMixin(object):
    """LifeRecords mixin（由 XMYZClient 组合）。"""

    def readParentVisitByParent(self, **kw):
        """activiti/business/parent-visit!readByParent.action"""
        return self.get('/activiti/business/parent-visit!readByParent.action', dict(kw))

    def readByStudentOrParentCivilizedClassEvaluation(self, **kw):
        """class-evaluation/civilized-class-evaluation!readByStudentOrParent.action"""
        return self.get('/class-evaluation/civilized-class-evaluation!readByStudentOrParent.action', dict(kw))

    def exportMemberEvaluateByStudent(self, **kw):
        """community/member-evaluate!exportByStudent.action"""
        return self.get('/community/member-evaluate!exportByStudent.action', dict(kw))

    def exportPropertyBorrowByStudent(self, **kw):
        """community/property-borrow!exportByStudent.action"""
        return self.get('/community/property-borrow!exportByStudent.action', dict(kw))

    def readPropertyBorrowByStudent(self, **kw):
        """community/property-borrow!readByStudent.action"""
        return self.get('/community/property-borrow!readByStudent.action', dict(kw))

    def readByStudentOrParentQuantify(self, **kw):
        """dormitory/quantify!readByStudentOrParent.action"""
        return self.get('/dormitory/quantify!readByStudentOrParent.action', dict(kw))

    def readAttendanceByStudent(self, **kw):
        """edu/attendance!readByStudent.action"""
        return self.get('/edu/attendance!readByStudent.action', dict(kw))

    def readEvaluationByStudent(self, **kw):
        """edu/evaluation!readByStudent.action"""
        return self.get('/edu/evaluation!readByStudent.action', dict(kw))

    def readGrowthRecordByStudent(self, **kw):
        """edu/growth-record!readByStudent.action"""
        return self.get('/edu/growth-record!readByStudent.action', dict(kw))

    def readGrowthRecordClassByStudent(self, **kw):
        """edu/growth-record!readClassByStudent.action"""
        return self.get('/edu/growth-record!readClassByStudent.action', dict(kw))

    def uploadPhotoByStudentStudent(self, **kw):
        """edu/student!uploadPhotoByStudent.action"""
        return self.post('/edu/student!uploadPhotoByStudent.action', dict(kw))

    def getComboStoreByStudentOrParentElective(self, **kw):
        """elective/elective!getComboStoreByStudentOrParent.action"""
        return self.get('/elective/elective!getComboStoreByStudentOrParent.action', dict(kw))

    def reminderUnsubmittedStudentHealthInfo(self, **kw):
        """health/health-info!reminderUnsubmittedStudent.action"""
        return self.get('/health/health-info!reminderUnsubmittedStudent.action', dict(kw))

    def readStudentCheckByStudent(self, **kw):
        """moral/student-check!readByStudent.action"""
        return self.get('/moral/student-check!readByStudent.action', dict(kw))

    def readByStudentOrParentStudentAttendanceRecord(self, **kw):
        """student-attendance/student-attendance-record!readByStudentOrParent.action"""
        return self.get('/student-attendance/student-attendance-record!readByStudentOrParent.action', dict(kw))

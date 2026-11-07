"""ElectiveAttendance —— 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿（14 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ElectiveAttendanceMixin(object):
    """ElectiveAttendanceMixin mixin（由 XMYZClient 组合）。"""

    def createElectiveAttendance(self, **kw):
        """elective/attendance!create.action （我的考勤记录）"""
        return self.post('/elective/attendance!create.action', dict(kw))

    def destroyElectiveAttendance(self, **kw):
        """elective/attendance!destroy.action （我的考勤记录）"""
        return self.post('/elective/attendance!destroy.action', dict(kw))

    def exportElectiveAttendanceByStudent(self, **kw):
        """elective/attendance!export.action （我的考勤记录）"""
        return self.get('/elective/attendance!export.action', dict(kw))

    def exportElectiveAttendanceByClassTeacher(self, **kw):
        """elective/attendance!exportByClassTeacher.action （我的考勤记录）"""
        return self.get('/elective/attendance!exportByClassTeacher.action', dict(kw))

    def exportElectiveAttendanceByGradeTeacher(self, **kw):
        """elective/attendance!exportByGradeTeacher.action （我的考勤记录）"""
        return self.get('/elective/attendance!exportByGradeTeacher.action', dict(kw))

    def exportElectiveAttendanceByStudentOrParent(self, **kw):
        """elective/attendance!exportByStudentOrParent.action （我的考勤记录）"""
        return self.get('/elective/attendance!exportByStudentOrParent.action', dict(kw))

    def exportElectiveAttendanceByTeacher(self, **kw):
        """elective/attendance!exportByTeacher.action （我的考勤记录）"""
        return self.get('/elective/attendance!exportByTeacher.action', dict(kw))

    def importElectiveAttendance(self, **kw):
        """elective/attendance!imp.action （我的考勤记录）"""
        return self.post('/elective/attendance!imp.action', dict(kw))

    def readElectiveAttendance(self, **kw):
        """elective/attendance!read.action （我的考勤记录）"""
        return self.get('/elective/attendance!read.action', dict(kw))

    def readElectiveAttendanceByClassTeacher(self, **kw):
        """elective/attendance!readByClassTeacher.action （我的考勤记录）"""
        return self.get('/elective/attendance!readByClassTeacher.action', dict(kw))

    def readElectiveAttendanceByGradeTeacher(self, **kw):
        """elective/attendance!readByGradeTeacher.action （我的考勤记录）"""
        return self.get('/elective/attendance!readByGradeTeacher.action', dict(kw))

    def readElectiveAttendanceByStudentOrParent(self, **kw):
        """elective/attendance!readByStudentOrParent.action （我的考勤记录）"""
        return self.get('/elective/attendance!readByStudentOrParent.action', dict(kw))

    def readElectiveAttendanceByTeacher(self, **kw):
        """elective/attendance!readByTeacher.action （我的考勤记录）"""
        return self.get('/elective/attendance!readByTeacher.action', dict(kw))

    def updateElectiveAttendance(self, **kw):
        """elective/attendance!update.action （我的考勤记录）"""
        return self.post('/elective/attendance!update.action', dict(kw))

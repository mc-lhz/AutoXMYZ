"""ElectiveCourse —— 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿（23 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ElectiveCourseMixin(object):
    """ElectiveCourseMixin mixin（由 XMYZClient 组合）。"""

    def createElectiveCourse(self, **kw):
        """elective/course!create.action （选课）"""
        return self.post('/elective/course!create.action', dict(kw))

    def destroyElectiveCourse(self, **kw):
        """elective/course!destroy.action （选课）"""
        return self.post('/elective/course!destroy.action', dict(kw))

    def exportElectiveCourse(self, **kw):
        """elective/course!export.action （选课）"""
        return self.get('/elective/course!export.action', dict(kw))

    def getComboStoreByElectiveElectiveCourse(self, **kw):
        """elective/course!getComboStoreByElective.action （选课）"""
        return self.get('/elective/course!getComboStoreByElective.action', dict(kw))

    def getComboStoreByTeacherElectiveCourse(self, **kw):
        """elective/course!getComboStoreByTeacher.action （活动记录）"""
        return self.get('/elective/course!getComboStoreByTeacher.action', dict(kw))

    def getComboStoreByTeacherOrPresidentElectiveCourse(self, **kw):
        """elective/course!getComboStoreByTeacherOrPresident.action （活动记录）"""
        return self.get('/elective/course!getComboStoreByTeacherOrPresident.action', dict(kw))

    def importElectiveCourse(self, **kw):
        """elective/course!imp.action （选课）"""
        return self.post('/elective/course!imp.action', dict(kw))

    def loadTreeElectiveCourse(self, **kw):
        """elective/course!loadTree.action （活动记录 / 我的考勤记录 / 预选课）"""
        return self.get('/elective/course!loadTree.action', dict(kw))

    def loadTreeByAdvanceElectiveCourse(self, **kw):
        """elective/course!loadTreeByAdvance.action （预选课）"""
        return self.get('/elective/course!loadTreeByAdvance.action', dict(kw))

    def loadTreeByTeacherElectiveCourse(self, **kw):
        """elective/course!loadTreeByTeacher.action （活动记录 / 我的考勤记录 / 预选课）"""
        return self.get('/elective/course!loadTreeByTeacher.action', dict(kw))

    def readElectiveCourseByStudentOrParent(self, **kw):
        """elective/course!readByStudentOrParent.action （选课）"""
        return self.get('/elective/course!readByStudentOrParent.action', dict(kw))

    def updateElectiveCourse(self, **kw):
        """elective/course!update.action （选课）"""
        return self.post('/elective/course!update.action', dict(kw))

    def directSaveElectiveCourseDetail(self, **kw):
        """elective/course-detail!directSave.action （活动记录）"""
        return self.post('/elective/course-detail!directSave.action', dict(kw))

    def getComboStoreElective(self, **kw):
        """elective/elective!getComboStore.action （活动记录 / 我的考勤记录 / 预选课 / 选课 / 学生选课(厦一大讲堂)）"""
        return self.get('/elective/elective!getComboStore.action', dict(kw))

    def getComboStoreByAdvanceElective(self, **kw):
        """elective/elective!getComboStoreByAdvance.action （预选课）"""
        return self.get('/elective/elective!getComboStoreByAdvance.action', dict(kw))

    def getComboStoreByClassTeacherElective(self, **kw):
        """elective/elective!getComboStoreByClassTeacher.action （我的考勤记录 / 预选课）"""
        return self.get('/elective/elective!getComboStoreByClassTeacher.action', dict(kw))

    def getComboStoreByGradeOrClassTeacherElective(self, **kw):
        """elective/elective!getComboStoreByGradeOrClassTeacher.action （我的考勤记录）"""
        return self.get('/elective/elective!getComboStoreByGradeOrClassTeacher.action', dict(kw))

    def getComboStoreByStudentElective(self, **kw):
        """elective/elective!getComboStoreByStudent.action （学生选课(厦一大讲堂) / 选课）"""
        return self.get('/elective/elective!getComboStoreByStudent.action', dict(kw))

    def getComboStoreByTeacherElective(self, **kw):
        """elective/elective!getComboStoreByTeacher.action （活动记录 / 我的考勤记录 / 预选课）"""
        return self.get('/elective/elective!getComboStoreByTeacher.action', dict(kw))

    def getGradeClassTreeElective(self, **kw):
        """elective/elective!getGradeClassTree.action （我的考勤记录 / 预选课）"""
        return self.get('/elective/elective!getGradeClassTree.action', dict(kw))

    def getGradeClassTreeByClassTeacherElective(self, **kw):
        """elective/elective!getGradeClassTreeByClassTeacher.action （我的考勤记录 / 预选课）"""
        return self.get('/elective/elective!getGradeClassTreeByClassTeacher.action', dict(kw))

    def getStudentWishWish(self, **kw):
        """elective/wish!getStudentWish.action （学生选课(厦一大讲堂) / 选课）"""
        return self.get('/elective/wish!getStudentWish.action', dict(kw))

    def saveWishWish(self, **kw):
        """elective/wish!saveWish.action （学生选课(厦一大讲堂) / 选课）"""
        return self.post('/elective/wish!saveWish.action', dict(kw))

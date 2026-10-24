"""ElectiveResult —— 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿（36 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ElectiveResultMixin(object):
    """ElectiveResultMixin mixin（由 XMYZClient 组合）。"""

    def batchAddElectiveResult(self, **kw):
        """elective/elective-result!batchAdd.action （预选课）"""
        return self.post('/elective/elective-result!batchAdd.action', dict(kw))

    def batchPackingExportElectiveResult(self, **kw):
        """elective/elective-result!batchPackingExport.action （预选课）"""
        return self.post('/elective/elective-result!batchPackingExport.action', dict(kw))

    def createElectiveResult(self, **kw):
        """elective/elective-result!create.action （预选课）"""
        return self.post('/elective/elective-result!create.action', dict(kw))

    def createByAdvanceElectiveResult(self, **kw):
        """elective/elective-result!createByAdvance.action （预选课）"""
        return self.post('/elective/elective-result!createByAdvance.action', dict(kw))

    def destroyElectiveResult(self, **kw):
        """elective/elective-result!destroy.action （预选课）"""
        return self.post('/elective/elective-result!destroy.action', dict(kw))

    def destroyByAdvanceElectiveResult(self, **kw):
        """elective/elective-result!destroyByAdvance.action （预选课）"""
        return self.post('/elective/elective-result!destroyByAdvance.action', dict(kw))

    def destroyByClassTeacherElectiveResult(self, **kw):
        """elective/elective-result!destroyByClassTeacher.action （预选课）"""
        return self.post('/elective/elective-result!destroyByClassTeacher.action', dict(kw))

    def electiveElectiveResult(self, **kw):
        """elective/elective-result!elective.action （选课）"""
        return self.post('/elective/elective-result!elective.action', dict(kw))

    def exportElectiveResult(self, **kw):
        """elective/elective-result!export.action （预选课）"""
        return self.get('/elective/elective-result!export.action', dict(kw))

    def exportElectiveResultByAdvance(self, **kw):
        """elective/elective-result!exportByAdvance.action （预选课）"""
        return self.get('/elective/elective-result!exportByAdvance.action', dict(kw))

    def exportElectiveResultByClassTeacher(self, **kw):
        """elective/elective-result!exportByClassTeacher.action （预选课）"""
        return self.get('/elective/elective-result!exportByClassTeacher.action', dict(kw))

    def exportElectiveResultByTeacher(self, **kw):
        """elective/elective-result!exportByTeacher.action （预选课）"""
        return self.get('/elective/elective-result!exportByTeacher.action', dict(kw))

    def exportPackingElectiveResult(self, **kw):
        """elective/elective-result!exportPacking.action （预选课）"""
        return self.get('/elective/elective-result!exportPacking.action', dict(kw))

    def importElectiveResult(self, **kw):
        """elective/elective-result!imp.action （预选课）"""
        return self.post('/elective/elective-result!imp.action', dict(kw))

    def initProcessGradeElectiveResult(self, **kw):
        """elective/elective-result!initProcessGrade.action （预选课）"""
        return self.post('/elective/elective-result!initProcessGrade.action', dict(kw))

    def readElectiveResultByAdvance(self, **kw):
        """elective/elective-result!readByAdvance.action （预选课）"""
        return self.get('/elective/elective-result!readByAdvance.action', dict(kw))

    def readElectiveResultByClassTeacher(self, **kw):
        """elective/elective-result!readByClassTeacher.action （预选课）"""
        return self.get('/elective/elective-result!readByClassTeacher.action', dict(kw))

    def readElectiveResultByTeacher(self, **kw):
        """elective/elective-result!readByTeacher.action （预选课）"""
        return self.get('/elective/elective-result!readByTeacher.action', dict(kw))

    def reportClassHourRegistrationElectiveResult(self, **kw):
        """elective/elective-result!reportClassHourRegistration.action （预选课）"""
        return self.post('/elective/elective-result!reportClassHourRegistration.action', dict(kw))

    def reportClassHourRegistrationExcelElectiveResult(self, **kw):
        """elective/elective-result!reportClassHourRegistrationExcel.action （预选课）"""
        return self.post('/elective/elective-result!reportClassHourRegistrationExcel.action', dict(kw))

    def reportRollBookElectiveResult(self, **kw):
        """elective/elective-result!reportRollBook.action （预选课）"""
        return self.post('/elective/elective-result!reportRollBook.action', dict(kw))

    def updateElectiveResult(self, **kw):
        """elective/elective-result!update.action （预选课）"""
        return self.post('/elective/elective-result!update.action', dict(kw))

    def updateByAdvanceElectiveResult(self, **kw):
        """elective/elective-result!updateByAdvance.action （预选课）"""
        return self.post('/elective/elective-result!updateByAdvance.action', dict(kw))

    def updateByClassTeacherElectiveResult(self, **kw):
        """elective/elective-result!updateByClassTeacher.action （预选课）"""
        return self.post('/elective/elective-result!updateByClassTeacher.action', dict(kw))

    def updateByTeacherElectiveResult(self, **kw):
        """elective/elective-result!updateByTeacher.action （预选课）"""
        return self.post('/elective/elective-result!updateByTeacher.action', dict(kw))

    def createMultipleCourse(self, **kw):
        """elective/multiple-course!create.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-course!create.action', dict(kw))

    def destroyMultipleCourse(self, **kw):
        """elective/multiple-course!destroy.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-course!destroy.action', dict(kw))

    def exportMultipleCourse(self, **kw):
        """elective/multiple-course!export.action （学生选课(厦一大讲堂)）"""
        return self.get('/elective/multiple-course!export.action', dict(kw))

    def getComboStoreByElectiveMultipleCourse(self, **kw):
        """elective/multiple-course!getComboStoreByElective.action （学生选课(厦一大讲堂)）"""
        return self.get('/elective/multiple-course!getComboStoreByElective.action', dict(kw))

    def importMultipleCourse(self, **kw):
        """elective/multiple-course!imp.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-course!imp.action', dict(kw))

    def readMultipleCourse(self, **kw):
        """elective/multiple-course!readByStudent.action （学生选课(厦一大讲堂)）"""
        return self.get('/elective/multiple-course!readByStudent.action', dict(kw))

    def updateMultipleCourse(self, **kw):
        """elective/multiple-course!update.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-course!update.action', dict(kw))

    def loadMultipleCourseDetail(self, **kw):
        """elective/multiple-course-detail!load.action （学生选课(厦一大讲堂)）"""
        return self.get('/elective/multiple-course-detail!load.action', dict(kw))

    def cancelElectiveMultipleResult(self, **kw):
        """elective/multiple-result!cancelElective.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-result!cancelElective.action', dict(kw))

    def electiveMultipleResult(self, **kw):
        """elective/multiple-result!elective.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-result!elective.action', dict(kw))

    def lockElectiveMultipleResult(self, **kw):
        """elective/multiple-result!lockElective.action （学生选课(厦一大讲堂)）"""
        return self.post('/elective/multiple-result!lockElective.action', dict(kw))

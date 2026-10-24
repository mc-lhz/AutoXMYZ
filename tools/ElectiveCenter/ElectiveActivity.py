"""ElectiveActivity —— 选课系统（厦一大讲堂/校本选课）：课程、选课结果、多轮预选、活动记录、考勤、志愿（19 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ElectiveActivityMixin(object):
    """ElectiveActivityMixin mixin（由 XMYZClient 组合）。"""

    def createActivityRecord(self, **kw):
        """elective/activity-record!create.action （活动记录）"""
        return self.post('/elective/activity-record!create.action', dict(kw))

    def createByCourseTeacherActivityRecord(self, **kw):
        """elective/activity-record!createByCourseTeacher.action （活动记录）"""
        return self.post('/elective/activity-record!createByCourseTeacher.action', dict(kw))

    def createByTeacherOrPresidentActivityRecord(self, **kw):
        """elective/activity-record!createByTeacherOrPresident.action （活动记录）"""
        return self.post('/elective/activity-record!createByTeacherOrPresident.action', dict(kw))

    def delteActivityPhotosActivityRecord(self, **kw):
        """elective/activity-record!delteActivityPhotos.action （活动记录）"""
        return self.post('/elective/activity-record!delteActivityPhotos.action', dict(kw))

    def destroyActivityRecord(self, **kw):
        """elective/activity-record!destroy.action （活动记录）"""
        return self.post('/elective/activity-record!destroy.action', dict(kw))

    def downloadAttachmentActivityRecord(self, **kw):
        """elective/activity-record!downloadAttachment.action （活动记录）"""
        return self.get('/elective/activity-record!downloadAttachment.action', dict(kw))

    def downloadAttachmentByCourseTeacherActivityRecord(self, **kw):
        """elective/activity-record!downloadAttachmentByCourseTeacher.action （活动记录）"""
        return self.get('/elective/activity-record!downloadAttachmentByCourseTeacher.action', dict(kw))

    def exportActivityRecord(self, **kw):
        """elective/activity-record!export.action （活动记录）"""
        return self.get('/elective/activity-record!export.action', dict(kw))

    def exportActivityRecordByCourseTeacher(self, **kw):
        """elective/activity-record!exportByCourseTeacher.action （活动记录）"""
        return self.get('/elective/activity-record!exportByCourseTeacher.action', dict(kw))

    def exportActivityRecordByTeacher(self, **kw):
        """elective/activity-record!exportByTeacher.action（⚠️ 线上 404 GONE） （活动记录）"""
        return self.get('/elective/activity-record!exportByTeacher.action', dict(kw))

    def importActivityRecord(self, **kw):
        """elective/activity-record!imp.action （活动记录）"""
        return self.post('/elective/activity-record!imp.action', dict(kw))

    def impByCourseTeacherActivityRecord(self, **kw):
        """elective/activity-record!impByCourseTeacher.action （活动记录）"""
        return self.post('/elective/activity-record!impByCourseTeacher.action', dict(kw))

    def readActivityRecord(self, **kw):
        """elective/activity-record!read.action （活动记录）"""
        return self.get('/elective/activity-record!read.action', dict(kw))

    def readActivityRecordByCourseTeacher(self, **kw):
        """elective/activity-record!readByCourseTeacher.action （活动记录）"""
        return self.get('/elective/activity-record!readByCourseTeacher.action', dict(kw))

    def readActivityRecordByTeacher(self, **kw):
        """elective/activity-record!readByTeacher.action（⚠️ 线上 404 GONE） （活动记录）"""
        return self.get('/elective/activity-record!readByTeacher.action', dict(kw))

    def readActivityRecordByTeacherOrPresident(self, **kw):
        """elective/activity-record!readByTeacherOrPresident.action （活动记录）"""
        return self.get('/elective/activity-record!readByTeacherOrPresident.action', dict(kw))

    def reportRollBookActivityRecord(self, **kw):
        """elective/activity-record!reportRollBook.action （活动记录）"""
        return self.post('/elective/activity-record!reportRollBook.action', dict(kw))

    def updateActivityRecord(self, **kw):
        """elective/activity-record!update.action （活动记录）"""
        return self.post('/elective/activity-record!update.action', dict(kw))

    def uploadActivityPhotosActivityRecord(self, **kw):
        """elective/activity-record!uploadActivityPhotos.action （活动记录）"""
        return self.post('/elective/activity-record!uploadActivityPhotos.action', dict(kw))

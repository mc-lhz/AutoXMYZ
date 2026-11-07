"""PsychAppointment —— 心理咨询预约：预约、时间下拉、明细（13 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class PsychAppointmentMixin(object):
    """PsychAppointmentMixin mixin（由 XMYZClient 组合）。"""

    def createAppointment(self, **kw):
        """psychological/appointment!create.action （预约申请 / 我的预约）"""
        return self.post('/psychological/appointment!create.action', dict(kw))

    def createByTeacherAppointment(self, **kw):
        """psychological/appointment!createByTeacher.action （预约申请 / 我的预约）"""
        return self.post('/psychological/appointment!createByTeacher.action', dict(kw))

    def destroyAppointment(self, **kw):
        """psychological/appointment!destroy.action （预约申请 / 我的预约）"""
        return self.post('/psychological/appointment!destroy.action', dict(kw))

    def exportAppointment(self, **kw):
        """psychological/appointment!export.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment!export.action', dict(kw))

    def importAppointment(self, **kw):
        """psychological/appointment!imp.action （预约申请 / 我的预约）"""
        return self.post('/psychological/appointment!imp.action', dict(kw))

    def readAppointment(self, **kw):
        """psychological/appointment!read.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment!read.action', dict(kw))

    def readAppointmentByRequest(self, **kw):
        """psychological/appointment!readByRequest.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment!readByRequest.action', dict(kw))

    def readAppointmentByTeacher(self, **kw):
        """psychological/appointment!readByTeacher.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment!readByTeacher.action', dict(kw))

    def updateAppointment(self, **kw):
        """psychological/appointment!update.action （预约申请 / 我的预约）"""
        return self.post('/psychological/appointment!update.action', dict(kw))

    def loadAppointmentDetail(self, **kw):
        """psychological/appointment-detail!load.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment-detail!load.action', dict(kw))

    def saveAppointmentDetail(self, **kw):
        """psychological/appointment-detail!save.action （预约申请 / 我的预约）"""
        return self.post('/psychological/appointment-detail!save.action', dict(kw))

    def getComboStoreAppointmentTime(self, **kw):
        """psychological/appointment-time!getComboStore.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment-time!getComboStore.action', dict(kw))

    def getComboStoreByRequestAppointmentTime(self, **kw):
        """psychological/appointment-time!getComboStoreByRequest.action （预约申请 / 我的预约）"""
        return self.get('/psychological/appointment-time!getComboStoreByRequest.action', dict(kw))

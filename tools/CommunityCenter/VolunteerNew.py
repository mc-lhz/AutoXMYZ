"""VolunteerNew —— 志愿者(新)：活动报名/签到/调查/AIMUNC/美辩（19 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class VolunteerNewMixin(object):
    """VolunteerNewMixin mixin（由 XMYZClient 组合）。"""

    def readVolunteerActivityBySign(self, **kw):
        """volunteer/activity!readBySign.action （志愿者签到）"""
        return self.get('/volunteer/activity!readBySign.action', dict(kw))

    def createActivityRegistration(self, **kw):
        """volunteer/activity-registration!create.action （我参与的活动）"""
        return self.post('/volunteer/activity-registration!create.action', dict(kw))

    def destroyActivityRegistration(self, **kw):
        """volunteer/activity-registration!destroy.action （我参与的活动）"""
        return self.post('/volunteer/activity-registration!destroy.action', dict(kw))

    def exportActivityRegistration(self, **kw):
        """volunteer/activity-registration!exportByStudent.action （我参与的活动）"""
        return self.get('/volunteer/activity-registration!exportByStudent.action', dict(kw))

    def importActivityRegistration(self, **kw):
        """volunteer/activity-registration!imp.action （我参与的活动）"""
        return self.post('/volunteer/activity-registration!imp.action', dict(kw))

    def readActivityRegistration(self, **kw):
        """volunteer/activity-registration!readByStudent.action （我参与的活动）"""
        return self.get('/volunteer/activity-registration!readByStudent.action', dict(kw))

    def registrationActivityRegistration(self, **kw):
        """volunteer/activity-registration!registration.action （志愿者活动报名）"""
        return self.post('/volunteer/activity-registration!registration.action', dict(kw))

    def unregistrationActivityRegistration(self, **kw):
        """volunteer/activity-registration!unregistration.action （志愿者活动报名）"""
        return self.post('/volunteer/activity-registration!unregistration.action', dict(kw))

    def updateActivityRegistration(self, **kw):
        """volunteer/activity-registration!update.action （我参与的活动）"""
        return self.post('/volunteer/activity-registration!update.action', dict(kw))

    def readVolunteerActivity2ByRegistration(self, **kw):
        """volunteer/activity2!readByRegistration.action （志愿者活动报名）"""
        return self.get('/volunteer/activity2!readByRegistration.action', dict(kw))

    def loadAimuncDetail(self, **kw):
        """volunteer/aimunc-detail!load.action （AIMUNC志愿者申请）"""
        return self.get('/volunteer/aimunc-detail!load.action', dict(kw))

    def saveAimuncDetail(self, **kw):
        """volunteer/aimunc-detail!save.action （AIMUNC志愿者申请）"""
        return self.post('/volunteer/aimunc-detail!save.action', dict(kw))

    def loadNhsdlcDetail(self, **kw):
        """volunteer/nhsdlc-detail!load.action （美辩志愿者报名）"""
        return self.get('/volunteer/nhsdlc-detail!load.action', dict(kw))

    def saveNhsdlcDetail(self, **kw):
        """volunteer/nhsdlc-detail!save.action （美辩志愿者报名）"""
        return self.post('/volunteer/nhsdlc-detail!save.action', dict(kw))

    def loadSurveyDetail(self, **kw):
        """volunteer/survey-detail!load.action （志愿者调查）"""
        return self.get('/volunteer/survey-detail!load.action', dict(kw))

    def saveSurveyDetail(self, **kw):
        """volunteer/survey-detail!save.action （志愿者调查）"""
        return self.post('/volunteer/survey-detail!save.action', dict(kw))

    def signVolunteer(self, **kw):
        """volunteer/volunteer!sign.action （志愿者签到）"""
        return self.post('/volunteer/volunteer!sign.action', dict(kw))

    def loadVolunteerRegistrationDetail(self, **kw):
        """volunteer/volunteer-registration-detail!load.action （志愿者报名 / 志愿者活动报名）"""
        return self.get('/volunteer/volunteer-registration-detail!load.action', dict(kw))

    def saveVolunteerRegistrationDetail(self, **kw):
        """volunteer/volunteer-registration-detail!save.action （志愿者报名 / 志愿者活动报名）"""
        return self.post('/volunteer/volunteer-registration-detail!save.action', dict(kw))

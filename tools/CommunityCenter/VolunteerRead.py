"""社团与志愿服务：community（111 端点，最大域）与 volunteer（19 端点）。

对应端点前缀：`community/`、`volunteer/`
"""


class CommunityMixin(object):

    def communityTree(self, **kw):
        """社团树。GET /community/community!loadTree.action"""
        return self.get("/community/community!loadTree.action", dict(kw))

    def communityCombo(self):
        """社团下拉。GET /community/community!getComboStore.action"""
        return self.get("/community/community!getComboStore.action", {})

    def myCommunities(self, **kw):
        """我参与的社团。GET /community/community!readByMember.action
        ⚠️ 旧实现打 member!readByStudent.action——线上 404（GONE 类死路由），
        2026-10-24 改打 readByMember（success:true，无加入时返回空数组）。"""
        return self.paged("/community/community!readByMember.action", dict(kw))

    def memberEvaluate(self, **kw):
        """成员评价。GET /community/member-evaluate!readByStudent.action"""
        return self.paged("/community/member-evaluate!readByStudent.action", dict(kw))

    def communityAttendance(self, **kw):
        """社团考勤。GET /community/attendance!readByStudent.action"""
        return self.paged("/community/attendance!readByStudent.action", dict(kw))

    def communityNotice(self, **kw):
        """社团通知。GET /community/notice!read.action"""
        return self.paged("/community/notice!read.action", dict(kw))

    def propertyBorrow(self, **kw):
        """校产借出明细。GET /community/property-borrow!read.action"""
        return self.paged("/community/property-borrow!read.action", dict(kw))

    def forum(self, communityId=None, **kw):
        """社团论坛。GET /community/forum!read.action"""
        p = {"communityId": communityId}
        p.update(kw)
        return self.paged("/community/forum!read.action", p)

    def workDetail(self, id=None):
        """社团作业详情。GET /community/work!detail.action"""
        return self.get("/community/work!detail.action", {"id": id})

    def memberTree(self, **kw):
        """成员树。GET /community/member!loadStudentTree.action"""
        return self.get("/community/member!loadStudentTree.action", dict(kw))


class VolunteerMixin(object):

    def myVolunteerActivities(self, **kw):
        """我参与的活动。GET /volunteer/activity!readByParticipate.action"""
        return self.paged("/volunteer/activity!readByParticipate.action", dict(kw))

    def volunteerActivities(self, **kw):
        """志愿活动列表。GET /volunteer/activity!read.action"""
        return self.paged("/volunteer/activity!read.action", dict(kw))

    def activityDetail(self, id=None, **kw):
        """活动详情。GET /volunteer/activity-detail!detail.action"""
        p = {"id": id}
        p.update(kw)
        return self.get("/volunteer/activity-detail!detail.action", p)

    def signRecords(self, **kw):
        """志愿者签到。GET /volunteer/sign!read.action"""
        return self.paged("/volunteer/sign!read.action", dict(kw))

    def surveys(self, **kw):
        """志愿者调查。GET /volunteer/survey!read.action"""
        return self.paged("/volunteer/survey!read.action", dict(kw))

    def registrations(self, **kw):
        """报名记录。GET /volunteer/registration!read.action"""
        return self.paged("/volunteer/registration!read.action", dict(kw))

    def volunteerHours(self, **kw):
        """志愿时长统计。GET /volunteer/activity!stat.action"""
        return self.get("/volunteer/activity!stat.action", dict(kw))
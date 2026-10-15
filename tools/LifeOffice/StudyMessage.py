"""日常生活与办公：成长记录、成绩、作业、体测、短信、通知、附件。

对应端点前缀：`edu/`、`score/`、`transcript/`、`message/`、`office/`、`system/attachment`
"""


class StudyMixin(object):

    def myScores(self, **kw):
        """我的成绩（分页）。GET /score/student-score!read.action"""
        return self.paged("/score/student-score!read.action", dict(kw))

    def studentScoreTable(self, **kw):
        """成绩表视图。GET /score/student-score!readByStudent.action"""
        return self.get("/score/student-score!readByStudent.action", dict(kw))

    def moduleScores(self, **kw):
        """模块修习成绩。GET /edu/module-score!read.action"""
        return self.paged("/edu/module-score!read.action", dict(kw))

    def transcript(self, **kw):
        """我的成绩单。GET /transcript/transcript!readByStudent.action"""
        return self.get("/transcript/transcript!readByStudent.action", dict(kw))

    def transcriptDetail(self, id=None, **kw):
        """成绩单详情。GET /transcript/transcript!detail.action"""
        p = {"id": id}
        p.update(kw)
        return self.get("/transcript/transcript!detail.action", p)

    def physicalExamination(self, **kw):
        """体能测试结果。GET /edu/physical-examination!readByStudent.action"""
        return self.get("/edu/physical-examination!readByStudent.action", dict(kw))

    def growthRecords(self, **kw):
        """我的成长记录（分页）。GET /edu/growth-record!read.action"""
        return self.paged("/edu/growth-record!read.action", dict(kw))

    def growthRecordDetail(self, id=None, **kw):
        """成长记录详情。GET /edu/growth-record-detail!detailJosn.action"""
        p = {"id": id}
        p.update(kw)
        return self.get("/edu/growth-record-detail!detailJosn.action", p)

    def classGrowthRecords(self, **kw):
        """同学成长记录（班主任）。GET /edu/growth-record!readByClassTeacher.action"""
        return self.paged("/edu/growth-record!readByClassTeacher.action", dict(kw))

    def classWork(self, **kw):
        """班级作业。GET /edu/work!readByClass.action"""
        return self.paged("/edu/work!readByClass.action", dict(kw))

    def homeworkCompleteTime(self, **kw):
        """作业完成时间登记。GET /edu/homework-complete-time!read.action"""
        return self.paged("/edu/homework-complete-time!read.action", dict(kw))

    def excellentWorks(self, **kw):
        """优秀作品。GET /edu/student-work!readExcellentWork.action"""
        return self.get("/edu/student-work!readExcellentWork.action", dict(kw))

    def matchAwards(self, **kw):
        """比赛获奖。GET /edu/match-awards!read.action"""
        return self.paged("/edu/match-awards!read.action", dict(kw))

    def attendanceByClass(self, classId=None, **kw):
        """班级考勤。GET /edu/attendance!readByClass.action"""
        p = {"classId": classId}
        p.update(kw)
        return self.paged("/edu/attendance!readByClass.action", p)

    def speciality(self, **kw):
        """特长信息。GET /edu/speciality!readByStudent.action"""
        return self.get("/edu/speciality!readByStudent.action", dict(kw))


class MessageMixin(object):

    def inbox(self, **kw):
        """短信收件箱（分页）。GET /message/short-message!inbox.action"""
        return self.paged("/message/short-message!inbox.action", dict(kw))

    def outbox(self, **kw):
        """短信发件箱。GET /message/short-message!outbox.action"""
        return self.paged("/message/short-message!outbox.action", dict(kw))

    def messageDetail(self, id=None, **kw):
        """短信详情。GET /message/short-message-detail!read.action"""
        p = {"id": id}
        p.update(kw)
        return self.get("/message/short-message-detail!read.action", p)

    def unreadStat(self):
        """未读统计。GET /message/recipient!findUnread.action"""
        return self.get("/message/recipient!findUnread.action", {})

    def recipientStat(self):
        """收发统计。GET /message/recipient!statInfo.action"""
        return self.get("/message/recipient!statInfo.action", {})

    def categoryMessages(self, categoryId=None, **kw):
        """分类消息。GET /message/message-grid!findReadByCategory.action"""
        p = {"categoryId": categoryId}
        p.update(kw)
        return self.paged("/message/message-grid!findReadByCategory.action", p)

    def noticeFeedback(self, **kw):
        """通知公告查看。GET /office/notification-feedback!read.action"""
        return self.paged("/office/notification-feedback!read.action", dict(kw))

    def noticeByTarget(self, **kw):
        """按目标查通知已读情况。GET /office/notice!findTargetRead.action"""
        return self.get("/office/notice!findTargetRead.action", dict(kw))

    def officeNotice(self, **kw):
        """公文通知。GET /office/notice!read.action"""
        return self.paged("/office/notice!read.action", dict(kw))


class AttachmentMixin(object):

    def attachmentsByIds(self, ids):
        """按 id 批量读附件。GET /system/attachment!readByIds.action?ids=a,b"""
        return self.get("/system/attachment!readByIds.action",
                        {"ids": ids if isinstance(ids, str) else ",".join(map(str, ids))})

    def myAttachments(self, **kw):
        """最近上传。GET /system/attachment!readByUser.action"""
        return self.paged("/system/attachment!readByUser.action", dict(kw))

    def downloadUrl(self, id):
        """下载直链（不下载内容，只给 URL）。"""
        return "%s/system/attachment!download.action?id=%s" % (self._base(), id)

    def _base(self):
        from Access.HttpTransport import BASE
        return BASE
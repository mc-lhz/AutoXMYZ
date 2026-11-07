"""综合素质评价（quality 域）：学业之外的十项记录。

对应端点前缀：`quality/`
面板：QualityPanel 统辖社团活动、党团活动、志愿服务、公益劳动、荣誉称号、
竞赛成绩、体育比赛、艺术活动、军事训练、生产劳动、社会调查、勤工俭学等。
"""


class QualityMixin(object):

    def quality(self, **kw):
        """我的综合素质评价总表（分页）。GET /quality/quality!read.action"""
        return self.paged("/quality/quality!read.action", dict(kw))

    def qualityDetail(self, id=None, **kw):
        """综评记录详情。GET /quality/quality-detail!detailJosn.action"""
        p = {"id": id}
        p.update(kw)
        return self.get("/quality/quality-detail!detailJosn.action", p)

    def qualityScoreStat(self, **kw):
        """综评得分统计。GET /quality/quality-score-stat!read.action"""
        return self.get("/quality/quality-score-stat!read.action", dict(kw))

    def selfDescription(self, **kw):
        """自我陈述报告。GET /quality/student-self-description!read.action"""
        return self.get("/quality/student-self-description!read.action", dict(kw))

    def honors(self, **kw):
        """先进个人荣誉称号。GET /quality/personal-honor!read.action"""
        return self.paged("/quality/personal-honor!read.action", dict(kw))

    def volunteerService(self, **kw):
        """志愿服务。GET /quality/volunteer-service!read.action"""
        return self.paged("/quality/volunteer-service!read.action", dict(kw))

    def volunteerLabour(self, **kw):
        """公益劳动。GET /quality/volunteer-labour!read.action"""
        return self.paged("/quality/volunteer-labour!read.action", dict(kw))

    def competitionResult(self, **kw):
        """学科竞赛成绩。GET /quality/competition-result!read.action"""
        return self.paged("/quality/competition-result!read.action", dict(kw))

    def sportsCompetition(self, **kw):
        """体育比赛项目。GET /quality/sports-competition!read.action"""
        return self.paged("/quality/sports-competition!read.action", dict(kw))

    def artActivity(self, **kw):
        """艺术活动。GET /quality/art-activity!read.action"""
        return self.paged("/quality/art-activity!read.action", dict(kw))

    def studentArt(self, **kw):
        """学生艺术。GET /quality/student-art!read.action"""
        return self.paged("/quality/student-art!read.action", dict(kw))

    def militaryTraining(self, **kw):
        """军事训练。GET /quality/military-training!read.action"""
        return self.paged("/quality/military-training!read.action", dict(kw))

    def productiveLabour(self, **kw):
        """生产劳动。GET /quality/productive-labour!read.action"""
        return self.paged("/quality/productive-labour!read.action", dict(kw))

    def socialSurvey(self, **kw):
        """社会调查。GET /quality/social-survey!read.action"""
        return self.paged("/quality/social-survey!read.action", dict(kw))

    def workStudy(self, **kw):
        """勤工俭学。GET /quality/work-study-program!read.action"""
        return self.paged("/quality/work-study-program!read.action", dict(kw))

    def learningOutcome(self, **kw):
        """科技创新与研究性学习成果。GET /quality/learning-outcome!read.action"""
        return self.paged("/quality/learning-outcome!read.action", dict(kw))

    def createInvention(self, **kw):
        """创造发明成果。GET /quality/create-invention!read.action"""
        return self.paged("/quality/create-invention!read.action", dict(kw))

    def typicalCase(self, **kw):
        """典型案例材料。GET /quality/typical-case-material!read.action"""
        return self.paged("/quality/typical-case-material!read.action", dict(kw))

    def partyActivity(self, **kw):
        """党团活动。GET /quality/party-activity!read.action"""
        return self.paged("/quality/party-activity!read.action", dict(kw))

    def communityActivity(self, **kw):
        """社团活动。GET /quality/community-activity!read.action"""
        return self.paged("/quality/community-activity!read.action", dict(kw))
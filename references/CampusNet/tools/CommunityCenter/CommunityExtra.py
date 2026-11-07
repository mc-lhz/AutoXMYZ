"""CommunityExtra —— 社团补齐：考试成绩查看、报名、出勤、课程下拉（6 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CommunityExtraMixin(object):
    """CommunityExtraMixin mixin（由 XMYZClient 组合）。"""

    def exportCommunityAttendance(self, **kw):
        """community/attendance!exportByStudent.action （出勤记录）"""
        return self.get('/community/attendance!exportByStudent.action', dict(kw))

    def readCommunityByRegister(self, **kw):
        """community/community!readByRegister.action （报名）"""
        return self.get('/community/community!readByRegister.action', dict(kw))

    def exportCommunityExamScore(self, **kw):
        """community/exam-score!exportByStudent.action （考试成绩查看）"""
        return self.get('/community/exam-score!exportByStudent.action', dict(kw))

    def importCommunityExamScore(self, **kw):
        """community/exam-score!imp.action （考试成绩查看）"""
        return self.post('/community/exam-score!imp.action', dict(kw))

    def stateByStudentCommunityExamScore(self, **kw):
        """community/exam-score!stateByStudent.action （考试成绩查看）"""
        return self.get('/community/exam-score!stateByStudent.action', dict(kw))

    def getCommunityLessonCombo(self, **kw):
        """community/lesson!getComboStore.action （考勤(组长/社长) / 社团任务提交）"""
        return self.get('/community/lesson!getComboStore.action', dict(kw))

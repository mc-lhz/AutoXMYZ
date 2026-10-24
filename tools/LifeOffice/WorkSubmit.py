"""WorkSubmit —— 作业查看及提交：内容/附件的保存与提交（8 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WorkSubmitMixin(object):
    """WorkSubmitMixin mixin（由 XMYZClient 组合）。"""

    def getComboStoreByMemberCommunity(self, **kw):
        """community/community!getComboStoreByMember.action （社团任务提交）"""
        return self.get('/community/community!getComboStoreByMember.action', dict(kw))

    def getSubmitWorkLessonCombo(self, **kw):
        """community/lesson!getComboStore.action （考勤(组长/社长) / 社团任务提交）"""
        return self.get('/community/lesson!getComboStore.action', dict(kw))

    def loadSubmitWork(self, **kw):
        """community/work!load.action （社团任务提交）"""
        return self.get('/community/work!load.action', dict(kw))

    def saveSubmitWorkAttachment(self, **kw):
        """community/work!saveAttachment.action （社团任务提交）"""
        return self.post('/community/work!saveAttachment.action', dict(kw))

    def saveSubmitWorkContent(self, **kw):
        """community/work!saveContent.action （社团任务提交）"""
        return self.post('/community/work!saveContent.action', dict(kw))

    def saveWorkDetail(self, **kw):
        """community/work-detail!save.action （社团任务提交）"""
        return self.post('/community/work-detail!save.action', dict(kw))

    def findWorkByStudentClassWork(self, **kw):
        """edu/class-work!findWorkByStudent.action （学生主页 / 作业查看及提交）"""
        return self.get('/edu/class-work!findWorkByStudent.action', dict(kw))

    def saveStudentWorkDetail(self, **kw):
        """edu/student-work-detail!save.action （学生主页 / 作业查看及提交）"""
        return self.post('/edu/student-work-detail!save.action', dict(kw))

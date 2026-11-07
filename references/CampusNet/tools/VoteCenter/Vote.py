"""Vote —— 投票系统：表单获取与投票（2 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class VoteMixin(object):
    """VoteMixin mixin（由 XMYZClient 组合）。"""

    def getFormVoteQuestion(self, **kw):
        """vote/question!getForm.action （投票）"""
        return self.get('/vote/question!getForm.action', dict(kw))

    def voteVoteResult(self, **kw):
        """vote/result!vote.action （学生主页 / 投票）"""
        return self.post('/vote/result!vote.action', dict(kw))

"""AccountExtras —— 账号扩展：家长角色、家长录入学生、学生照片上传（家长向）（3 个端点）。

学生向零引用端点收口（2026-10-25 全量终检）。
参数 **kw 透传（GET query / POST form）。详见同名 md。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AccountExtrasMixin(object):
    """AccountExtras mixin（由 XMYZClient 组合）。"""

    def readByStudentOrParentParentRole(self, **kw):
        """account/parent-role!readByStudentOrParent.action"""
        return self.get('/account/parent-role!readByStudentOrParent.action', dict(kw))

    def inputStudentByParentUser(self, **kw):
        """account/user!inputStudentByParent.action"""
        return self.post('/account/user!inputStudentByParent.action', dict(kw))

    def updateStudentFaceFileByParentUser(self, **kw):
        """account/user!updateStudentFaceFileByParent.action"""
        return self.post('/account/user!updateStudentFaceFileByParent.action', dict(kw))

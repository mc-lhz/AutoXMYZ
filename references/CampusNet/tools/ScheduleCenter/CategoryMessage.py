"""CategoryMessage —— 日常办公：个人日程（日历网格）与分类消息查看（5 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CategoryMessageMixin(object):
    """CategoryMessageMixin mixin（由 XMYZClient 组合）。"""

    def getSubCategoryMessageCategory(self, **kw):
        """message/category!getSubCategory.action （学生主页 / 新闻公告）"""
        return self.get('/message/category!getSubCategory.action', dict(kw))

    def findReadByParentMessageGrid(self, **kw):
        """message/message-grid!findReadByParent.action （学生主页 / 新闻公告）"""
        return self.get('/message/message-grid!findReadByParent.action', dict(kw))

    def findReadByStudentMessageGrid(self, **kw):
        """message/message-grid!findReadByStudent.action （学生主页 / 新闻公告）"""
        return self.get('/message/message-grid!findReadByStudent.action', dict(kw))

    def readMessageGridByCategory(self, **kw):
        """message/message-grid!readByCategory.action （学生主页 / 新闻公告）"""
        return self.get('/message/message-grid!readByCategory.action', dict(kw))

    def setReadMessageGrid(self, **kw):
        """message/message-grid!setRead.action （学生主页 / 新闻公告）"""
        return self.post('/message/message-grid!setRead.action', dict(kw))

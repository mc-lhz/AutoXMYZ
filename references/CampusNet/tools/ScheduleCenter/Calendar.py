"""Calendar —— 日常办公：个人日程（日历网格）与分类消息查看（10 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CalendarMixin(object):
    """CalendarMixin mixin（由 XMYZClient 组合）。"""

    def createCalendar(self, **kw):
        """office/calendar!create.action （个人日程安排）"""
        return self.post('/office/calendar!create.action', dict(kw))

    def destroyCalendar(self, **kw):
        """office/calendar!destroy.action （个人日程安排）"""
        return self.post('/office/calendar!destroy.action', dict(kw))

    def exportCalendar(self, **kw):
        """office/calendar!export.action （个人日程安排）"""
        return self.get('/office/calendar!export.action', dict(kw))

    def gridCreateCalendar(self, **kw):
        """office/calendar!gridCreate.action （个人日程安排）"""
        return self.post('/office/calendar!gridCreate.action', dict(kw))

    def gridDestroyCalendar(self, **kw):
        """office/calendar!gridDestroy.action （个人日程安排）"""
        return self.post('/office/calendar!gridDestroy.action', dict(kw))

    def gridReadCalendar(self, **kw):
        """office/calendar!gridRead.action （个人日程安排）"""
        return self.post('/office/calendar!gridRead.action', dict(kw))

    def gridUpdateCalendar(self, **kw):
        """office/calendar!gridUpdate.action （个人日程安排）"""
        return self.post('/office/calendar!gridUpdate.action', dict(kw))

    def importCalendar(self, **kw):
        """office/calendar!imp.action （个人日程安排）"""
        return self.post('/office/calendar!imp.action', dict(kw))

    def readCalendar(self, **kw):
        """office/calendar!read.action （个人日程安排）"""
        return self.get('/office/calendar!read.action', dict(kw))

    def updateCalendar(self, **kw):
        """office/calendar!update.action （个人日程安排）"""
        return self.post('/office/calendar!update.action', dict(kw))

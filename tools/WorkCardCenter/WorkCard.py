"""WorkCard —— 作业打卡：打卡记录与统计（5 个端点的薄包装）。

来源：菜单模块 JS 还原；读 GET / 写 POST（Struts2 表单）。
参数契约：**kw 原样透传（GET query / POST form），字段以页面抓包为准。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WorkCardMixin(object):
    """WorkCardMixin mixin（由 XMYZClient 组合）。"""

    def getWorkCardRecordWorkWorkCardWork(self, **kw):
        """work-card/work!getWorkCardRecordWork.action （打卡）"""
        return self.get('/work-card/work!getWorkCardRecordWork.action', dict(kw))

    def getComboStoreWorkCard(self, **kw):
        """work-card/work-card!getComboStore.action （打卡）"""
        return self.get('/work-card/work-card!getComboStore.action', dict(kw))

    def getComboStoreByStudentOrParentWorkCard(self, **kw):
        """work-card/work-card!getComboStoreByStudentOrParent.action （打卡）"""
        return self.get('/work-card/work-card!getComboStoreByStudentOrParent.action', dict(kw))

    def statPercentRankByStudentWorkCardRecord(self, **kw):
        """work-card/work-card-record!statPercentRankByStudent.action （打卡）"""
        return self.get('/work-card/work-card-record!statPercentRankByStudent.action', dict(kw))

    def updateWorkCardRecordWorkCardRecord(self, **kw):
        """work-card/work-card-record!updateWorkCardRecord.action （打卡）"""
        return self.post('/work-card/work-card-record!updateWorkCardRecord.action', dict(kw))

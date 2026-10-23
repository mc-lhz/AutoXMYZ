"""站内消息 —— 学社（api.xmyzstudent.com/api/v2）15 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MessageMixin(object):
    """MessageMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/messages/batch
    def deleteAdminMessagesBatch(self):
        path = '/admin/messages/batch'
        return self.delete(path)

    # -- DELETE /admin/messages/templates/{}
    def deleteAdminMessageTemplate(self, id):
        path = '/admin/messages/templates/{}'.format(id)
        return self.delete(path)

    # -- DELETE /admin/messages/{}
    def deleteAdminMessage(self, id):
        path = '/admin/messages/{}'.format(id)
        return self.delete(path)

    # -- DELETE /messages/{}
    def deleteMessage(self, id):
        path = '/messages/{}'.format(id)
        return self.delete(path)

    # -- GET /admin/messages
    def getAdminMessages(self, params=None, userId=None, type_=None, isRead=None, keyword=None, page=1, size=20):
        path = '/admin/messages'
        return self.get(path, params=_clean({"params": params, "userId": userId, "type_": type, "isRead": isRead, "keyword": keyword, "page": page, "size": size}))

    # -- GET /admin/messages/stats
    def getAdminMessageStats(self):
        path = '/admin/messages/stats'
        return self.get(path)

    # -- GET /admin/messages/templates
    def getAdminMessageTemplates(self, type_=None, status=None):
        path = '/admin/messages/templates'
        return self.get(path, params=_clean({'type': type_, 'status': status}))

    # -- GET /messages
    def getMessages(self, type_=None, isRead=None, page=1, size=20):
        path = '/messages'
        return self.get(path, params=_clean({"type_": type, "isRead": isRead, "page": page, "size": size}))

    # -- GET /messages/unread-count
    def getUnreadMessageCount(self):
        path = '/messages/unread-count'
        return self.get(path)

    # -- POST /admin/messages/broadcast
    def broadcastAdminMessage(self):
        path = '/admin/messages/broadcast'
        return self.post(path)

    # -- POST /admin/messages/send
    def sendAdminMessage(self):
        path = '/admin/messages/send'
        return self.post(path)

    # -- POST /admin/messages/templates
    def createAdminMessageTemplate(self):
        path = '/admin/messages/templates'
        return self.post(path)

    # -- PUT /admin/messages/templates/{}
    def updateAdminMessageTemplate(self, id):
        path = '/admin/messages/templates/{}'.format(id)
        return self.put(path)

    # -- PUT /messages/read-all
    def markAllMessagesRead(self, type_=None):
        path = '/messages/read-all'
        return self.put(path, _clean({'type_': type}))

    # -- PUT /messages/{}/read
    def markMessageRead(self, id):
        path = '/messages/{}/read'.format(id)
        return self.put(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

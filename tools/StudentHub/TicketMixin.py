"""电子票务 —— 学社（api.xmyzstudent.com/api/v2）20 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TicketMixin(object):
    """TicketMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/ticket/activities/{}
    def deleteAdminTicketActivities(self, id):
        path = '/admin/ticket/activities/{}'.format(id)
        return self.delete(path)

    # -- DELETE /admin/ticket/sessions/{}
    def deleteAdminTicketSessions(self, sessionId):
        path = '/admin/ticket/sessions/{}'.format(sessionId)
        return self.delete(path)

    # -- GET /admin/ticket/activities
    def getAdminTicketActivities(self, page=1, pageSize=10, status=None):
        path = '/admin/ticket/activities'
        return self.get(path, params=_clean({"page": page, "pageSize": pageSize, "status": status}))

    # -- GET /admin/ticket/activities/{}
    def getAdminTicketActivitiesById(self, id):
        path = '/admin/ticket/activities/{}'.format(id)
        return self.get(path)

    # -- GET /admin/ticket/activities/{}/review
    def getAdminTicketReview(self, id, page=1, pageSize=10, status=None, sessionId=None):
        path = '/admin/ticket/activities/{}/review'.format(id)
        return self.get(path, params=_clean({"id": id, "page": page, "pageSize": pageSize, "status": status, "sessionId": sessionId}))

    # -- GET /admin/ticket/activities/{}/stats
    def getAdminTicketActivitiesStats(self, id):
        path = '/admin/ticket/activities/{}/stats'.format(id)
        return self.get(path)

    # -- GET /admin/ticket/verify
    def getTicketByCode(self, code):
        path = '/admin/ticket/verify'
        return self.get(path, _clean({'code': code}))

    # -- GET /ticket-activities
    def getPublicTicketActivities(self, page=1, pageSize=10, status=None):
        path = '/ticket-activities'
        return self.get(path, params=_clean({"page": page, "pageSize": pageSize, "status": status}))

    # -- GET /ticket-activities/{}
    def getTicketActivitiesById(self, id):
        path = '/ticket-activities/{}'.format(id)
        return self.get(path)

    # -- GET /tickets/my
    def getTicketsMy(self):
        path = '/tickets/my'
        return self.get(path)

    # -- GET /tickets/my/activity/{}
    def getTicketsMyActivityById(self, id):
        path = '/tickets/my/activity/{}'.format(id)
        return self.get(path)

    # -- POST /admin/ticket/activities
    def createAdminTicketActivities(self, payload):
        path = '/admin/ticket/activities'
        return self.post(path)

    # -- POST /admin/ticket/activities/{}/sessions
    def createAdminTicketActivitiesSessions(self, id, payload):
        path = '/admin/ticket/activities/{}/sessions'.format(id)
        return self.post(path)

    # -- POST /admin/ticket/activities/{}/status
    def createAdminTicketActivitiesStatus(self, id, status):
        path = '/admin/ticket/activities/{}/status'.format(id)
        return self.post(path, json={"status": status})

    # -- POST /admin/ticket/tickets/batch-review
    def batchReviewAdminTicketTickets(self, payload):
        path = '/admin/ticket/tickets/batch-review'
        return self.post(path)

    # -- POST /admin/ticket/tickets/{}/review
    def reviewAdminTicketTickets(self, ticketId, payload):
        path = '/admin/ticket/tickets/{}/review'.format(ticketId)
        return self.post(path)

    # -- POST /admin/ticket/verify/use
    def useAdminTicketVerify(self, ticketCode):
        path = '/admin/ticket/verify/use'
        return self.post(path, json={"ticketCode": ticketCode})

    # -- POST /tickets/grab
    def grabTickets(self, payload):
        path = '/tickets/grab'
        return self.post(path)

    # -- PUT /admin/ticket/activities/{}
    def updateAdminTicketActivities(self, id, payload):
        path = '/admin/ticket/activities/{}'.format(id)
        return self.put(path)

    # -- PUT /admin/ticket/sessions/{}
    def updateAdminTicketSessions(self, sessionId, payload):
        path = '/admin/ticket/sessions/{}'.format(sessionId)
        return self.put(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

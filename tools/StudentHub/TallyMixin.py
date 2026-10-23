"""实时唱票 —— 学社（api.xmyzstudent.com/api/v2）11 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TallyMixin(object):
    """TallyMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/tally/activities/{}
    def deleteAdminTallyActivities(self, id):
        path = '/admin/tally/activities/{}'.format(id)
        return self.delete(path)

    # -- DELETE /admin/tally/candidates/{}
    def deleteAdminTallyCandidates(self, candidateId):
        path = '/admin/tally/candidates/{}'.format(candidateId)
        return self.delete(path)

    # -- GET /admin/tally/activities
    def getAdminTallyActivities(self):
        path = '/admin/tally/activities'
        return self.get(path)

    # -- GET /admin/tally/activities/{}
    def getAdminTallyActivitiesById(self, id):
        path = '/admin/tally/activities/{}'.format(id)
        return self.get(path)

    # -- GET /admin/tally/activities/{}/records
    def getAdminTallyActivitiesRecords(self, id):
        path = '/admin/tally/activities/{}/records'.format(id)
        return self.get(path)

    # -- POST /admin/tally/activities
    def createAdminTallyActivities(self, title):
        path = '/admin/tally/activities'
        return self.post(path, json={"title": title})

    # -- POST /admin/tally/activities/{}/candidates
    def createAdminTallyActivitiesCandidates(self, id, payload):
        path = '/admin/tally/activities/{}/candidates'.format(id)
        return self.post(path)

    # -- POST /admin/tally/activities/{}/undo
    def undoAdminTallyActivities(self, id):
        path = '/admin/tally/activities/{}/undo'.format(id)
        return self.post(path)

    # -- POST /admin/tally/candidates/{}/vote
    def voteAdminTallyCandidates(self, candidateId, delta):
        path = '/admin/tally/candidates/{}/vote'.format(candidateId)
        return self.post(path, json={"delta": delta})

    # -- PUT /admin/tally/activities/{}
    def updateAdminTallyActivities(self, id, payload):
        path = '/admin/tally/activities/{}'.format(id)
        return self.put(path)

    # -- PUT /admin/tally/candidates/{}
    def updateAdminTallyCandidates(self, candidateId, payload):
        path = '/admin/tally/candidates/{}'.format(candidateId)
        return self.put(path)

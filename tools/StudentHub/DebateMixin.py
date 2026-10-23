"""辩论场管理 —— 学社（api.xmyzstudent.com/api/v2）9 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DebateMixin(object):
    """DebateMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/debate/rounds/{}
    def deleteAdminDebateRounds(self, roundId):
        path = '/admin/debate/rounds/{}'.format(roundId)
        return self.delete(path)

    # -- GET /admin/debate/rounds
    def getAdminDebateRounds(self):
        path = '/admin/debate/rounds'
        return self.get(path)

    # -- POST /admin/debate/rounds
    def createAdminDebateRounds(self, payload):
        path = '/admin/debate/rounds'
        return self.post(path)

    # -- PUT /admin/debate/rounds/{}
    def updateAdminDebateRounds(self, roundId, payload):
        path = '/admin/debate/rounds/{}'.format(roundId)
        return self.put(path)

    # -- PUT /admin/debate/rounds/{}/active
    def updateAdminDebateRoundsActive(self, roundId):
        path = '/admin/debate/rounds/{}/active'.format(roundId)
        return self.put(path)

    # -- PUT /admin/debate/rounds/{}/lock
    def lockAdminDebateRounds(self, roundId):
        path = '/admin/debate/rounds/{}/lock'.format(roundId)
        return self.put(path)

    # -- PUT /admin/debate/rounds/{}/regenerate-password
    def regeneratePasswordAdminDebateRounds(self, roundId):
        path = '/admin/debate/rounds/{}/regenerate-password'.format(roundId)
        return self.put(path)

    # -- PUT /admin/debate/rounds/{}/reset
    def resetAdminDebateRounds(self, roundId):
        path = '/admin/debate/rounds/{}/reset'.format(roundId)
        return self.put(path)

    # -- PUT /admin/debate/rounds/{}/unlock
    def unlockAdminDebateRounds(self, id, extendSeconds):
        path = '/admin/debate/rounds/{}/unlock'.format(id)
        return self.put(path, params={'extendSeconds': extendSeconds})

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

    # ---------------- 2026-10 新版前端新增（公开投票 + 操作员台） ----------------

    # -- GET /debate/active
    def getActiveDebateRounds(self):
        """当前进行中的辩论场次（公开）。"""
        path = '/debate/active'
        return self.get(path)

    # -- GET /debate/round/{}
    def getDebateRoundById(self, id):
        path = '/debate/round/{}'.format(id)
        return self.get(path)

    # -- GET /debate/me
    def getMyDebateIdentity(self):
        """本人本场身份/可投票状态。"""
        path = '/debate/me'
        return self.get(path)

    # -- POST /debate/vote
    def submitDebateVote(self, payload):
        """投票；payload 键以线上站点为准（body 原样透传）。"""
        path = '/debate/vote'
        return self.post(path, json=payload)

    # -- GET /debate/results/{}
    def getDebateResultsById(self, id):
        path = '/debate/results/{}'.format(id)
        return self.get(path)

    # -- GET /debate/wechat/login
    def debateWechatLoginUrl(self, returnPath="/vote"):
        """构造微信登录跳转 URL（站点为 URL builder，不发请求）。"""
        return 'https://api.xmyzstudent.com/api/v2/debate/wechat/login?return=%s' % returnPath

    # -- POST /debate/operator/verify
    def verifyDebateOperator(self, roundId, password):
        """操作员核验口令，换取操作资格。"""
        path = '/debate/operator/verify'
        return self.post(path, json={'roundId': roundId, 'password': password})

    def _opHeaders(self, password):
        """操作员台统一用 X-Round-Password 头鉴权（非 Bearer）。"""
        return {'X-Round-Password': password}

    # -- PUT /debate/operator/rounds/{}
    def updateDebateOperatorRound(self, roundId, password, payload):
        path = '/debate/operator/rounds/{}'.format(roundId)
        return self.put(path, json=payload, headers=self._opHeaders(password))

    # -- PUT /debate/operator/rounds/{}/reset
    def resetDebateOperatorRound(self, roundId, password):
        path = '/debate/operator/rounds/{}/reset'.format(roundId)
        return self.put(path, headers=self._opHeaders(password))

    # -- PUT /debate/operator/rounds/{}/active
    def activateDebateOperatorRound(self, roundId, password):
        path = '/debate/operator/rounds/{}/active'.format(roundId)
        return self.put(path, headers=self._opHeaders(password))

    # -- PUT /debate/operator/rounds/{}/lock
    def lockDebateOperatorRound(self, roundId, password):
        path = '/debate/operator/rounds/{}/lock'.format(roundId)
        return self.put(path, headers=self._opHeaders(password))

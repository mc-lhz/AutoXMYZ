"""声音问答 —— 学社（api.xmyzstudent.com/api/v2）21 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VoicesMixin(object):
    """VoicesMixin mixin（由 StudentHubClient 组合）。"""

    # -- GET /admin/voices/answers
    def getAdminVoicesAnswers(self, params):
        path = '/admin/voices/answers'
        return self.get(path, params=params)

    # -- GET /admin/voices/questions
    def getAdminVoicesQuestions(self, params):
        path = '/admin/voices/questions'
        return self.get(path, params=params)

    # -- GET /admin/voices/reports
    def getAdminVoicesReports(self, params):
        path = '/admin/voices/reports'
        return self.get(path, params=params)

    # -- GET /admin/voices/stats
    def getAdminVoicesStats(self):
        path = '/admin/voices/stats'
        return self.get(path)

    # -- GET /voices/mine/answers
    def getMyAnswers(self, page=1, size=10):
        path = '/voices/mine/answers'
        return self.get(path, params=_clean({"page": page, "size": size}))

    # -- GET /voices/mine/favorites
    def getMyFavorites(self, page=1, size=10):
        path = '/voices/mine/favorites'
        return self.get(path, params=_clean({"page": page, "size": size}))

    # -- GET /voices/mine/questions
    def getMyQuestions(self, page=1, size=10):
        path = '/voices/mine/questions'
        return self.get(path, params=_clean({"page": page, "size": size}))

    # -- GET /voices/questions
    def getVoiceQuestions(self, params=None, scope='mine', sort='latest', targets=None, page=1, size=12):
        path = '/voices/questions'
        return self.get(path, params=_clean({"params": params, "scope": scope, "sort": sort, "targets": targets, "page": page, "size": size}))

    # -- GET /voices/questions/{}
    def getVoicesQuestions2(self, questionId):
        path = '/voices/questions/{}'.format(questionId)
        return self.get(path)

    # -- GET /voices/status
    def getVoicesStatus(self):
        path = '/voices/status'
        return self.get(path)

    # -- POST /voices/answers/{}/like
    def likeVoicesAnswers(self, answerId):
        path = '/voices/answers/{}/like'.format(answerId)
        return self.post(path)

    # -- POST /voices/identity
    def createVoicesIdentity(self, identity):
        path = '/voices/identity'
        return self.post(path, json={"identity": identity})

    # -- POST /voices/questions
    def createVoicesQuestions(self, content, targetIdentities):
        path = '/voices/questions'
        return self.post(path, json={"content": content, "targetIdentities": targetIdentities})

    # -- POST /voices/questions/{}/answers
    def createVoicesQuestionsAnswers(self, questionId, content):
        path = '/voices/questions/{}/answers'.format(questionId)
        return self.post(path, json={"content": content})

    # -- POST /voices/questions/{}/favorite
    def favoriteVoicesQuestions(self, questionId):
        path = '/voices/questions/{}/favorite'.format(questionId)
        return self.post(path)

    # -- POST /voices/report
    def reportVoices(self, targetType, targetId, reason):
        path = '/voices/report'
        return self.post(path, json={"targetType": targetType, "targetId": targetId, "reason": reason})

    # -- PUT /admin/voices/answers/{}/restore
    def restoreAdminVoicesAnswers(self, answerId):
        path = '/admin/voices/answers/{}/restore'.format(answerId)
        return self.put(path)

    # -- PUT /admin/voices/answers/{}/takedown
    def takedownAdminVoicesAnswers(self, answerId):
        path = '/admin/voices/answers/{}/takedown'.format(answerId)
        return self.put(path)

    # -- PUT /admin/voices/questions/{}/restore
    def restoreAdminVoicesQuestions(self, questionId):
        path = '/admin/voices/questions/{}/restore'.format(questionId)
        return self.put(path)

    # -- PUT /admin/voices/questions/{}/takedown
    def takedownAdminVoicesQuestions(self, questionId):
        path = '/admin/voices/questions/{}/takedown'.format(questionId)
        return self.put(path)

    # -- PUT /admin/voices/reports/{}/handle
    def handleAdminVoicesReports(self, reportId):
        path = '/admin/voices/reports/{}/handle'.format(reportId)
        return self.put(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

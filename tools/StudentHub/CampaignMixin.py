"""投票征集活动 —— 学社（api.xmyzstudent.com/api/v2）19 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CampaignMixin(object):
    """CampaignMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/review/submissions
    def deleteAdminReviewSubmissions(self, payload):
        path = '/admin/review/submissions'
        return self.delete(path, json=payload)

    # -- GET /admin/review/campaigns/{}/submissions
    def getAdminReviewCampaignsSubmissions(self, campaignId):
        path = '/admin/review/campaigns/{}/submissions'.format(campaignId)
        return self.get(path)

    # -- GET /admin/voting/campaigns/{}/results
    def getAdminVotingCampaignsResults(self, campaignId):
        path = '/admin/voting/campaigns/{}/results'.format(campaignId)
        return self.get(path)

    # -- GET /campaigns
    def getCampaigns(self):
        path = '/campaigns'
        return self.get(path)

    # -- GET /campaigns/{}
    def getCampaignsById(self, campaignId):
        path = '/campaigns/{}'.format(campaignId)
        return self.get(path)

    # -- GET /music/detail
    def getMusicDetail(self, musicId):
        path = '/music/detail'
        return self.get(path, _clean({'musicId': musicId}))

    # -- GET /music/search
    def searchMusic(self, keyword, page=1, pageSize=20):
        path = '/music/search'
        return self.get(path, params=_clean({"keyword": keyword, "page": page, "pageSize": pageSize}))

    # -- GET /music/url
    def getMusicUrl(self, musicId, quality=8):
        path = '/music/url'
        return self.get(path, params=_clean({"musicId": musicId, "quality": quality}))

    # -- GET /submissions/campaigns/{}
    def getSubmissionsCampaignsById(self, campaignId):
        path = '/submissions/campaigns/{}'.format(campaignId)
        return self.get(path)

    # -- GET /voting/campaigns/{}/config
    def getVotingCampaignsConfig(self, campaignId):
        path = '/voting/campaigns/{}/config'.format(campaignId)
        return self.get(path)

    # -- GET /voting/campaigns/{}/my-votes
    def getVotingCampaignsMyVotes(self, campaignId):
        path = '/voting/campaigns/{}/my-votes'.format(campaignId)
        return self.get(path)

    # -- GET /voting/campaigns/{}/options
    def getVotingOptions(self, id, buildingCode=None):
        path = '/voting/campaigns/{}/options'.format(id)
        return self.get(path, params=_clean({"id": id, "buildingCode": buildingCode}))

    # -- POST /admin/campaigns
    def createAdminCampaigns(self, payload):
        path = '/admin/campaigns'
        return self.post(path, json=payload)

    # -- POST /admin/campaigns/{}/activate
    def activateAdminCampaigns(self, campaignId):
        path = '/admin/campaigns/{}/activate'.format(campaignId)
        return self.post(path)

    # -- POST /admin/campaigns/{}/close
    def closeAdminCampaigns(self, campaignId):
        path = '/admin/campaigns/{}/close'.format(campaignId)
        return self.post(path)

    # -- POST /admin/campaigns/{}/stage-operation
    def stageOperationAdminCampaigns(self, campaignId, payload):
        path = '/admin/campaigns/{}/stage-operation'.format(campaignId)
        return self.post(path, json=payload)

    # -- POST /submissions
    def createResourceSubmissions(self, payload):
        path = '/submissions'
        return self.post(path, json=payload)

    # -- POST /voting/vote
    def voteVoting(self, payload):
        path = '/voting/vote'
        return self.post(path, json=payload)

    # -- PUT /admin/campaigns/{}
    def updateAdminCampaigns(self, campaignId, payload):
        path = '/admin/campaigns/{}'.format(campaignId)
        return self.put(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

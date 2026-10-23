"""校园博物馆 —— 学社（api.xmyzstudent.com/api/v2）26 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MuseumMixin(object):
    """MuseumMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/museum/events/{}
    def deleteAdminMuseumEvents(self, eventId):
        path = '/admin/museum/events/{}'.format(eventId)
        return self.delete(path)

    # -- DELETE /admin/museum/events/{}/blocks/{}
    def deleteAdminMuseumEventsBlocks(self, eventId, blockId):
        path = '/admin/museum/events/{}/blocks/{}'.format(eventId, blockId)
        return self.delete(path)

    # -- DELETE /admin/museum/moments/{}
    def deleteAdminMuseumMoments(self, momentId):
        path = '/admin/museum/moments/{}'.format(momentId)
        return self.delete(path)

    # -- DELETE /admin/museum/tags/{}
    def deleteAdminMuseumTags(self, tagId):
        path = '/admin/museum/tags/{}'.format(tagId)
        return self.delete(path)

    # -- GET /admin/museum/events
    def getAdminMuseumEvents(self, params):
        path = '/admin/museum/events'
        return self.get(path, params=params)

    # -- GET /admin/museum/events/{}
    def getAdminMuseumEventsById(self, eventId):
        path = '/admin/museum/events/{}'.format(eventId)
        return self.get(path)

    # -- GET /admin/museum/events/{}/blocks
    def getAdminMuseumEventsBlocks(self, eventId):
        path = '/admin/museum/events/{}/blocks'.format(eventId)
        return self.get(path)

    # -- GET /admin/museum/moments
    def getAdminMuseumMoments(self, params):
        path = '/admin/museum/moments'
        return self.get(path, params=params)

    # -- GET /admin/museum/tags
    def getAdminMuseumTags(self, params):
        path = '/admin/museum/tags'
        return self.get(path, params=params)

    # -- POST /admin/museum/events
    def createAdminMuseumEvents(self, payload):
        path = '/admin/museum/events'
        return self.post(path)

    # -- POST /admin/museum/events/batch
    def batchAdminMuseumEvents(self, payload):
        path = '/admin/museum/events/batch'
        return self.post(path)

    # -- POST /admin/museum/events/{}/blocks
    def createAdminMuseumEventsBlocks(self, eventId, payload):
        path = '/admin/museum/events/{}/blocks'.format(eventId)
        return self.post(path)

    # -- POST /admin/museum/events/{}/blocks/sort
    def sortAdminMuseumEventsBlocks(self, eventId, ids):
        path = '/admin/museum/events/{}/blocks/sort'.format(eventId)
        return self.post(path, json={"ids": ids})

    # -- POST /admin/museum/events/{}/feature
    def featureAdminMuseumEvents(self, eventId):
        path = '/admin/museum/events/{}/feature'.format(eventId)
        return self.post(path)

    # -- POST /admin/museum/events/{}/publish
    def publishAdminMuseumEvents(self, eventId):
        path = '/admin/museum/events/{}/publish'.format(eventId)
        return self.post(path)

    # -- POST /admin/museum/events/{}/unfeature
    def unfeatureAdminMuseumEvents(self, eventId):
        path = '/admin/museum/events/{}/unfeature'.format(eventId)
        return self.post(path)

    # -- POST /admin/museum/events/{}/unpublish
    def unpublishAdminMuseumEvents(self, eventId):
        path = '/admin/museum/events/{}/unpublish'.format(eventId)
        return self.post(path)

    # -- POST /admin/museum/moments/batch
    def batchAdminMuseumMoments(self, payload):
        path = '/admin/museum/moments/batch'
        return self.post(path)

    # -- POST /admin/museum/moments/{}/approve
    def approveAdminMuseumMoments(self, momentId):
        path = '/admin/museum/moments/{}/approve'.format(momentId)
        return self.post(path)

    # -- POST /admin/museum/moments/{}/reject
    def rejectAdminMuseumMoments(self, momentId, payload):
        path = '/admin/museum/moments/{}/reject'.format(momentId)
        return self.post(path)

    # -- POST /admin/museum/moments/{}/takedown
    def takedownAdminMuseumMoments(self, momentId, payload):
        path = '/admin/museum/moments/{}/takedown'.format(momentId)
        return self.post(path)

    # -- POST /admin/museum/tags
    def createAdminMuseumTags(self, payload):
        path = '/admin/museum/tags'
        return self.post(path)

    # -- POST /admin/museum/tags/{}/toggle-status
    def toggleStatusAdminMuseumTags(self, tagId):
        path = '/admin/museum/tags/{}/toggle-status'.format(tagId)
        return self.post(path)

    # -- PUT /admin/museum/events/{}
    def updateAdminMuseumEvents(self, eventId, payload):
        path = '/admin/museum/events/{}'.format(eventId)
        return self.put(path)

    # -- PUT /admin/museum/events/{}/blocks/{}
    def updateAdminMuseumEventsBlocks(self, eventId, blockId, payload):
        path = '/admin/museum/events/{}/blocks/{}'.format(eventId, blockId)
        return self.put(path)

    # -- PUT /admin/museum/tags/{}
    def updateAdminMuseumTags(self, tagId, payload):
        path = '/admin/museum/tags/{}'.format(tagId)
        return self.put(path)

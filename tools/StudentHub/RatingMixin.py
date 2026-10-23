"""评分社区 —— 学社（api.xmyzstudent.com/api/v2）74 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RatingMixin(object):
    """RatingMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /rating-community/comments/{}
    def deleteRatingCommunityComments(self, commentId):
        path = '/rating-community/comments/{}'.format(commentId)
        return self.delete(path)

    # -- GET /rating-community/categories/{}
    def getRatingCommunityCategoriesById(self, categoryId):
        path = '/rating-community/categories/{}'.format(categoryId)
        return self.get(path)

    # -- GET /rating-community/collections
    def getRatingCommunityCollections(self):
        path = '/rating-community/collections'
        return self.get(path)

    # -- GET /rating-community/collections/{}
    def getRatingCommunityCollectionsById(self, collectionId):
        path = '/rating-community/collections/{}'.format(collectionId)
        return self.get(path)

    # -- GET /rating-community/contributions/history
    def getContributionHistory(self, targetType, targetId):
        path = '/rating-community/contributions/history'
        return self.get(path, params=_clean({"targetType": targetType, "targetId": targetId}))

    # -- GET /rating-community/contributions/my
    def getRatingCommunityContributionsMy(self, params):
        path = '/rating-community/contributions/my'
        return self.get(path, params=params)

    # -- GET /rating-community/hot-items
    def getHotRatingItems(self, count=None):
        path = '/rating-community/hot-items'
        return self.get(path, _clean({'count': count}))

    # -- GET /rating-community/major-sections/{}/minor-sections
    def getRatingCommunityMajorSectionsMinorSectionsById(self, sectionId):
        path = '/rating-community/major-sections/{}/minor-sections'.format(sectionId)
        return self.get(path)

    # -- GET /rating-community/minor-sections/{}/rating-items
    def getRatingCommunityMinorSectionsRatingItemsById(self, sectionId):
        path = '/rating-community/minor-sections/{}/rating-items'.format(sectionId)
        return self.get(path)

    # -- GET /rating-community/random-items
    def getRandomRatingItems(self, schoolId=None, count=None):
        path = '/rating-community/random-items'
        return self.get(path, params=_clean({"schoolId": schoolId, "count": count}))

    # -- GET /rating-community/rating-items/{}
    def getRatingCommunityRatingItemsById(self, itemId):
        path = '/rating-community/rating-items/{}'.format(itemId)
        return self.get(path)

    # -- GET /rating-community/schools/{}/categories
    def getRatingCommunitySchoolsCategoriesById(self, schoolId):
        path = '/rating-community/schools/{}/categories'.format(schoolId)
        return self.get(path)

    # -- GET /rating-community/search
    def searchRatingItems(self, keyword):
        path = '/rating-community/search'
        return self.get(path, _clean({'keyword': keyword}))

    # -- POST /rating-community/comments
    def createRatingCommunityComments(self, payload):
        path = '/rating-community/comments'
        return self.post(path)

    # -- POST /rating-community/contributions
    def createRatingCommunityContributions(self, payload):
        path = '/rating-community/contributions'
        return self.post(path)

    # -- POST /rating-community/contributions/batch-rating-items
    def batchRatingItemsRatingCommunityContributions(self, payload):
        path = '/rating-community/contributions/batch-rating-items'
        return self.post(path)

    # -- POST /rating-community/contributions/upload-image
    def uploadContributionImage(self, filepath):
        return self.upload('/rating-community/contributions/upload-image', filepath, businessType='comment_image')

    # -- POST /rating-community/likes
    def createRatingCommunityLikes(self, commentId):
        path = '/rating-community/likes'
        return self.post(path, json={"commentId": commentId})

    # -- POST /rating-community/ratings
    def createRatingCommunityRatings(self, payload):
        path = '/rating-community/ratings'
        return self.post(path)

    # -- GET /admin/rating-community/statistics/overview
    def getStatisticsOverview(self):
        path = '/admin/rating-community/statistics/overview'
        return self.get(path)

    # -- GET /admin/rating-community/statistics/daily-ratings
    def getStatisticsDailyRatings(self, params):
        path = '/admin/rating-community/statistics/daily-ratings'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/schools
    def getSchoolsById2(self, params):
        path = '/admin/rating-community/schools'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/schools/{}
    def getSchoolsById(self, schoolId):
        path = '/admin/rating-community/schools/{}'.format(schoolId)
        return self.get(path)

    # -- POST /admin/rating-community/schools
    def createSchools(self, payload):
        path = '/admin/rating-community/schools'
        return self.post(path)

    # -- PUT /admin/rating-community/schools/{}
    def updateSchools(self, schoolId, payload):
        path = '/admin/rating-community/schools/{}'.format(schoolId)
        return self.put(path)

    # -- DELETE /admin/rating-community/schools/{}
    def deleteSchools(self, schoolId):
        path = '/admin/rating-community/schools/{}'.format(schoolId)
        return self.delete(path)

    # -- PUT /admin/rating-community/schools/{}/status
    def updateSchoolsStatus(self, schoolId, payload):
        path = '/admin/rating-community/schools/{}/status'.format(schoolId)
        return self.put(path)

    # -- GET /admin/rating-community/major-sections
    def getMajorSectionsById(self, params):
        path = '/admin/rating-community/major-sections'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/major-sections/{}
    def getMajorSectionsById2(self, sectionId):
        path = '/admin/rating-community/major-sections/{}'.format(sectionId)
        return self.get(path)

    # -- POST /admin/rating-community/major-sections
    def createMajorSections(self, payload):
        path = '/admin/rating-community/major-sections'
        return self.post(path)

    # -- PUT /admin/rating-community/major-sections/{}
    def updateMajorSections(self, sectionId, payload):
        path = '/admin/rating-community/major-sections/{}'.format(sectionId)
        return self.put(path)

    # -- DELETE /admin/rating-community/major-sections/{}
    def deleteMajorSections(self, sectionId):
        path = '/admin/rating-community/major-sections/{}'.format(sectionId)
        return self.delete(path)

    # -- PUT /admin/rating-community/major-sections/{}/status
    def updateMajorSectionsStatus(self, sectionId, payload):
        path = '/admin/rating-community/major-sections/{}/status'.format(sectionId)
        return self.put(path)

    # -- DELETE /admin/rating-community/major-sections/{}/image
    def deleteMajorSectionsImage(self, sectionId):
        path = '/admin/rating-community/major-sections/{}/image'.format(sectionId)
        return self.delete(path)

    # -- GET /admin/rating-community/minor-sections
    def getMinorSectionsById(self, params):
        path = '/admin/rating-community/minor-sections'
        return self.get(path, params=params)

    # -- POST /admin/rating-community/minor-sections
    def createMinorSections(self, payload):
        path = '/admin/rating-community/minor-sections'
        return self.post(path)

    # -- PUT /admin/rating-community/minor-sections/{}
    def updateMinorSections(self, sectionId, payload):
        path = '/admin/rating-community/minor-sections/{}'.format(sectionId)
        return self.put(path)

    # -- DELETE /admin/rating-community/minor-sections/{}
    def deleteMinorSections(self, sectionId):
        path = '/admin/rating-community/minor-sections/{}'.format(sectionId)
        return self.delete(path)

    # -- PUT /admin/rating-community/minor-sections/{}/status
    def updateMinorSectionsStatus(self, sectionId, payload):
        path = '/admin/rating-community/minor-sections/{}/status'.format(sectionId)
        return self.put(path)

    # -- DELETE /admin/rating-community/minor-sections/{}/image
    def deleteMinorSectionsImage(self, sectionId):
        path = '/admin/rating-community/minor-sections/{}/image'.format(sectionId)
        return self.delete(path)

    # -- GET /admin/rating-community/categories
    def getCategoriesById2(self, params):
        path = '/admin/rating-community/categories'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/categories/{}
    def getCategoriesById(self, categoryId):
        path = '/admin/rating-community/categories/{}'.format(categoryId)
        return self.get(path)

    # -- POST /admin/rating-community/categories
    def createCategories(self, payload):
        path = '/admin/rating-community/categories'
        return self.post(path)

    # -- PUT /admin/rating-community/categories/{}
    def updateCategories(self, categoryId, payload):
        path = '/admin/rating-community/categories/{}'.format(categoryId)
        return self.put(path)

    # -- DELETE /admin/rating-community/categories/{}
    def deleteCategories(self, categoryId):
        path = '/admin/rating-community/categories/{}'.format(categoryId)
        return self.delete(path)

    # -- PUT /admin/rating-community/categories/{}/status
    def updateCategoriesStatus(self, categoryId, payload):
        path = '/admin/rating-community/categories/{}/status'.format(categoryId)
        return self.put(path)

    # -- DELETE /admin/rating-community/categories/{}/image
    def deleteCategoriesImage(self, categoryId):
        path = '/admin/rating-community/categories/{}/image'.format(categoryId)
        return self.delete(path)

    # -- GET /admin/rating-community/rating-items
    def getRatingItemsById(self, params):
        path = '/admin/rating-community/rating-items'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/rating-items/{}
    def getRatingItemsById2(self, itemId):
        path = '/admin/rating-community/rating-items/{}'.format(itemId)
        return self.get(path)

    # -- POST /admin/rating-community/rating-items
    def createRatingItems(self, payload):
        path = '/admin/rating-community/rating-items'
        return self.post(path)

    # -- PUT /admin/rating-community/rating-items/{}
    def updateRatingItems(self, itemId, payload):
        path = '/admin/rating-community/rating-items/{}'.format(itemId)
        return self.put(path)

    # -- DELETE /admin/rating-community/rating-items/{}
    def deleteRatingItems(self, itemId):
        path = '/admin/rating-community/rating-items/{}'.format(itemId)
        return self.delete(path)

    # -- PUT /admin/rating-community/rating-items/{}/status
    def updateRatingItemsStatus(self, itemId, payload):
        path = '/admin/rating-community/rating-items/{}/status'.format(itemId)
        return self.put(path)

    # -- DELETE /admin/rating-community/rating-items/{}/image
    def deleteRatingItemsImage(self, itemId):
        path = '/admin/rating-community/rating-items/{}/image'.format(itemId)
        return self.delete(path)

    # -- GET /admin/rating-community/comments
    def getCommentsById(self, params):
        path = '/admin/rating-community/comments'
        return self.get(path, params=params)

    # -- DELETE /admin/rating-community/comments/{}
    def deleteComments(self, commentId):
        path = '/admin/rating-community/comments/{}'.format(commentId)
        return self.delete(path)

    # -- DELETE /admin/rating-community/comments/batch
    def batchComments(self, payload):
        path = '/admin/rating-community/comments/batch'
        return self.delete(path, json=payload)

    # -- GET /admin/rating-community/ratings
    def getRatingsById(self, params):
        path = '/admin/rating-community/ratings'
        return self.get(path, params=params)

    # -- DELETE /admin/rating-community/ratings/{}
    def deleteRatings(self, ratingId):
        path = '/admin/rating-community/ratings/{}'.format(ratingId)
        return self.delete(path)

    # -- DELETE /admin/rating-community/ratings/batch
    def batchRatings(self, payload):
        path = '/admin/rating-community/ratings/batch'
        return self.delete(path, json=payload)

    # -- GET /admin/rating-community/collections
    def getCollectionsById(self, params):
        path = '/admin/rating-community/collections'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/collections/{}
    def getCollectionsById2(self, collectionId):
        path = '/admin/rating-community/collections/{}'.format(collectionId)
        return self.get(path)

    # -- POST /admin/rating-community/collections
    def createCollections(self, payload):
        path = '/admin/rating-community/collections'
        return self.post(path)

    # -- PUT /admin/rating-community/collections/{}
    def updateCollections(self, collectionId, payload):
        path = '/admin/rating-community/collections/{}'.format(collectionId)
        return self.put(path)

    # -- DELETE /admin/rating-community/collections/{}
    def deleteCollections(self, collectionId):
        path = '/admin/rating-community/collections/{}'.format(collectionId)
        return self.delete(path)

    # -- PUT /admin/rating-community/collections/{}/status
    def updateCollectionsStatus(self, collectionId, payload):
        path = '/admin/rating-community/collections/{}/status'.format(collectionId)
        return self.put(path)

    # -- DELETE /admin/rating-community/collections/{}/image
    def deleteCollectionsImage(self, collectionId):
        path = '/admin/rating-community/collections/{}/image'.format(collectionId)
        return self.delete(path)

    # -- GET /admin/rating-community/collections/{}/items
    def getCollectionsItemsById(self, collectionId, params):
        path = '/admin/rating-community/collections/{}/items'.format(collectionId)
        return self.get(path, json={"params": params})

    # -- POST /admin/rating-community/collections/{}/items
    def createCollectionsItems(self, collectionId, payload):
        path = '/admin/rating-community/collections/{}/items'.format(collectionId)
        return self.post(path)

    # -- DELETE /admin/rating-community/collections/{}/items/{}
    def deleteCollectionsItems(self, collectionId, itemId):
        path = '/admin/rating-community/collections/{}/items/{}'.format(collectionId, itemId)
        return self.delete(path)

    # -- PUT /admin/rating-community/collections/{}/items/{}/sort
    def sortCollectionsItems(self, collectionId, itemId, payload):
        path = '/admin/rating-community/collections/{}/items/{}/sort'.format(collectionId, itemId)
        return self.put(path)

    # -- GET /admin/rating-community/contributions
    def getContributionsById(self, params):
        path = '/admin/rating-community/contributions'
        return self.get(path, params=params)

    # -- GET /admin/rating-community/contributions/pending-count
    def getContributionsPendingCount(self):
        path = '/admin/rating-community/contributions/pending-count'
        return self.get(path)

    # -- POST /admin/rating-community/contributions/{}/review
    def reviewContributions(self, contributionId, payload):
        path = '/admin/rating-community/contributions/{}/review'.format(contributionId)
        return self.post(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

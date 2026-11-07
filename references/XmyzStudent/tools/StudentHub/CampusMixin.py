"""校区楼宇时段 + 用户检索 —— 学社（api.xmyzstudent.com/api/v2）19 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CampusMixin(object):
    """CampusMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/buildings/time-periods
    def deleteAdminBuildingsTimePeriods(self, payload):
        path = '/admin/buildings/time-periods'
        return self.delete(path, json=payload)

    # -- DELETE /admin/buildings/{}
    def deleteAdminBuildings(self, buildingId):
        path = '/admin/buildings/{}'.format(buildingId)
        return self.delete(path)

    # -- DELETE /admin/campuses/{}
    def deleteAdminCampuses(self, campusId):
        path = '/admin/campuses/{}'.format(campusId)
        return self.delete(path)

    # -- DELETE /admin/time-periods/{}
    def deleteAdminResourceTimePeriods(self, periodId):
        path = '/admin/time-periods/{}'.format(periodId)
        return self.delete(path)

    # -- GET /admin/users/search/by-campus-account
    def searchUsersByCampusAccount(self, campusAccount):
        path = '/admin/users/search/by-campus-account'
        return self.get(path, _clean({'campusAccount': campusAccount}))

    # -- GET /admin/users/search/by-campus-name
    def searchUsersByCampusName(self, name):
        path = '/admin/users/search/by-campus-name'
        return self.get(path, _clean({'name': name}))

    # -- GET /admin/users/search/by-user
    def searchUsersByUser(self, params=None):
        path = '/admin/users/search/by-user'
        return self.get(path, params=_clean({"params": params}))

    # -- GET /buildings
    def getBuildings(self, params):
        path = '/buildings'
        return self.get(path, json={"params": params})

    # -- GET /buildings/{}/time-periods
    def getBuildingsTimePeriods(self, buildingId):
        path = '/buildings/{}/time-periods'.format(buildingId)
        return self.get(path)

    # -- GET /campuses
    def getCampuses(self):
        path = '/campuses'
        return self.get(path)

    # -- GET /campuses/{}/buildings
    def getCampusesBuildingsById(self, campusId):
        path = '/campuses/{}/buildings'.format(campusId)
        return self.get(path)

    # -- GET /time-periods
    def getResourceTimePeriods(self):
        path = '/time-periods'
        return self.get(path)

    # -- POST /admin/buildings
    def createAdminBuildings(self, payload):
        path = '/admin/buildings'
        return self.post(path, json=payload)

    # -- POST /admin/buildings/time-periods
    def createAdminBuildingsTimePeriods(self, payload):
        path = '/admin/buildings/time-periods'
        return self.post(path, json=payload)

    # -- POST /admin/campuses
    def createAdminCampuses(self, payload):
        path = '/admin/campuses'
        return self.post(path, json=payload)

    # -- POST /admin/time-periods
    def createAdminResourceTimePeriods(self, payload):
        path = '/admin/time-periods'
        return self.post(path, json=payload)

    # -- PUT /admin/buildings/{}
    def updateAdminBuildings(self, buildingId, payload):
        path = '/admin/buildings/{}'.format(buildingId)
        return self.put(path)

    # -- PUT /admin/campuses/{}
    def updateAdminCampuses(self, campusId, payload):
        path = '/admin/campuses/{}'.format(campusId)
        return self.put(path)

    # -- PUT /admin/time-periods/{}
    def updateAdminResourceTimePeriods(self, periodId, payload):
        path = '/admin/time-periods/{}'.format(periodId)
        return self.put(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

"""门户（横幅/年级/文件/音乐） —— 学社（api.xmyzstudent.com/api/v2）17 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PortalMixin(object):
    """PortalMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /admin/banners/{}
    def deleteAdminBanner(self, id):
        path = '/admin/banners/{}'.format(id)
        return self.delete(path)

    # -- DELETE /grade/unbind
    def unbindGrade(self):
        path = '/grade/unbind'
        return self.delete(path)

    # -- GET /admin/banners
    def getAdminBanners(self, params):
        path = '/admin/banners'
        return self.get(path, params=params)

    # -- GET /banners
    def getPublicBanners(self, position=None):
        path = '/banners'
        return self.get(path, _clean({'position': position}))

    # -- GET /campus/captcha
    def getCampusCaptcha(self):
        path = '/campus/captcha'
        return self.get(path)

    # -- GET /grade/exams
    def getGradeExams(self, page=1, pageSize=10):
        path = '/grade/exams'
        return self.get(path, params=_clean({"page": page, "pageSize": pageSize}))

    # -- GET /grade/exams/{}
    def getGradeExamsById(self, examId):
        path = '/grade/exams/{}'.format(examId)
        return self.get(path)

    # -- GET /grade/status
    def getGradeStatus(self):
        path = '/grade/status'
        return self.get(path)

    # -- GET /qqmusic/auth/qrcode
    def getQQMusicQrCode(self):
        path = '/qqmusic/auth/qrcode'
        return self.get(path)

    # -- GET /qqmusic/auth/qrcode/status
    def getQQMusicQrStatus(self, qrKey):
        path = '/qqmusic/auth/qrcode/status'
        return self.get(path, _clean({'qrKey': qrKey}))

    # -- GET /qqmusic/auth/status
    def getQQMusicAuthStatus(self):
        path = '/qqmusic/auth/status'
        return self.get(path)

    # -- GET /qqmusic/qualities
    def getQQMusicQualities(self):
        path = '/qqmusic/qualities'
        return self.get(path)

    # -- POST /admin/banners
    def createAdminBanner(self, payload):
        path = '/admin/banners'
        return self.post(path)

    # -- POST /admin/banners/{}/toggle-status
    def toggleAdminBannerStatus(self, id):
        path = '/admin/banners/{}/toggle-status'.format(id)
        return self.post(path)

    # -- POST /files/upload
    def uploadFile(self, filepath, businessType=None):
        return self.upload('/files/upload', filepath, businessType=businessType, btField='business_type')

    # -- POST /grade/bind
    def bindGrade(self, payload):
        path = '/grade/bind'
        return self.post(path)

    # -- PUT /admin/banners/{}
    def updateAdminBanner(self, id, payload):
        path = '/admin/banners/{}'.format(id)
        return self.put(path)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

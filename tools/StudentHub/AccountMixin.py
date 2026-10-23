"""账号与会话（auth/user/sms/permissions） —— 学社（api.xmyzstudent.com/api/v2）29 个端点的薄包装。

来源：镜像 bundle 接口层导出名（保持站点语义命名），签名按镜像函数体还原。
本文件由构建流水线生成骨架后人工校对；改端点契约请同步 HubEndpoints.py。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AccountMixin(object):
    """AccountMixin mixin（由 StudentHubClient 组合）。"""

    # -- DELETE /sms/unbind
    def unbindSms(self):
        path = '/sms/unbind'
        return self.delete(path)

    # -- DELETE /user/unbind-campus
    def unbindCampus(self):
        path = '/user/unbind-campus'
        return self.delete(path)

    # -- DELETE /user/unbind-qq
    def unbindQQ(self):
        path = '/user/unbind-qq'
        return self.delete(path)

    # -- GET /auth/qq/authorize-url
    def getQQAuthorizeUrl(self):
        path = '/auth/qq/authorize-url'
        return self.get(path)

    # -- GET /permissions/my
    def getMyPermissions(self):
        path = '/permissions/my'
        return self.get(path)

    # -- GET /sms/binding
    def getSmsBinding(self):
        path = '/sms/binding'
        return self.get(path)

    # -- GET /user/campus-binding
    def getCampusBinding(self):
        path = '/user/campus-binding'
        return self.get(path)

    # -- GET /user/has-password
    def getHasPassword(self):
        path = '/user/has-password'
        return self.get(path)

    # -- GET /user/privacy-settings
    def getPrivacySettings(self):
        path = '/user/privacy-settings'
        return self.get(path)

    # -- GET /user/profile
    def getMyProfile(self):
        path = '/user/profile'
        return self.get(path)

    # -- GET /user/qq-binding
    def getQQBinding(self):
        path = '/user/qq-binding'
        return self.get(path)

    # -- GET /user/qq/authorize-url
    def getUserQQAuthorizeUrl(self):
        path = '/user/qq/authorize-url'
        return self.get(path)

    # -- GET /user/users/{}/avatar
    def getUserAvatar(self, id):
        path = '/user/users/{}/avatar'.format(id)
        return self.get(path)

    # -- GET /user/users/{}/profile
    def getUserProfile(self, id):
        path = '/user/users/{}/profile'.format(id)
        return self.get(path)

    # -- POST /auth/login
    def login(self):
        path = '/auth/login'
        return self.post(path)

    # -- POST /auth/qq-bind
    def qqBind(self, username, password, qqData):
        path = '/auth/qq-bind'
        return self.post(path, json={'username': username, 'password': password, 'qqData': qqData})

    # -- POST /auth/qq-login
    def qqLogin(self, code, state):
        path = '/auth/qq-login'
        return self.post(path, json={"code": code, "state": state})

    # -- POST /auth/qq-register
    def qqRegister(self, username, password, qqData):
        path = '/auth/qq-register'
        return self.post(path, json={'username': username, 'password': password, 'qqData': qqData})

    # -- POST /auth/register
    def register(self, username, password):
        path = '/auth/register'
        return self.post(path, json={'username': username, 'password': password})

    # -- POST /sms/bind
    def bindSms(self, phoneNumber, code):
        path = '/sms/bind'
        return self.post(path, json={"phoneNumber": phoneNumber, "code": code})

    # -- POST /sms/login
    def smsLogin(self, phoneNumber, code):
        path = '/sms/login'
        return self.post(path, json={"phoneNumber": phoneNumber, "code": code})

    # -- POST /sms/send
    def sendSmsCode(self, phoneNumber, purpose):
        path = '/sms/send'
        return self.post(path, json={"phoneNumber": phoneNumber, "code": code})

    # -- POST /user/avatar
    def uploadMyAvatar(self, filepath):
        return self.upload('/user/avatar', filepath)

    # -- POST /user/bind-campus
    def bindCampus(self):
        path = '/user/bind-campus'
        return self.post(path)

    # -- POST /user/bind-qq
    def bindQQ(self):
        path = '/user/bind-qq'
        return self.post(path)

    # -- POST /user/rebind-campus
    def rebindCampus(self):
        path = '/user/rebind-campus'
        return self.post(path)

    # -- PUT /user/password
    def updatePassword(self):
        path = '/user/password'
        return self.put(path)

    # -- PUT /user/privacy-settings
    def updatePrivacySettings(self, payload):
        path = '/user/privacy-settings'
        return self.put(path)

    # -- PUT /user/profile
    def updateMyProfile(self):
        path = '/user/profile'
        return self.put(path)

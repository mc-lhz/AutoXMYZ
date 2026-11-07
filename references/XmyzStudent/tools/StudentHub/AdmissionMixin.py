"""AdmissionMixin —— 学社纳新/准入域（admission，13 个端点）。

2026-10 从线上新版前端 bundle（index-D2vbWxba.js）调用点反推：
镜像仓库里没有这一域（镜像早于该功能上线）。
- 管理端：分组/成员/豁免/踢出/重发/扫码/修复（scan 60s、scan-fix 180s 长超时）
- 用户端：状态、QQ 档案、token 换取、验证、确认接管
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AdmissionMixin(object):
    """纳新/准入 mixin（由 StudentHubClient 组合）。"""

    # -- GET /admission/status
    def getAdmissionStatus(self):
        path = '/admission/status'
        return self.get(path)

    # -- GET /admission/qq-profile
    def getAdmissionQQProfile(self, qqNumber):
        path = '/admission/qq-profile'
        return self.get(path, _clean({'qqNumber': qqNumber}))

    # -- GET /admission/token/{}
    def getAdmissionTokenByQQ(self, qq):
        path = '/admission/token/{}'.format(qq)
        return self.get(path)

    # -- POST /admission/verify
    def verifyAdmission(self, payload):
        path = '/admission/verify'
        return self.post(path, json=payload)

    # -- POST /admission/confirm
    def confirmAdmission(self, sessionId, takeover=None):
        """confirm 接管会话；站点对它设置了长超时。"""
        path = '/admission/confirm'
        return self.post(path, json=_clean({'sessionId': sessionId, 'takeover': takeover}))

    # -- GET /admin/admission/groups
    def getAdminAdmissionGroups(self):
        path = '/admin/admission/groups'
        return self.get(path)

    # -- GET /admin/admission/members
    def getAdminAdmissionMembers(self, params=None):
        path = '/admin/admission/members'
        return self.get(path, params=params)

    # -- POST /admin/admission/exempt
    def exemptAdminAdmission(self, groupId, qqNumber, note=None):
        """豁免成员。"""
        path = '/admin/admission/exempt'
        return self.post(path, json=_clean(
            {'groupId': groupId, 'qqNumber': qqNumber, 'note': note}))

    # -- POST /admin/admission/revoke-exempt
    def revokeExemptAdminAdmission(self, groupId, qqNumber):
        path = '/admin/admission/revoke-exempt'
        return self.post(path, json={'groupId': groupId, 'qqNumber': qqNumber})

    # -- POST /admin/admission/kick
    def kickAdminAdmission(self, groupId, qqNumber):
        """踢出成员。"""
        path = '/admin/admission/kick'
        return self.post(path, json={'groupId': groupId, 'qqNumber': qqNumber})

    # -- POST /admin/admission/resend
    def resendAdminAdmission(self, groupId, qqNumber):
        path = '/admin/admission/resend'
        return self.post(path, json={'groupId': groupId, 'qqNumber': qqNumber})

    # -- GET /admin/admission/scan
    def scanAdminAdmission(self, groupId):
        """触发纳新扫码核对；站点设 60s 长超时。"""
        path = '/admin/admission/scan'
        return self.get(path, _clean({'groupId': groupId}), timeout=60)

    # -- POST /admin/admission/scan-fix
    def fixAdminAdmissionScan(self, groupId, qqNumbers):
        """批量修复扫码状态；站点设 180s 长超时。"""
        path = '/admin/admission/scan-fix'
        return self.post(path, json={'groupId': groupId, 'qqNumbers': qqNumbers},
                         timeout=180)


def _clean(d):
    """去掉值为 None 的查询参数。"""
    return {k: v for k, v in d.items() if v is not None}

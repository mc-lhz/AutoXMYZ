"""门面：组合各业务域 mixin，对外 API 就是 XMYZClient。

用法：
    from XMYZClient import XMYZClient
    c = XMYZClient()                       # 自动读 reference/.session.json
    c = XMYZClient(token="<JSESSIONID>")
    c = XMYZClient(cookie={"JSESSIONID": "..."})
    print(c.status()["loginName"])
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Access.HttpTransport import Http, XmyzError, WriteDenied  # noqa: F401,E402
from StudentBase.ProfileDict import ProfileMixin, DictMixin  # noqa: E402
from LifeOffice.StudyMessage import StudyMixin, MessageMixin, AttachmentMixin  # noqa: E402
from QualityCenter.QualityRead import QualityMixin  # noqa: E402
from CommunityCenter.VolunteerRead import CommunityMixin, VolunteerMixin  # noqa: E402


class XMYZClient(ProfileMixin, DictMixin, StudyMixin, MessageMixin,
                  AttachmentMixin, QualityMixin, CommunityMixin,
                  VolunteerMixin, Http):
    """厦门一中信息校园综合应用系统 —— **纯只读**客户端。

    写操作在 `Access/HttpTransport.py::_guard` 处被强制拦截，
    本类不提供任何绕过入口。
    """

    def healthCheck(self):
        """连通性与会话自检。

        ⚠️ 判据不能用 `loggedIn` 字段——**未登录时** `/account/user!status.action`
        返回 `{"success":true,"loggedIn":false,"principalSize":N}`，
        而**登录后该字段直接消失**，只剩 profile 字段。
        所以必须以「有 loginName / id」为准，否则会误报未登录。
        """
        try:
            j = self.status()
        except Exception as e:
            return {"ok": False, "error": str(e)}
        name = j.get("loginName")
        uid = j.get("id") or j.get("studentId")
        return {"ok": bool(name and uid), "loginName": name,
                "userId": (uid or "")[:8], "seat": j.get("seatNumber"),
                "classTeacher": j.get("classTeacherName")}

    def summary(self):
        """跨域一次性摘要，用于快速确认账号可用性。"""
        out = {}
        for name, fn in [("身份", self.status), ("未读短信", self.unreadStat),
                         ("学期", self.schoolTermCombo), ("综评", lambda: self.quality(limit=1))]:
            try:
                out[name] = fn()
            except Exception as e:
                out[name] = {"error": str(e)}
        return out


def main():
    import argparse
    import json
    ap = argparse.ArgumentParser(description="AutoXMYZ 只读客户端自检")
    ap.add_argument("--token", default="", help="JSESSIONID 值")
    ap.add_argument("--health", action="store_true", help="只做健康检查")
    ap.add_argument("--summary", action="store_true", help="跨域摘要")
    a = ap.parse_args()
    try:
        c = XMYZClient(token=a.token) if a.token else XMYZClient()
    except XmyzError as e:
        print("会话不可用：", e)
        return 4
    if a.summary or not a.health:
        print(json.dumps(c.summary(), ensure_ascii=False, indent=1)[:3000])
    else:
        print(json.dumps(c.healthCheck(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
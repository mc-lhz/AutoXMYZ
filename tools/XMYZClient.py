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

from Access.HttpTransport import Http, XmyzError  # noqa: F401,E402
from StudentBase.ProfileDict import ProfileMixin, DictMixin  # noqa: E402
from LifeOffice.StudyMessage import StudyMixin, MessageMixin, AttachmentMixin  # noqa: E402
from QualityCenter.QualityRead import QualityMixin  # noqa: E402
from CommunityCenter.VolunteerRead import CommunityMixin, VolunteerMixin  # noqa: E402
from ExamCenter.ExamPractice import ExamPracticeMixin  # noqa: E402
from ElectiveCenter.ElectiveCourse import ElectiveCourseMixin  # noqa: E402
from ElectiveCenter.ElectiveResult import ElectiveResultMixin  # noqa: E402
from ElectiveCenter.ElectiveActivity import ElectiveActivityMixin  # noqa: E402
from ElectiveCenter.ElectiveAttendance import ElectiveAttendanceMixin  # noqa: E402
from ScheduleCenter.Calendar import CalendarMixin  # noqa: E402
from ScheduleCenter.CategoryMessage import CategoryMessageMixin  # noqa: E402
from PsychCenter.PsychAppointment import PsychAppointmentMixin  # noqa: E402
from WorkCardCenter.WorkCard import WorkCardMixin  # noqa: E402
from SelectSubjectCenter.SelectSubject import SelectSubjectMixin  # noqa: E402
from StudentCenter.ScoreExtras import ScoreExtrasMixin  # noqa: E402
from StudentCenter.QualityExtras import QualityExtrasMixin  # noqa: E402
from StudentCenter.LifeRecords import LifeRecordsMixin  # noqa: E402
from StudentCenter.AccountExtras import AccountExtrasMixin  # noqa: E402
from VoteCenter.Vote import VoteMixin  # noqa: E402
from EvaluationCenter.TeacherEvaluation import TeacherEvaluationMixin  # noqa: E402
from EvaluationCenter.ElectiveEvaluation import ElectiveEvaluationMixin  # noqa: E402
from CommunityCenter.CommunityExtra import CommunityExtraMixin  # noqa: E402
from CommunityCenter.VolunteerNew import VolunteerNewMixin  # noqa: E402
from LifeOffice.WorkSubmit import WorkSubmitMixin  # noqa: E402


class XMYZClient(ProfileMixin, DictMixin, StudyMixin, MessageMixin,
                  AttachmentMixin, QualityMixin, CommunityMixin,
                  VolunteerMixin, ExamPracticeMixin, ElectiveCourseMixin,
                  ElectiveResultMixin, ElectiveActivityMixin,
                  ElectiveAttendanceMixin, CalendarMixin, CategoryMessageMixin,
                  PsychAppointmentMixin, WorkCardMixin, VoteMixin,
                  SelectSubjectMixin, ScoreExtrasMixin, QualityExtrasMixin,
                  LifeRecordsMixin, AccountExtrasMixin,
                  TeacherEvaluationMixin, ElectiveEvaluationMixin,
                  CommunityExtraMixin, VolunteerNewMixin, WorkSubmitMixin,
                  Http):
    """厦门一中信息校园综合应用系统客户端（读写均可用，能力政策 2026-10-24 修订）。

    写操作不再被客户端拦截，实际可写范围由服务端账号权限决定；
    纪律：只写本人数据、可逆优先、不碰他人密码与审批流。
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
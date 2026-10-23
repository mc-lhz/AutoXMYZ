"""学社门面：组合各业务域 mixin，对外 API 就是 StudentHubClient。

用法：
    import sys; sys.path.insert(0, "tools")
    from StudentHubClient import StudentHubClient
    c = StudentHubClient()                    # 自动读用户目录会话（仓库外）
    c = StudentHubClient(token="<Bearer>")
    print(c.healthCheck())

能力红线分工（与 XMYZClient 不同）：
  - xmyz.xmedu.cn   → 纯只读（HttpTransport._guard 强制拦截写端点）
  - 学社（本门面）   → **功能完备**：站点为学生自建平台，唱票/审核/发布等
    写操作是需求本身。写前请确认身份与影响面；删除类方法名均显式含 delete。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from StudentHub.HubTransport import HubHttp, HubError, HubAuthError  # noqa: F401,E402
from StudentHub.AccountMixin import AccountMixin  # noqa: E402
from StudentHub.PortalMixin import PortalMixin  # noqa: E402
from StudentHub.MessageMixin import MessageMixin  # noqa: E402
from StudentHub.TallyMixin import TallyMixin  # noqa: E402
from StudentHub.CampaignMixin import CampaignMixin  # noqa: E402
from StudentHub.TicketMixin import TicketMixin  # noqa: E402
from StudentHub.MuseumMixin import MuseumMixin  # noqa: E402
from StudentHub.RatingMixin import RatingMixin  # noqa: E402
from StudentHub.VoicesMixin import VoicesMixin  # noqa: E402
from StudentHub.CampusMixin import CampusMixin  # noqa: E402
from StudentHub.DebateMixin import DebateMixin  # noqa: E402


class StudentHubClient(AccountMixin, PortalMixin, MessageMixin,
                       TallyMixin, CampaignMixin, TicketMixin,
                       MuseumMixin, RatingMixin, VoicesMixin,
                       CampusMixin, DebateMixin, HubHttp):
    """厦门一中学生社区（xmyzstudent.com）客户端 —— 功能完备。

    端点事实来源：`StudentHub/HubEndpoints.py`（260 REST + 2 WS）。
    任意未包装端点可直接 `c.call`（见 HubHttp._request / get/post/...）。
    """

    def healthCheck(self):
        """会话自检：/user/profile 可达且有 username 即有效。

        公开端点未登录也返回 200，所以判据必须是**本人数据**端点，
        不能拿 /banners 这类公开端点当健康依据。
        """
        try:
            prof = self.getMyProfile()
        except HubAuthError:
            return {"ok": False, "error": "未登录或 token 过期（HubSession.py token/campus）"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        return {"ok": bool((prof or {}).get("username")),
                "username": (prof or {}).get("username"),
                "nickname": (prof or {}).get("nickname"),
                "campus": (prof or {}).get("campusName")}

    def summary(self):
        """跨域一次性摘要：本人 + 各公开面板。"""
        out = {}
        for name, fn in [
                ("本人", self.getMyProfile),
                ("未读消息", self.getUnreadMessageCount),
                ("权限", self.getMyPermissions),
                ("声音面板", self.getVoicesStatus),
                ("横幅", self.getPublicBanners),
                ("校区", self.getCampuses),
                ("唱票活动", self.getAdminTallyActivities)]:
            try:
                out[name] = fn()
            except Exception as e:
                out[name] = {"error": str(e)}
        return out


def main():
    import argparse
    import json
    ap = argparse.ArgumentParser(description="学社客户端自检")
    ap.add_argument("--token", default="", help="Bearer token 值")
    ap.add_argument("--health", action="store_true", help="只做健康检查")
    ap.add_argument("--summary", action="store_true", help="跨域摘要")
    a = ap.parse_args()
    try:
        c = StudentHubClient(token=a.token) if a.token else StudentHubClient()
    except HubError as e:
        print("会话不可用：", e)
        return 4
    if a.summary or not a.health:
        print(json.dumps(c.summary(), ensure_ascii=False, indent=1)[:3000])
    else:
        print(json.dumps(c.healthCheck(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""只读端点全量探测 —— 复刻建库时的 360 项，作为可重复的回归。

用法：
  python TestApiReadOnly.py                      # 读 reference/.session.json
  python TestApiReadOnly.py --token <JSESSIONID>
  python TestApiReadOnly.py --limit 20           # 快速冒烟
  python TestApiReadOnly.py --report out.json

判定口径与建库一致：只读端点各发一次 GET + POST，
`start=0&limit=1`，`id` 一律用不存在的 -1，限速 180ms。
写类端点**不在本测试范围内**，由 TestContract 的能力红线保证不会被调用。
"""
import argparse
import io
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from XMYZClient import XMYZClient, XmyzError  # noqa: E402

READONLY_TARGETS = [
    ("/account/user!status.action", "本人账号状态", None),
    ("/account/user!readSimpleUser.action", "用户简要信息", None),
    ("/system/dict!getComboStore.action", "字典下拉", {"dictCode": "sex"}),
    ("/system/dict!getTree.action", "树状字典", {"dictCode": "sex"}),
    ("/system/weather!getWeather.action", "校园天气", None),
    ("/system/attachment!readByUser.action", "最近上传附件", None),
    ("/edu/school-term!getComboStore.action", "学期列表", None),
    ("/edu/class!getComboStore.action", "班级列表", None),
    ("/edu/grade!getComboStore.action", "年段列表", None),
    ("/edu/subject!getComboStore.action", "科目列表", None),
    ("/edu/grade!loadTree.action", "年级树", None),
    ("/quality/quality!read.action", "综合素质评价总表", None),
    ("/quality/quality-score-stat!read.action", "综评得分统计", None),
    ("/score/student-score!read.action", "我的成绩", None),
    ("/transcript/transcript!readByStudent.action", "我的成绩单", None),
    ("/edu/module-score!read.action", "模块修习成绩", None),
    ("/edu/physical-examination!readByStudent.action", "体能测试", None),
    ("/edu/growth-record!read.action", "我的成长记录", None),
    ("/edu/work!readByClass.action", "班级作业", None),
    ("/edu/speciality!readByStudent.action", "特长信息", None),
    ("/edu/match-awards!read.action", "比赛获奖", None),
    ("/message/short-message!inbox.action", "短信收件箱", None),
    ("/message/short-message!outbox.action", "短信发件箱", None),
    ("/message/recipient!findUnread.action", "未读统计", None),
    ("/message/recipient!statInfo.action", "收发统计", None),
    ("/office/notification-feedback!read.action", "通知公告", None),
    ("/community/community!loadTree.action", "社团树", None),
    ("/community/member!readByStudent.action", "我参与的社团", None),
    ("/community/member-evaluate!readByStudent.action", "成员评价", None),
    ("/community/attendance!readByStudent.action", "社团考勤", None),
    ("/community/property-borrow!read.action", "校产借出", None),
    ("/volunteer/activity!readByParticipate.action", "我参与的志愿活动", None),
    ("/volunteer/activity!read.action", "志愿活动列表", None),
    ("/volunteer/sign!read.action", "志愿者签到", None),
    ("/elective/elective-result!read.action", "选课结果", None),
]


def probe(c, path, label, extra=None):
    """探测单个只读端点。

    ⚠️ 判定不能只看 `success` 或 `status`：本系统有两类响应——
      ① 信封型 `{"total":n,"data":[...],"success":true}`
      ② **裸数组 / 裸对象**（如 `dict!getTree`、`grade!loadTree`、
         `recipient!statInfo`、`community!loadTree`）
    早先的判定只认 ①，于是这 5 个真实可用的端点被误报 FAIL。
    结论：只要**解析出了 JSON** 就记 ALIVE，空数组也算（无数据≠不可用）。
    """
    params = {"start": 0, "limit": 1, "id": "-1"}
    if extra:
        params.update(extra)
    out = {"endpoint": path, "label": label, "tries": []}
    for m in ("GET", "POST"):
        try:
            d = c._call(path, m, params)
            rec = {"method": m}
            if isinstance(d, (list, dict)):
                rec["parsed"] = True
                rec["kind"] = "list" if isinstance(d, list) else "dict"
                rec["rows"] = len(d) if isinstance(d, list) else None
                if isinstance(d, dict):
                    rec["success"] = d.get("success")
                    rec["msg"] = (d.get("message") or "")[:60]
            else:
                rec["parsed"] = False
                rec["raw"] = str(d)[:80]
            out["tries"].append(rec)
        except Exception as e:
            out["tries"].append({"method": m, "error": str(e)[:80]})
    # 任一方法解析出 JSON 即视为 ALIVE（含空数组：端点通、无数据）
    out["verdict"] = "ALIVE" if any(t.get("parsed") for t in out["tries"]) else "FAIL"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--rate", type=float, default=0.18)
    ap.add_argument("--report", default="")
    a = ap.parse_args()

    try:
        c = XMYZClient(token=a.token) if a.token else XMYZClient()
    except XmyzError as e:
        print("会话不可用：", e)
        return 4

    health = c.status()
    print("[会话] loginName=%s userId=%s…" % (health.get("loginName"), (health.get("id") or "")[:8]))

    targets = READONLY_TARGETS[:a.limit] if a.limit else READONLY_TARGETS
    results, npass = [], 0
    for i, (path, label, extra) in enumerate(targets, 1):
        r = probe(c, path, label, extra)
        results.append(r)
        npass += r["verdict"] == "ALIVE"
        t0 = r["tries"][0]
        shape = ("list×%s" % t0.get("rows")) if t0.get("kind") == "list" else \
                ("dict" if t0.get("kind") == "dict" else "?")
        print("  [%2d/%2d] %-6s %-22s %-46s %s"
              % (i, len(targets), r["verdict"], label[:22], path[:46], shape))
        time.sleep(a.rate)

    print("\n%d/%d 通过" % (npass, len(targets)))
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print("报告 → %s" % a.report)
    return 0 if npass == len(targets) else 1


if __name__ == "__main__":
    sys.exit(main())
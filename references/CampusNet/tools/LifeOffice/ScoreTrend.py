"""成绩趋势：transcript 全量场次 → 结构化「科目×场次×分数/段位」→ xlsx / 控制台表。

数据源：transcript!readByStudent（场次）+ getTranscriptByStudent?transcriptId=（明细行，
data[0].content 为人类可读成绩行，形如「语文:116_  段次:70% 数学:125_ …」）。

解析规则（2026-10-24 对 14 场实测归纳）：
  - 条目形「<科目>:<值>」，科目可带赋分后缀（化赋/生赋）；值可带下划线尾巴
  - 位次口径三种写法：段次:70% / 段次%:19% / 百分比:56%，统一折算成 <percent> 数值
  - 非成绩条目（报名号/考场/身份证等）在 content 里无百分比对，自动归入 other
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 科目规范化：别名 → 标准名
SUBJECT_ALIASES = {
    "语文": "语文", "数学": "数学", "英语": "英语", "物理": "物理",
    "化学": "化学", "化赋": "化学(赋分)", "生物": "生物", "生赋": "生物(赋分)",
    "历史": "历史", "政治": "政治", "地理": "地理",
    "总分": "总分", "总 分": "总分",
}
PAIR_RE = re.compile(r"([一-龥A-Za-z0-9（）()]+)[:：]\s*([^:一-龥]*)")
PCT_RE = re.compile(r"(\d{1,3})\s*%")
# 位次伪键：它们不是科目，百分比值属于「前一个科目」
PCT_KEYS = ("段次", "段次%", "百分比", "位次")


def parseContent(content):
    """成绩行 → {科目: {score, percent}}；非成绩条目进 other。

    行格式实测：「语文:116  段次:70% 数学:125_  段次:95%」——
    「段次/百分比」是独立键值对，百分比值回填给前一个科目。
    """
    out, other, lastSub = {}, [], None
    if not content:
        return out, other
    s = content.replace("_", " ")
    for m in PAIR_RE.finditer(s):
        key, val = m.group(1), m.group(2).strip()
        if key == "姓名":
            continue
        pm = PCT_RE.search(val)
        if key in PCT_KEYS and pm:
            if lastSub and lastSub in out:
                out[lastSub]["percent"] = int(pm.group(1))
            continue
        sub = SUBJECT_ALIASES.get(key)
        num = re.match(r"^([\d.]+)", val)
        if sub:
            out[sub] = {"score": float(num.group(1)) if num else None,
                        "percent": None}
            lastSub = sub
        elif val:
            other.append(f"{key}:{val}")
    return out, other


def collectTrend(client, **kw):
    """拉全量场次并逐场解析。返回 [{name, time, scores{}, other[], content}]"""
    t = client.transcript(**kw)
    exams = sorted(t.get("data") or [], key=lambda x: x.get("time") or 0)
    import time as _time
    out = []
    for e in exams:
        r = client.get("/transcript/transcript!getTranscriptByStudent.action",
                       {"transcriptId": e.get("id")})
        rows = r.get("data") or []
        content = (rows[0].get("content") or "").strip() if rows else ""
        scores, other = parseContent(content)
        out.append({
            "name": e.get("name"),
            "time": _time.strftime("%Y-%m-%d", _time.localtime(e["time"] / 1000)) if e.get("time") else "",
            "scores": scores, "other": other, "content": content,
        })
    return out


def isRealExam(entry):
    """过滤信息采集类（无任何「分数+百分比」条目的场次）。"""
    return any(v.get("percent") is not None for v in entry["scores"].values())


def toXlsx(trend, path):
    """科目×场次 矩阵：上半分数、下半段位%。"""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    subs = []
    for e in trend:
        for s in e["scores"]:
            if s not in subs:
                subs.append(s)
    wb = Workbook()
    ws = wb.active
    ws.title = "成绩趋势"
    ws.append(["场次", "日期"] + subs)
    ws.cell(row=1, column=1).font = Font(bold=True)
    r_score, r_pct = 2, 3
    for e in trend:
        ws.cell(row=r_score, column=1, value=e["name"])
        ws.cell(row=r_score, column=2, value=e["time"])
        ws.cell(row=r_pct, column=1, value="  ↳段位%")
        for ci, s in enumerate(subs, start=3):
            v = e["scores"].get(s)
            if v:
                if v.get("score") is not None:
                    ws.cell(row=r_score, column=ci, value=v["score"])
                if v.get("percent") is not None:
                    ws.cell(row=r_pct, column=ci, value=v["percent"] / 100.0)
                    ws.cell(row=r_pct, column=ci).number_format = "0%"
        r_score += 2
        r_pct += 2
    wb.save(path)
    return path


def toConsole(trend):
    """控制台摘要：每场一行关键科目。"""
    lines = []
    for e in trend:
        if not isRealExam(e):
            continue
        parts = []
        for s in ("语文", "数学", "英语", "物理", "化学", "生物", "总分"):
            v = e["scores"].get(s)
            if v and v.get("score") is not None:
                p = f"({v['percent']}%)" if v.get("percent") is not None else ""
                parts.append(f"{s}{v['score']:.0f}{p}".replace(".0", ""))
        lines.append(f"{e['time']} {e['name']}: " + "  ".join(parts))
    return lines

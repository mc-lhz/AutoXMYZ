"""聚合契约审计 —— 三子技能分区结构（离线，无网络无凭据）。

检查：
  ① 结构：根 SKILL/AGENTS/README/VERSION + 三个 references/<Sub>/{SUBSKILL,AGENTS,tools,reference}
  ② 无游离 SKILL.md：references/** 下只允许 SUBSKILL.md（否则宿主会重复注册技能）
  ③ 根 description：三站点路由关键词 + 「数据不互通」+ 懒加载声明
  ④ 子树契约：依次子进程运行（各自根），CampusNet 9 项 / XmyzStudent 15 项 / XinYiWo 17 项且 FAIL=0
  ⑤ 各子树 reference 体积独立 ≤150KB
  ⑥ 根 tools/Login.py -h 冒烟；VERSION 格式
"""
import os
import re
import subprocess
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = []


def check(name, fn):
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, "异常: %s" % e
    RESULTS.append((name, ok, detail))
    return ok


SUBS = {"CampusNet": 9, "XmyzStudent": 15, "XinYiWo": 17}


def structure_ok():
    need = ["SKILL.md", "AGENTS.md", "README.md", "VERSION", "tools/Login.py",
            "tools/TestCases/TestAggregate.py"]
    for sub in SUBS:
        need += ["references/%s/SUBSKILL.md" % sub, "references/%s/tools" % sub,
                 "references/%s/reference" % sub]
    miss = [p for p in need if not os.path.exists(os.path.join(ROOT, p))]
    return (not miss), ("结构齐备" if not miss else "缺失 %s" % miss)


def no_stray_skill_md():
    bad = []
    for dp, dns, fs in os.walk(os.path.join(ROOT, "references")):
        dns[:] = [d for d in dns if d not in ("__pycache__", ".git")]
        for f in fs:
            if f == "SKILL.md":
                bad.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return (not bad), ("references/ 下无游离 SKILL.md" if not bad else "发现 %s" % bad[:5])


def routing_keywords():
    t = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    must = ["CampusNet", "XmyzStudent", "XinYiWo", "数据不互通",
            "不加载其他子技能", "xmyz.xmedu.cn", "xmyzstudent.com", "591iq.cn"]
    miss = [k for k in must if k not in t[:6000]]
    # 三站 description 触发词抽查
    for kw in ("成绩查询", "唱票", "综评"):
        if kw not in t[:6000]:
            miss.append(kw)
    return (not miss), ("路由关键词齐备" if not miss else "缺 %s" % miss)


def subtree_contracts():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    plan = [("CampusNet", "tools/TestCases/TestContract.py", r"(\d+)/\1 通过"),
            ("XmyzStudent", "tools/TestCases/TestHub.py", r"(\d+)/\1 通过"),
            ("XinYiWo", "tools/TestCases/TestContract.py", r"FAIL=(\d+)")]
    bad = []
    for sub, script, pat in plan:
        cwd = os.path.join(ROOT, "references", sub)
        r = subprocess.run([sys.executable, "-B", script], cwd=cwd, env=env,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        if sub == "XinYiWo":
            m = re.search(r"FAIL=(\d+)", out)
            if not m or int(m.group(1)) != 0:
                bad.append("%s FAIL!=0" % sub)
        else:
            m = re.search(r"(\d+)/(\d+) 通过", out)
            if not m or m.group(1) != m.group(2) or int(m.group(2)) != SUBS[sub]:
                bad.append("%s 契约未全过" % sub)
    return (not bad), ("三子树契约全绿" if not bad else "；".join(bad))


def reference_budgets():
    detail, bad = [], []
    for sub in SUBS:
        d = os.path.join(ROOT, "references", sub, "reference")
        kb = sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d)
                 if os.path.isfile(os.path.join(d, f))
                 and f not in (".session.json",)) / 1024.0
        detail.append("%s %.0fKB" % (sub, kb))
        if kb > 150:
            bad.append("%s %.0fKB>150" % (sub, kb))
    return (not bad), (" / ".join(detail) + ("（超限 %s）" % bad if bad else ""))


def version_and_cli():
    v = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
    if not re.fullmatch(r"v\d+\.\d+", v):
        return False, "VERSION 格式异常: %r" % v
    r = subprocess.run([sys.executable, "-B", "tools/Login.py", "-h"], cwd=ROOT,
                       capture_output=True, timeout=60)
    if r.returncode != 0:
        return False, "Login.py -h 失败"
    return True, "%s；Login.py -h 通过" % v


def main():
    print("AutoXMYZ 聚合契约审计（离线）")
    print("=" * 60)
    for name, fn in [("结构·三子技能", structure_ok),
                     ("结构·无游离 SKILL", no_stray_skill_md),
                     ("路由·根 description", routing_keywords),
                     ("契约·三子树", subtree_contracts),
                     ("体积·reference 分区", reference_budgets),
                     ("版本·VERSION+CLI", version_and_cli)]:
        check(name, fn)
    npass = 0
    for name, ok, detail in RESULTS:
        print("  [%s] %-18s %s" % ("PASS" if ok else "FAIL", name, detail))
        npass += ok
    print("=" * 60)
    print("%d/%d 通过" % (npass, len(RESULTS)))
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
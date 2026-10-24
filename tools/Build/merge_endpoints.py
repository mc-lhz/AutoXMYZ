#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""三方端点合并: desktop(菜单树+97模块) vs m.html vs m2.html

  python merge_endpoints.py
"""
import json, os, re, io, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from endpoint_kind import kind as KIND
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def _work_dir():
    """建库工作目录：环境变量 AUTOMXYZ_WORK > <仓库>/build_data。

    原始数据（menu_tree.json / endpoints.json / validation.json / js/）落在这里。
    ⚠️ 这些文件含真实姓名、学号、userId，**不入库**；
    需要时用 tools/Build/ 下的脚本重新生成。
    """
    import os as _os
    return _os.environ.get(
        "AUTOMXYZ_WORK",
        _os.path.join(_os.path.dirname(_os.path.dirname(
            _os.path.dirname(_os.path.abspath(__file__)))), "build_data"))


WD = _work_dir()
TOOL = os.environ.get("AUTOMXYZ_BUNDLE", os.path.join(WD, "bundles"))
EP_RE = re.compile(r"[A-Za-z0-9_\-/]+![A-Za-z]+\.action")

WRITE_HINT = re.compile(r"!(?:create|update|save|delete|destroy|remove|add|submit|approve|"
                        r"notApprovedComplete|.*ApprovedComplete|completedComplete|imp|"
                        r"upload|reset|change|send|input|insert|modify|edit|import|export|copy|"
                        r"move|transfer|bind|unbind|enable|disable|publish|release|withdraw|"
                        r"revoke|revert|resend|sort|setRead|batchUpdate|markAs|toAttachment|"
                        r"generatePdfAndHtml|compressDownload|cancel|confirm|accept|refuse)\.action$",
                        re.I)


def read_bundle(p):
    txt = open(p, encoding="gb18030", errors="replace").read()
    return set(EP_RE.findall(txt))


def main():
    desktop = json.load(open(os.path.join(WD, "desktop_endpoints.json"), encoding="utf-8"))
    dset = {k.lstrip("./") for k in desktop}
    m2 = read_bundle(os.path.join(TOOL, "tool_124c92b30001rlb29dXmo5jHgt"))
    m1 = read_bundle(os.path.join(TOOL, "tool_124c7e5550015IqDtyvCFsAI72"))

    print("desktop(菜单树+97模块) = %d" % len(dset))
    print("m2.html 主 bundle       = %d" % len(m2))
    print("m.html 主 bundle        = %d" % len(m1))
    print()
    print("交集 d∩m2 = %d   d∩m = %d   m2∩m = %d   三方共有 = %d"
          % (len(dset & m2), len(dset & m1), len(m2 & m1), len(dset & m2 & m1)))
    print("仅 desktop = %d" % len(dset - m2 - m1))
    print("仅 m2       = %d" % len(m2 - dset - m1))
    print("仅 m        = %d" % len(m1 - dset - m2))
    print()

    # 无 `!` 的直连路由（m3 微信端 / 招生 / UEditor）：EP_RE 天生抓不到，
    # 逐一从新版 bundle 字面量核实后显式登记（2026-10-24 对账）。
    # kind 交给 KIND() 的兜底（判 read）；其中 ueditor-plus 实为上传后端（写语义），
    # 在 api.md 阅读时注意。
    DIRECT_ROUTES = frozenset([
        "m3/category.action",
        "m3/recipient-detail.action",
        "m3/shake-attendance/attendance-detail.action",
        "m3/shake-attendance/daily-attendance-detail.action",
        "m3/short-message-detail.action",
        "m3/weixin/login.action",
        "recruit/admission-school.action",
        "recruit/physical-examination-form-detail.action",
        "system/ueditor-plus.action",
    ])

    all_eps = dset | m2 | m1 | DIRECT_ROUTES
    rows = []
    for e in sorted(all_eps):
        src = []
        if e in dset:
            src.append("desktop")
        if e in m2:
            src.append("m2")
        if e in m1:
            src.append("m")
        info = desktop.get(e.lstrip("./")) or desktop.get(e) or {}
        rows.append({
            "endpoint": e,
            "sources": src,
            # ⚠️ kind 唯一来源是 endpoint_kind（红线）。本文件曾有第二套
            # WRITE_HINT 正则，对新版 m2 的上百个 *Complete 动作漏判 —— 已废除。
            "kind": KIND(e),
            "menus": info.get("menus", []),
            "files": sorted(set(info.get("sources", [])))[:6],
        })

    out = os.path.join(WD, "endpoints.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    read_n = sum(1 for r in rows if r["kind"] == "read")
    write_n = len(rows) - read_n
    print("合并后唯一端点 = %d  (只读 %d / 写类 %d)" % (len(rows), read_n, write_n))
    print("-> %s" % out)

    # 按 namespace 汇总
    ns = {}
    for r in rows:
        ns.setdefault(r["endpoint"].split("/")[0], {"n": 0, "d": 0, "m2": 0, "m": 0})
        ns[r["endpoint"].split("/")[0]]["n"] += 1
        if "desktop" in r["sources"]:
            ns[r["endpoint"].split("/")[0]]["d"] += 1
        if "m2" in r["sources"]:
            ns[r["endpoint"].split("/")[0]]["m2"] += 1
        if "m" in r["sources"]:
            ns[r["endpoint"].split("/")[0]]["m"] += 1
    print()
    print("%-24s %5s %8s %5s %5s" % ("namespace", "合计", "desktop", "m2", "m"))
    for k in sorted(ns, key=lambda x: -ns[x]["n"]):
        v = ns[k]
        print("%-24s %5d %8d %5d %5d" % (k, v["n"], v["d"], v["m2"], v["m"]))


if __name__ == "__main__":
    main()
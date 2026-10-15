#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按菜单树下发的 action.jsFile 定向抓取桌面端模块,并抽取端点。

  python fetch_modules.py
"""
import json, os, re, sys, io, time
from concurrent.futures import ThreadPoolExecutor, as_completed
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


import requests

BASE = "https://xmyz.xmedu.cn"
WD = _work_dir()
JS_DIR = os.path.join(WD, "js")
EP_RE = re.compile(r"[A-Za-z0-9_\-/]+![A-Za-z]+\.action")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def collect_jsfiles():
    d = json.load(open(os.path.join(WD, "menu_tree.json"), encoding="utf-8"))
    files, owner = [], {}
    def walk(nodes):
        for n in (nodes or []):
            a = n.get("action")
            if a and a.get("jsFile"):
                for f in a["jsFile"].split("|"):
                    f = f.strip()
                    if f and f not in owner:
                        owner[f] = []
                        files.append(f)
                    if f and n.get("text"):
                        owner.setdefault(f, []).append(n["text"])
            if n.get("children"):
                walk(n["children"])
    walk(d)
    return files, owner


def fetch_one(sess, rel):
    url = BASE + "/" + rel.lstrip("./").lstrip("/")
    local = os.path.join(JS_DIR, rel.replace("./", "").replace("/", os.sep))
    os.makedirs(os.path.dirname(local), exist_ok=True)
    if os.path.exists(local) and os.path.getsize(local) > 0:
        return rel, "cached", os.path.getsize(local), url
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=30)
            if r.status_code == 200 and r.content:
                with open(local, "wb") as f:
                    f.write(r.content)
                return rel, "ok", len(r.content), url
            last = "HTTP %d" % r.status_code
        except Exception as e:
            last = str(e)[:60]
        time.sleep(0.6 * (attempt + 1))
    return rel, "FAIL " + last, 0, url


def main():
    files, owner = collect_jsfiles()
    print("待抓 JS 文件: %d" % len(files))
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Referer": BASE + "/manager.html"})

    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch_one, s, f): f for f in files}
        for i, fut in enumerate(as_completed(futs), 1):
            res = fut.result()
            results.append(res)
            if res[1].startswith("FAIL"):
                print("  [%2d/%2d] %-58s %s" % (i, len(files), res[0][:58], res[1]))
    ok = sum(1 for r in results if r[1] in ("ok", "cached"))
    kb = sum(r[2] for r in results) / 1024.0
    print("完成: 成功 %d / %d, 合计 %.1f KB" % (ok, len(files), kb))

    # 抽端点
    eps = {}
    for root, _, fs in os.walk(JS_DIR):
        for fn in fs:
            if not fn.endswith(".js"):
                continue
            p = os.path.join(root, fn)
            rel = "./" + os.path.relpath(p, JS_DIR).replace(os.sep, "/")
            try:
                txt = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for e in EP_RE.findall(txt):
                eps.setdefault(e, {"sources": [], "menus": []})
                eps[e]["sources"].append(rel)
                for m in owner.get(rel, []):
                    if m not in eps[e]["menus"]:
                        eps[e]["menus"].append(m)

    out = os.path.join(WD, "desktop_endpoints.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(eps, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("桌面端端点(含来源 jsFile 与所属菜单): %d -> %s" % (len(eps), out))


if __name__ == "__main__":
    main()
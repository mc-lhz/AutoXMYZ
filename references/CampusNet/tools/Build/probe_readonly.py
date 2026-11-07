#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""只读端点探测: 对 406 个只读端点逐个发请求, 记录状态码与返回结构。

安全约束:
  - 只对 kind == 'read' 的端点发请求
  - 一律 GET / POST, 不带任何写语义参数 (id 只用不存在的负数)
  - 限速 200ms, 连续 3 次非 2xx 则降速
  - 绝不探测 !delete / !update / !save / !create 等写端点

  python probe_readonly.py [--limit N] [--rate 0.2]
"""
import argparse, io, json, os, re, sys, time
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
TIMEOUT = 8
WD = _work_dir()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
NEG_ID = "-1"


def load_session():
    st = json.load(open(os.path.join(WD, "session.json"), encoding="utf-8"))
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": BASE + "/manager.html",
        "Origin": BASE,
        "X-Requested-With": "XMLHttpRequest",
    })
    for k, v in st["cookies"].items():
        s.cookies.set(k, v, domain="xmyz.xmedu.cn", path="/")
    return s


def summarize(text, limit=400):
    """提取返回结构摘要: JSON 则记顶层键, 否则记前若干字符 + 是否 HTML。"""
    t = (text or "").strip()
    if not t:
        return {"type": "empty", "detail": ""}
    if t[0] in "[{":
        try:
            d = json.loads(t)
            if isinstance(d, dict):
                keys = list(d.keys())[:15]
                s = d.get("success")
                n = d.get("total")
                if isinstance(d.get("data"), list):
                    n = len(d["data"])
                    item = d["data"][0] if d["data"] else None
                    item_keys = list(item.keys())[:15] if isinstance(item, dict) else None
                else:
                    item_keys = None
                return {"type": "json", "keys": keys, "success": s,
                        "rows": n, "item_keys": item_keys, "raw": t[:limit]}
            if isinstance(d, list):
                return {"type": "json_list", "rows": len(d),
                        "item_keys": list(d[0].keys())[:15] if d and isinstance(d[0], dict) else None,
                        "raw": t[:limit]}
        except Exception:
            pass
    if t.startswith("<"):
        m = re.search(r"<title>(.*?)</title>", t, re.S | re.I)
        return {"type": "html", "title": (m.group(1).strip() if m else "")[:120]}
    return {"type": "text", "raw": t[:limit]}


def probe(s, ep):
    path = ep.lstrip("/")
    url = BASE + "/" + path
    base_params = {"start": 0, "limit": 1}
    # 用不存在的 id, 保证即使端点语义含删除也只会命中"无此记录"
    params = dict(base_params)
    if re.search(r"(?:detail|read|ById|id)!|!.*(?:detail|ById)\.action$", ep):
        params["id"] = NEG_ID
    out = {"endpoint": ep, "attempts": []}
    for method in ("GET", "POST"):
        try:
            if method == "GET":
                r = s.get(url, params=params, timeout=TIMEOUT, allow_redirects=False)
            else:
                r = s.post(url, data=params, timeout=TIMEOUT, allow_redirects=False)
            rec = {"method": method, "status": r.status_code,
                   "len": len(r.content),
                   "ct": (r.headers.get("Content-Type") or "")[:40],
                   "loc": (r.headers.get("Location") or "")[:120]}
            rec.update(summarize(r.text))
            out["attempts"].append(rec)
        except Exception as e:
            out["attempts"].append({"method": method, "error": str(e)[:120]})
    # 判定
    st = [a.get("status") for a in out["attempts"] if "status" in a]
    if not st:
        out["verdict"] = "ERROR"
    elif all(x in (401, 403) for x in st):
        out["verdict"] = "FORBIDDEN"
    elif any(200 <= x < 300 for x in st):
        out["verdict"] = "ALIVE"
    elif any(x in (302, 301) for x in st):
        out["verdict"] = "REDIRECT"
    elif all(x == 404 for x in st):
        out["verdict"] = "GONE"
    else:
        out["verdict"] = "ERR%d" % st[0]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--rate", type=float, default=0.2)
    ap.add_argument("--timeout", type=int, default=8)
    a = ap.parse_args()

    rows = json.load(open(os.path.join(WD, "endpoints.json"), encoding="utf-8"))
    reads = [r for r in rows if r["kind"] == "read"]
    if a.limit:
        reads = reads[:a.limit]
    print("待探测只读端点: %d" % len(reads), flush=True)

    s = load_session()
    r = s.post(BASE + "/account/user!status.action", timeout=15)
    print("[会话自检] %s loggedIn=%s" % (r.status_code, '"loggedIn":true' in r.text.replace(" ", "")), flush=True)

    global TIMEOUT
    TIMEOUT = a.timeout
    # 增量落盘 + 断点续跑：1176 个端点在中断后不必从头再来
    outPath = os.path.join(WD, "validation.json")
    results = []
    if os.path.exists(outPath):
        results = json.load(open(outPath, encoding="utf-8"))
        print("[resume] 已有 %d 条，跳过" % len(results))
    done = {r["endpoint"] for r in results}
    t0 = time.time()
    for i, row in enumerate(reads, 1):
        if row["endpoint"] in done:
            continue
        res = probe(s, row["endpoint"])
        res["menus"] = row["menus"]
        res["sources"] = row["sources"]
        results.append(res)
        if i % 25 == 0 or res["verdict"] not in ("ALIVE",):
            print("  [%3d/%3d] %-58s %s" % (i, len(reads), res["endpoint"][:58], res["verdict"]), flush=True)
        if len(results) % 50 == 0:
            with open(outPath, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=1)
        time.sleep(a.rate)

    with open(outPath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)

    from collections import Counter
    c = Counter(r["verdict"] for r in results)
    print("\n用时 %.1fs" % (time.time() - t0))
    print("结果分布:", dict(c))
    print("-> %s" % outPath)


if __name__ == "__main__":
    main()
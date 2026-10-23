#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""学社只读端点全量探测：对注册表 kind=='read' 的 GET 端点逐个免登录请求，
验证路径真实存在性，并产出「公开 / 需登录」分类。

安全约束（与 xmyz 的 probe_readonly.py 同纪律）：
  - 只探测 kind == 'read' 的端点；**写端点一个不碰**
    （空 body 的写请求在未鉴权下无法保证服务端先鉴权后执行，风险不值得冒）
  - 路径参数一律填不存在的 `-1`（AGENTS.md 探测纪律）
  - 限速默认 180ms；连续 5 次网络错误立即停手
  - 全程免凭据：401 是**预期且有用**的结果（= 端点存在且需登录）

产物：
  - <AUTOMXYZ_WORK|build_data>/hub_probe_raw.json   原始逐条结果（不入库）
  - reference/hub-probe.json                         脱敏摘要（入库，驱动 hub-api.md 状态列）

用法：python tools/Build/probe_hub_readonly.py [--rate 0.18] [--limit N]
"""
import argparse
import io
import json
import os
import re
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from StudentHub import HubEndpoints as HE  # noqa: E402

BASE = "https://api.xmyzstudent.com/api/v2"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
NEG_ID = "-1"


def _work_dir():
    return os.environ.get(
        "AUTOMXYZ_WORK",
        os.path.join(ROOT, "build_data"))


def probeOne(s, path, timeout=15):
    """返回 (分类, http状态, 业务code, 备注)。分类: public/auth/exists/missing/throttled/net。"""
    real = re.sub(r"\{[^}]*\}", NEG_ID, path)
    try:
        r = s.get(BASE + real, timeout=timeout)
    except Exception as e:
        return "net", 0, None, type(e).__name__
    try:
        doc = r.json()
    except Exception:
        # 502/503 非 JSON = 网关层限流/防护（实测连发 ~70 请求后触发），不是 404
        if r.status_code in (502, 503):
            return "throttled", r.status_code, None, "网关限流"
        return "exists" if r.status_code < 500 else "missing", r.status_code, None, "非JSON"
    code = doc.get("code") if isinstance(doc, dict) else None
    if r.status_code == 200 and code == 200:
        return "public", 200, 200, ""
    if code == 401 or r.status_code == 401:
        return "auth", r.status_code, 401, (doc.get("message") if isinstance(doc, dict) else "")
    if r.status_code == 404:
        return "missing", 404, code, ""
    if r.status_code == 405:
        return "exists", 405, code, "方法不符"
    if r.status_code >= 500:
        # 探测 id=-1 打进处理器后服务端 500：端点存在，参数不合
        return "exists", r.status_code, code, "服务端500(id=-1)"
    return "exists", r.status_code, code, "业务码=%s" % code


def main():
    ap = argparse.ArgumentParser(description="学社只读端点探测（免凭据）")
    ap.add_argument("--rate", type=float, default=0.18, help="请求间隔秒")
    ap.add_argument("--limit", type=int, default=0, help="只探前 N 个（冒烟）")
    a = ap.parse_args()

    import requests
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/json, text/plain, */*"})

    targets = [(m, p) for m, p, k, _, w in HE.REST_ENDPOINTS
               if k == "read" and "{}" not in p or k == "read"]
    targets = [(m, p) for m, p, k, _, _ in HE.REST_ENDPOINTS if k == "read"]
    if a.limit:
        targets = targets[:a.limit]
    print("学社只读探测：%d 个 GET 端点，限速 %.0fms" % (len(targets), a.rate * 1000))

    raw, netFail = [], 0
    t0 = time.time()
    for i, (m, p) in enumerate(targets, 1):
        kind, status, code, note = probeOne(s, p)
        if kind == "net":
            netFail += 1
            if netFail >= 5:
                print("连续 5 次网络错误，第 %d 条停手" % i)
                raw.append({"method": m, "path": p, "kind": "net", "status": 0,
                            "code": None, "note": "停手"})
                break
        else:
            netFail = 0
        raw.append({"method": m, "path": p, "kind": kind,
                    "status": status, "code": code, "note": note})
        print("  %-6s %-52s %s %s %s" % (m, p, kind, status, note))
        time.sleep(a.rate)
    print("第一遍耗时 %.1fs" % (time.time() - t0))

    # 二遍：被网关限流的端点放慢重探（实测 900ms 稳定）
    throttled = [(r["method"], r["path"]) for r in raw if r["kind"] in ("throttled", "net")]
    if throttled:
        print("二遍重探 %d 个限流/网络端点（间隔 1.2s）" % len(throttled))
        time.sleep(3)
        for m, p in throttled:
            kind, status, code, note = probeOne(s, p)
            time.sleep(1.2)
            for r in raw:
                if r["path"] == p and r["method"] == m:
                    r.update(kind=kind, status=status, code=code, note="二遍:" + note)
                    break
            print("  %-6s %-52s %s %s %s" % (m, p, kind, status, note))

    wd = _work_dir()
    os.makedirs(wd, exist_ok=True)
    rawPath = os.path.join(wd, "hub_probe_raw.json")
    with open(rawPath, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)

    summary = {}
    for row in raw:
        summary["%s %s" % (row["method"], row["path"])] = row["kind"]
    from collections import Counter
    stat = Counter(r["kind"] for r in raw)
    refPath = os.path.join(ROOT, "reference", "hub-probe.json")
    with open(refPath, "w", encoding="utf-8") as f:
        json.dump({"probedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "note": "免凭据 GET 探测（path 参数填 -1）；public=未登录可用，"
                           "auth=端点存在需登录，exists=端点存在但参数/方法不符，"
                           "missing=未挂载，net=网络错误",
                   "stats": dict(stat),
                   "results": summary}, f, ensure_ascii=False, indent=1)
    print("raw → %s\nsummary → %s\n统计：%s" % (rawPath, refPath, dict(stat)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

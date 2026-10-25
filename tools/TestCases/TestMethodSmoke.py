"""具名方法安全冒烟 —— 可重复运行的线上测试（需有效会话）。

范围纪律：
  - 只测 **GET 型 + 注册表 kind==read + 无必填参数** 的具名方法；
  - 写方法（POST）与带必填参数的方法**一律跳过**——空参调用写端点有真实副作用；
  - 每方法间隔 150ms。

判定：
  - success/dict/list = PASS；business-false 单列（教师角色拦截 / 导出流 / 缺必填参数，
    属预期，不算失败）；
  - **404 死路由 = FAIL**（对应注册表 GONE 名单，方法 md 应有标注）；
  - 网络超时单列，不算失败（重跑即可）。

用法：python -B tools/TestCases/TestMethodSmoke.py [--rate 0.15] [--report out.json]
"""
import argparse
import inspect
import json
import re
import sys
import time
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from XMYZClient import XMYZClient  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="具名方法安全冒烟（GET+read+无必填）")
    ap.add_argument("--rate", type=float, default=0.15)
    ap.add_argument("--report", default="")
    a = ap.parse_args()

    rows = json.load(open(os.path.join(ROOT, "..", "_xmyz_build_data", "endpoints.json"),
                          encoding="utf-8")) \
        if os.path.exists(os.path.join(ROOT, "..", "_xmyz_build_data", "endpoints.json")) else []
    kind_of = {r["endpoint"].lstrip("/"): r["kind"] for r in rows}

    c = XMYZClient()
    results = []
    from collections import Counter
    res = Counter()

    for name in sorted(dir(XMYZClient)):
        if name.startswith("_"):
            continue
        m = getattr(XMYZClient, name)
        if not callable(m):
            continue
        try:
            src = inspect.getsource(m)
        except Exception:
            continue
        if "self.get(" not in src:
            continue
        eps = [e.lstrip("/") for e in
               re.findall(r"[A-Za-z0-9_\-/]+![A-Za-z]+\.action", src)]
        eps = [e for e in eps if e in kind_of]
        if not eps or any(kind_of[e] != "read" for e in eps):
            continue
        sig = inspect.signature(m)
        if any(p.default is p.empty and p.name not in ("self", "kw")
               for p in sig.parameters.values()):
            continue
        fn = getattr(c, name)
        verdict = None
        detail = ""
        try:
            r = fn()
            if isinstance(r, dict):
                if r.get("success") is True:
                    verdict = "PASS"
                elif r.get("_status") == 404:
                    verdict = "FAIL404"
                    detail = "GONE 死路由"
                elif r.get("success") is False:
                    verdict = "BIZ"
                    detail = str(r.get("message", ""))[:50]
                else:
                    verdict = "PASS"
            elif isinstance(r, list):
                verdict = "PASS"
            else:
                verdict = "PASS"
        except Exception as e:
            msg = str(e)
            verdict = "NET" if ("timeout" in msg.lower() or "connection" in msg.lower()) else "ERR"
            detail = msg[:60]
        results.append({"method": name, "verdict": verdict, "detail": detail})
        res[verdict] += 1
        if verdict in ("FAIL404", "ERR"):
            print(f"  [{verdict}] {name} {detail}", flush=True)
        time.sleep(a.rate)

    print("\n结果分布:", dict(res))
    print("总计:", sum(res.values()),
          "| PASS:", res["PASS"] + res["✓"] if "PASS" in res else res.get("PASS", 0) + sum(v for k, v in res.items() if k == "PASS"),
          "| FAIL404:", res["FAIL404"],
          "| BIZ(预期):", res["BIZ"],
          "| NET:", res["NET"])
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print("report →", a.report)
    return 0 if res["FAIL404"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

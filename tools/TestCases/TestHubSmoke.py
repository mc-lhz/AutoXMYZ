"""学社具名方法安全冒烟（线上，需有效 token）。

范围：**GET 型 + 无必填参数**的具名方法逐个调用；写方法（POST/PUT/DELETE）
与带必填参数的方法一律跳过——空参写调用有真实副作用。

判定：
  - OK = 正常返回（信封已由传输层解包）；
  - 403 = 本账号无该管理权限（**预期，不算失败**，服务端授权边界）；
  - BIZ-4xx = 缺参数/未绑定等业务拒绝（预期）；
  - AUTH401 = token 失效（先跑 HubSession.py check）；
  - NET/ERR = 网络或未知异常。

用法：python -B tools/TestCases/TestHubSmoke.py [--rate 0.16]
"""
import argparse
import inspect
import os
import sys
import time
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from StudentHubClient import StudentHubClient  # noqa: E402
from StudentHub.HubTransport import HubError, HubAuthError  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="学社具名方法安全冒烟（GET+无必填）")
    ap.add_argument("--rate", type=float, default=0.16)
    a = ap.parse_args()

    c = StudentHubClient()
    from collections import Counter
    res, details = Counter(), []

    for name in sorted(dir(StudentHubClient)):
        if name.startswith("_") or name in ("healthCheck", "summary"):
            continue
        m = getattr(StudentHubClient, name)
        if not callable(m):
            continue
        try:
            src = inspect.getsource(m)
        except Exception:
            continue
        if "self.get(" not in src:
            continue
        if any(w in src for w in ("self.post(", "self.put(", "self.delete(")):
            continue
        req = [p for p in inspect.signature(m).parameters.values()
               if p.default is p.empty and p.name != "self"]
        if req:
            continue
        try:
            getattr(c, name)()
            res["OK"] += 1
        except HubAuthError:
            res["AUTH401"] += 1
            details.append((name, "401"))
        except HubError as e:
            if e.code == 403:
                res["403无权限"] += 1
            else:
                res["BIZ-%s" % e.code] += 1
                details.append((name, "%s %s" % (e.code, e.message[:36])))
        except Exception as e:
            res["NET/ERR"] += 1
            details.append((name, str(e)[:50]))
        done = sum(res.values())
        if done % 20 == 0:
            print(f"  ... 已测 {done} 个（{dict(res)}）", flush=True)
        time.sleep(a.rate)

    print("学社具名方法冒烟（GET 型+无必填）:", sum(res.values()), "个")
    print("分布:", dict(res))
    for name, d in details[:20]:
        print(f"  {name:44s} {d}")
    bad = res["AUTH401"] + res["NET/ERR"]
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
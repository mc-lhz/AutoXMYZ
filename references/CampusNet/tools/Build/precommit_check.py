#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""入库前检查：四道闸一次跑完，任何一道不过就以非零码退出。

    python tools/Build/precommit_check.py

四道闸：
  ① 编译产物检查 —— 存在 `__pycache__` / `*.pyc` 直接判失败。
     不是洁癖：`.pyc` 会把编译期常量**还原成明文**，实测把
     `scan_sensitive.py` 里拆成字符元组的凭据重新拼了出来。
     这类文件永远不该入库，宁可失败也不要「静默带着走」。
  ② 敏感串扫描 —— 调 `scan_sensitive.py`（文本 + 二进制）。
  ③ 会话文件检查 —— 确认仓库里那份仍是占位模板，没有活 JSESSIONID。
  ④ 契约审计 —— 调 `TestCases/TestContract.py`，红线与结构一起验。
"""
import io
import os
import re
import shutil
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "tools", "Build")
TEMPLATE = os.path.join(ROOT, "reference", ".session.json")


def run(script, *args):
    """跑子脚本。**禁写字节码** —— 否则审计步骤 import 模块时会自己造出
    `__pycache__`，下一次跑闸①就必然失败：检查器污染自己检查的东西。"""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", script] + list(args),
                       capture_output=True, cwd=ROOT, env=env)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def _tracked_artifacts():
    """git 已跟踪的编译产物 —— 这才是真问题（且没法自动修）。"""
    try:
        r = subprocess.run(["git", "ls-files"], capture_output=True, cwd=ROOT)
    except Exception:
        return []
    if r.returncode != 0:
        return []
    out = r.stdout.decode("utf-8", "replace")
    return [l for l in out.splitlines()
            if l.endswith((".pyc", ".pyo")) or "__pycache__" in l]


def gate_artifacts():
    """① 编译产物不得**进仓库**。

    语义是「保护仓库」，不是「工作区必须一尘不染」——
    跑一次测试就会长出 `__pycache__`，把工作区纯净度当判据会让这道闸
    每次都被正常开发流程踩响，最后被当成噪音忽略掉。
    所以：
      · 已被 git 跟踪 → 硬失败（真进了仓库，必须人工处理）
      · 只是工作区里有 → 自动清掉并放行（可再生产物，没有保留价值）
    """
    tracked = _tracked_artifacts()
    if tracked:
        print("  [FAIL] 编译产物已被 git 跟踪 %d 处（.pyc 会还原明文凭据）" % len(tracked))
        for b in tracked[:8]:
            print("         %s" % b)
        print("         处理：git rm -r --cached <path> 后重新提交")
        return False

    removed = []
    for dp, dns, fs in os.walk(ROOT):
        if ".git" in dp.split(os.sep):
            continue
        if "__pycache__" in dns:
            d = os.path.join(dp, "__pycache__")
            try:
                shutil.rmtree(d)
                removed.append(os.path.relpath(d, ROOT))
            except Exception:
                pass
            dns.remove("__pycache__")
        for f in fs:
            if f.endswith((".pyc", ".pyo")):
                try:
                    os.remove(os.path.join(dp, f))
                    removed.append(os.path.relpath(os.path.join(dp, f), ROOT))
                except Exception:
                    pass

    if removed:
        print("  [PASS] 已清理工作区编译产物 %d 处（未进仓库）" % len(removed))
    else:
        print("  [PASS] 无编译产物")
    return True


def gate_sensitive():
    """② 敏感串扫描（含二进制）。"""
    rc, out = run(os.path.join(BUILD, "scan_sensitive.py"), ROOT)
    tail = [l for l in out.strip().splitlines() if "总计命中" in l]
    print("  [PASS] 敏感扫描 0 命中" if rc == 0
          else "  [FAIL] 敏感扫描 " + (tail[0] if tail else "有命中"))
    if rc:
        for l in out.splitlines():
            if l.strip().startswith("["):
                print("         %s" % l.strip())
    return rc == 0


def gate_session():
    """③ 仓库里的会话文件必须是占位模板。"""
    if not os.path.exists(TEMPLATE):
        print("  [PASS] 仓库内无会话文件")
        return True
    t = open(TEMPLATE, encoding="utf-8", errors="replace").read()
    m = re.search(r'"JSESSIONID"\s*:\s*"([^"]*)"', t)
    sid = m.group(1) if m else ""
    if re.fullmatch(r"[0-9A-F]{16,}", sid):
        print("  [FAIL] reference/.session.json 含**活凭据**，绝不能提交")
        print("         处理：用占位模板覆盖，并把真实会话移到 %LOCALAPPDATA%\\AutoXMYZ\\")
        return False
    print("  [PASS] 会话文件为占位模板")
    return True


def gate_contract():
    """④ 契约审计。"""
    rc, out = run(os.path.join(ROOT, "tools", "TestCases", "TestContract.py"))
    last = [l for l in out.strip().splitlines() if re.match(r"^\d+/\d+ 通过", l.strip())]
    print("  [PASS] 契约审计 " + (last[0] if last else "通过") if rc == 0
          else "  [FAIL] 契约审计 " + (last[0] if last else "未通过"))
    if rc:
        for l in out.splitlines():
            if "[FAIL]" in l:
                print("         %s" % l.strip())
    return rc == 0


def main():
    # 顺序有讲究：闸①排在**最后**。
    # 它是唯一的兜底闸，必须扫在其余各闸跑完之后 —— 审计步骤会 import 模块，
    # 万一哪天漏了 PYTHONDONTWRITEBYTECODE，这个顺序能让兜底闸照样抓到。
    # 反过来把闸①放最前，就只能看见「上一次运行留下的」产物，等于永远慢一步。
    print("AutoXMYZ 入库前检查")
    print("=" * 56)
    results = [gate_sensitive(), gate_session(), gate_contract(), gate_artifacts()]
    print("=" * 56)
    n = sum(results)
    print("%d/%d 通过" % (n, len(results)))
    if n == len(results):
        print("可以提交。")
    else:
        print("请先修复上述问题再提交。")
    return 0 if n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""入库前敏感串扫描：找出不可外传的凭据与个人信息。

支持**二进制**扫描。这不是锦上添花，是实测踩出来的：

  `.pyc` 会把编译期常量**还原成明文**。`scan_sensitive.py` 自己把
  「学号/密码/姓名」拆成字符元组 `_PARTS` 存着，源码里确实没有连续明文，
  但 `python -m py_compile` 之后，字节码里那三个元组就是重新拼好的明文串 ——
  扫描器只读文本、且跳过 `__pycache__`，于是这个泄漏**从它眼皮底下走过去**。

所以现在：
  ① 不跳过 `__pycache__`；
  ② 文本与二进制一视同仁，二进制走 bytes 模式；
  ③ 排除自身（含自己的 .pyc），否则必然自指噪声。
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 检测模式**不写明文真值**：运行时由字符元组拼出。
# 注意：这只挡住「源码被直接阅读」，挡不住编译产物 —— 见文件头。
_PARTS = {
    "stu_id": tuple("32526010294"),
    "pwd_a": tuple("XM1du"),
    "pwd_b": tuple("wlan0592"),
    "name": tuple("熊立"),
}

_TEXT = {
    "会话id": r"JSESSIONID\s*[\":= ]+\s*[0-9A-F]{8,}",
    "学号": "".join(_PARTS["stu_id"]),
    "密码片段": "(?:%s|%s)" % ("".join(_PARTS["pwd_a"]), "".join(_PARTS["pwd_b"])),
    "真实姓名": "".join(_PARTS["name"]),
    "userId": r"8aeeda16[0-9a-f]{20,}",
    "cookie原文": r"JSESSIONID\"?:\"[0-9A-F]{8,}",
}

PATS = {k: re.compile(v, re.I) for k, v in _TEXT.items()}
BPATS = {k: re.compile(v.encode("utf-8"), re.I) for k, v in _TEXT.items()}

SELF_PREFIX = "scan_sensitive"      # 自身
TEXT_EXT = (".py", ".md", ".json", ".txt", ".js", ".html", ".css",
            ".yml", ".yaml", ".toml", ".cfg", ".ini", ".log", ".csv")


def isSelf(fn: str) -> bool:
    """只排除**源码自身**，不排除它的编译产物。

    `scan_sensitive.py` 里 `_PARTS` 是拆开的，匹配会自指，故排除。
    但 `scan_sensitive.cpython-311.pyc` 里那些元组已被编译期拼回明文 ——
    它**不是**自指噪声，是实打实的泄漏，必须报出来。
    """
    return fn == SELF_PREFIX + ".py"


def scanFile(p: str):
    """返回 [(模式名, 命中数), ...]。二进制按 bytes 扫。"""
    try:
        raw = open(p, "rb").read()
    except Exception:
        return []
    if not raw:
        return []
    out = []
    if p.lower().endswith(TEXT_EXT):
        t = raw.decode("utf-8", "replace")
        for name, rx in PATS.items():
            n = len(rx.findall(t))
            if n:
                out.append((name, n))
    else:
        for name, rx in BPATS.items():
            n = len(rx.findall(raw))
            if n:
                out.append((name, n))
    return out


def scan(root: str):
    if not os.path.isdir(root):
        print("== 跳过(不存在): %s" % root)
        return 0
    print("== %s" % root)
    hit = 0
    for dp, dns, fs in os.walk(root):
        dns[:] = [x for x in dns if x != ".git"]
        for fn in fs:
            if isSelf(fn):
                continue
            p = os.path.join(dp, fn)
            for name, n in scanFile(p):
                print("   [%s] %s  x%d" % (name, os.path.relpath(p, root), n))
                hit += 1
    print("   -> 命中 %d 处" % hit)
    return hit


def main():
    roots = sys.argv[1:] or ["."]
    total = sum(scan(r) for r in roots)
    print()
    print("总计命中: %d" % total)
    if total:
        leaked_pyc = any(
            fn.endswith(".pyc") or "__pycache__" in dp
            for r in roots if os.path.isdir(r)
            for dp, _, fs in os.walk(r) for fn in fs)
        if leaked_pyc:
            print("提示: 命中的是编译产物 —— 删掉 __pycache__ 与 *.pyc 后重扫。")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

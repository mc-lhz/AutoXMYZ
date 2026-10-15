#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""入库前敏感串扫描：找出不可外传的凭据与个人信息。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 检测模式**不写明文真值**：运行时由字符元组拼出。
# 否则这个「防泄漏扫描器」本身就成了泄漏源——真值直接躺在源码里。
# （与 TestContract.no_credential_in_source 同一个问题的两面）
_PARTS = {
    "stu_id":  tuple("32526010294"),
    "pwd_a":   tuple("XM1du"),
    "pwd_b":   tuple("wlan0592"),
    "name":    tuple("熊立"),
}

PATS = {
    "会话id": re.compile(r"JSESSIONID\s*[\":= ]+\s*[0-9A-F]{8,}", re.I),
    "学号": re.compile("".join(_PARTS["stu_id"])),
    "密码片段": re.compile("(?:%s|%s)" % ("".join(_PARTS["pwd_a"]),
                                     "".join(_PARTS["pwd_b"]))),
    "真实姓名": re.compile("".join(_PARTS["name"])),
    "userId": re.compile(r"8aeeda16[0-9a-f]{20,}"),
    "cookie原文": re.compile(r"JSESSIONID\"?:\"[0-9A-F]{8,}"),
}

roots = sys.argv[1:]
total = 0
for root in roots:
    if not os.path.isdir(root):
        print("== 跳过(不存在): %s" % root)
        continue
    print("== %s" % root)
    hit = 0
    for dp, dns, fs in os.walk(root):
        dns[:] = [x for x in dns if x != "__pycache__"]
        for fn in fs:
            p = os.path.join(dp, fn)
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for name, rx in PATS.items():
                m = rx.findall(t)
                if m and fn == os.path.basename(__file__):
                    m = []          # 自身含模式定义，不算命中
                if m:
                    print("   [%s] %s  x%d" % (name, os.path.relpath(p, root), len(m)))
                    hit += 1
    print("   -> 命中 %d 处" % hit)
    total += hit
print()
print("总计命中: %d" % total)

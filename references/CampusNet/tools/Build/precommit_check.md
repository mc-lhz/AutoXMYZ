入库前检查：四道闸一次跑完，任何一道不过就以非零码退出。

```bash
python tools/Build/precommit_check.py
```

四道闸：

1. **编译产物检查** —— 存在 `__pycache__` / `*.pyc` 直接判失败。
   不是洁癖：`.pyc` 会把编译期常量**还原成明文**，实测把
   `scan_sensitive.py` 里拆成字符元组的凭据重新拼了出来。
   这类文件永远不该入库，宁可失败也不要「静默带着走」。
2. **敏感串扫描** —— 调 `scan_sensitive.py`（文本 + 二进制）。
3. **会话文件检查** —— 确认仓库里那份仍是占位模板，没有活 JSESSIONID。
4. **契约审计** —— 调 `TestCases/TestContract.py`，红线与结构一起验。

---
**开发提示**：本仓库内**不要用 `py_compile` 做语法校验** —— 它会写出
`__pycache__`，下次入库前检查就报失败。用内存编译代替：

```bash
python -c "import sys; compile(open(sys.argv[1],encoding='utf-8').read(), sys.argv[1], 'exec'); print('OK')" tools/XMYZClient.py
```

# TestMethodSmoke — 具名方法安全冒烟（线上，需会话）

273 个具名方法里 **GET 型 + 注册表 kind==read + 无必填参数** 的方法逐个调用并分桶。
**写方法与带必填参数的方法一律跳过**——空参调用写端点有真实副作用。

## 判定

| verdict | 含义 |
|---|---|
| PASS | success / dict / list 正常返回 |
| BIZ | business-false：教师角色拦截、导出流、缺必填参数——**预期内，不算失败** |
| FAIL404 | GONE 死路由——**唯一算失败的判定**（返回码 1） |
| NET | 网络超时，重跑即可 |

```bash
python -B tools/TestCases/TestMethodSmoke.py                  # 全量（约 1 分钟）
python -B tools/TestCases/TestMethodSmoke.py --report r.json  # 出报告
```

## 已知基线（2026-10-24）

PASS 66 / BIZ 41 / NET 7 / **FAIL404 2**（elective/activity-record 的
readByTeacher、exportByTeacher，已在 ElectiveActivity.md 标注）。

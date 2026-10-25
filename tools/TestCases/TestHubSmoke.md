# TestHubSmoke — 学社具名方法安全冒烟（线上，需 token）

**GET 型 + 无必填参数**的具名方法逐个调用；写方法与带必填参数的方法一律跳过。

| verdict | 含义 |
|---|---|
| OK | 正常返回（信封已解包） |
| 403无权限 | 本账号无该管理权限——**预期**，服务端授权边界 |
| BIZ-4xx | 缺参数/未绑定等业务拒绝——预期 |
| AUTH401 | token 失效，先跑 `HubSession.py check` |
| NET/ERR | 网络或未知异常（返回码 1） |

```bash
python -B tools/TestCases/TestHubSmoke.py
```

## 基线（2026-10-25）

46 个可安全冒烟方法：**OK 33 / 403无权限 11 / BIZ-400 2**
（getAdminAdmissionMembers 缺 groupId、getGradeExams 未绑好分数）。

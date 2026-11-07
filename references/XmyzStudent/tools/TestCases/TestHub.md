# TestHub — 学社契约审计（离线）

与 `TestContract.py` 同风格的离线审计，覆盖学社侧新增物：

| 组 | 检查 |
|---|---|
| 注册表 | 形态（路径/kind/重复）、wrapper 命名、is_write 与 kind 双向对称（未知端点 KeyError） |
| 门面 | 11 域方法齐备、MRO 里 HubHttp 居末位、**无方法同名覆盖**（同名即丢端点） |
| 传输 | 信封解包、code!=200 抛 HubError、401 抛 HubAuthError、Bearer 头、非 JSON 抛错（全部 mock，无网络） |
| 文档 | `reference/hub-api.md` 与注册表内存重生成一致（漂移即 FAIL，反文档腐化） |
| 安全 | StudentHub 目录无 32+ hex 凭据样例 |
| CLI | `StudentHubClient.py` / `HubSession.py` 的 `-h` 冒烟 |

```bash
python -B tools/TestCases/TestHub.py
```

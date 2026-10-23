# probe_hub_readonly — 学社只读端点全量探测

对 `HubEndpoints.py` 注册表里 **kind=="read"**（103 个 GET）逐个免凭据请求，
验证路径真实性并产出「公开 / 需登录」分类。**写端点一个不碰**——空 body 的写请求
无法保证服务端先鉴权后执行，风险不值得冒。

## 纪律

- 路径参数一律填 `-1`（不存在的 id，AGENTS.md 探测纪律）
- 限速默认 180ms；连续 5 次网络错误立即停手
- 401 是**预期且有用**的结果（端点存在且需登录），不是失败

## 分类语义

| kind | 含义 |
|---|---|
| `public` | 未登录即可用（200 + code 200） |
| `auth` | 端点存在，需登录（401） |
| `exists` | 端点存在，但当前参数/方法不符（业务码非 200/401、405 等） |
| `missing` | 404 未挂载 —— **注册表可能有过时条目，需核查** |
| `net` | 网络错误 |

## 产物

- `<AUTOMXYZ_WORK|build_data>/hub_probe_raw.json` —— 逐条原始结果（**不入库**）
- `reference/hub-probe.json` —— 脱敏摘要（入库），由 `gen_hub_api_md.py` 读它
  给 `reference/hub-api.md` 的 GET 行加「探测」列

```bash
python tools/Build/probe_hub_readonly.py              # 全量（约 30s）
python tools/Build/probe_hub_readonly.py --limit 5    # 冒烟
```

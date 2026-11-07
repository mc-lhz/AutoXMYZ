# gen_hub_api_md — 学社文档再生成

从 `StudentHub/HubEndpoints.py` 注册表派生两份文档（都是产物，不手改）：

1. `reference/hub-api.md` —— 全量端点清单（262 行表格）
2. `tools/StudentHub/<Mixin>.md` × 11 —— 各域方法表（同时满足
   TestContract 的「每 py 有同名 md」契约）

## 用法

```bash
python tools/Build/gen_hub_api_md.py
```

## 流程位置

端点变更：改 `HubEndpoints.py`（事实）→ 跑本脚本（文档）→ 跑 `TestCases/TestHub.py`
（一致性校验会比对内存重生成结果与落盘文件）。

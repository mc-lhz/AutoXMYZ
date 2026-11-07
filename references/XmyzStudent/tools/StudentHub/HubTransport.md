# HubTransport — 学社传输层

`api.xmyzstudent.com/api/v2` 的唯一 HTTP 出口。与 xmyz 的 `Access/HttpTransport.py`
完全独立（不同源站、不同鉴权模型）。

## 关键决策

| 决策 | 理由 |
|---|---|
| Bearer token（`Authorization` 头） | 站点前端 localStorage 存 token，axios 拦截器同款 |
| 无写拦截 `_guard` | 学社是学生自建平台，写操作是需求本身；读写分类保留在 `HubEndpoints.py` 供文档/统计 |
| 信封解包：`code==200 → data`，否则抛 `HubError` | 业务失败也是 HTTP 200（链路分析报告 §3.1），不解包会把失败当成功 |
| `401 → HubAuthError` | 唯一需要重新登录的信号 |
| 默认限速 150ms（`AUTOMXYZ_HUB_MIN_INTERVAL_MS` 可调，0 关闭） | 自建平台单实例，默认留喘息 |
| 会话文件在仓库外 `hub_session.json` | 同 xmyz 的路径隔离哲学：不配 .gitignore 也不会漏 |

## 常用入口

- `get/post/put/delete(path, params=, json=)` —— 薄包装统一走这里
- `upload(path, filepath, businessType=, field=, btField=)` —— multipart；
  站点业务字段名不统一（`/files/upload` 用 `business_type`，rating 用 `businessType`），故开放 `btField`
- `paged(path, params=, pageKey="page", sizeKey="size")` —— 学社分页；`data` 兼容
  裸数组 / `{records|list|items|rows, total}` 两种形态
- `wsSnapshots(wsPath, onFrame, seconds=)` —— WS 全量快照订阅（tally/debate）
- `saveDataUrl(dataUrl, out)` —— campus 验证码 dataURL 落盘

## 已踩过的坑

- 无参构造**必须自己读会话文件**（与 xmyz 同教训）：学社公开端点未登录也 200，
  静默未登录会表现为「公开数据正常、本人数据全 401」的半绿假象。
- `delete` 带 body 的端点（`/admin/messages/batch` 等）走 `json=` 参数，
  requests 原生支持，不要为了「DELETE 不该有 body」而改约定。

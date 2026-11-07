# XmyzStudent — 开发契约（学社 xmyzstudent.com）

本子树对应学生社区（JSON API，`api.xmyzstudent.com/api/v2`）。路径相对 `references/XmyzStudent/`。

## 架构

```
tools/
  StudentHubClient.py        门面：组合 12 域 mixin（284 端点全包装 + 辅助 14）
  StudentHub/
    HubTransport.py          Bearer、信封解包（code!=200→HubError，401→HubAuthError）、
                             150ms 限速、upload（business_type/businessType 双字段）、WS 快照
    HubSession.py            登录四式：campus(+验证码 vision/OCR) / normal / sms / token
    HubEndpoints.py          端点注册表（284 REST + 2 WS，事实唯一来源）
    AccountMixin.py          auth/user/sms/permissions
    AdmissionMixin.py        纳新/准入
    PortalMixin.py           横幅/年级绑定/文件/音乐
    MessageMixin.py          站内消息（收发 + 管理端群发/模板）
    TallyMixin.py            实时唱票（REST + WS）
    CampaignMixin.py         投票征集
    TicketMixin.py           电子票务
    MuseumMixin.py           校园博物馆
    RatingMixin.py           评分社区（74 端点）
    VoicesMixin.py           声音问答
    CampusMixin.py           校区/楼宇/时段 + 用户检索
    DebateMixin.py           辩论场（WS）
  Common/Logcat.py           彩色日志（单例 Log）
  Common/Ocr.py              自包含验证码 OCR（与 CampusNet 同源同参）
  Build/gen_hub_api_md.py    从注册表派生 hub-api.md 与各 Mixin.md
  Build/probe_hub_readonly.py 只读端点探测（限流→二遍慢速重探）
  TestCases/TestHub.py       离线契约 15 项
  TestCases/TestHubSmoke.py  具名方法冒烟（GET+无必填）
```

- `reference/hub-api.md` — 端点清单（生成产物）；`reference/hub-probe.json` — 探测摘要
- 每个 `.py` 有同名 `.md`；每个业务目录有 `__init__.py`

## 关键契约

- **认证拓扑**：campus 登录 = 学社服务端拿同一学号密码回调 CampusNet 校验；
  客户端只需同一凭据 + 学社自己的验证码。凭据与 CampusNet/XinYiWo 同源。
- **信封**：`{code,message,data}`；业务失败也是 HTTP 200，`code!=200` 抛 `HubError`；
  401 → `HubAuthError`（重登，不换参重试）
- **分页**：`page` + `size`（部分 `pageSize`）
- **WS**：`/ws/tally/activity/{id}`、`/ws/debate/round/{id}`（全量快照，单向）
- **写能力**：本站功能完备不设客户端闸门；删除类方法名显式含 `delete`
- **生成方法**：`payload` 参数必须真发 body（`self.post(path, json=payload)`）；
  TestHub 的「payload 不丢体」闸防回归（曾有 36 个空体方法）
- **文档反漂移**：端点事实只改 `HubEndpoints.py` → 跑 `gen_hub_api_md.py`；
  TestHub 比对内存重生成与落盘文档

## 开发契约

- 命名：目录/文件/类大驼峰、方法小驼峰；同 CampusNet
- 新增端点 = 改 `HubEndpoints.py` + 对应 mixin + 重跑文档生成 + TestHub 绿
- 每 py 同名 md；业务目录有 `__init__.py`
- `HubHttp` 留在继承链末位

## 已踩过的坑

1. **生成器系统性漏 body**：透传型 POST 产出「有 payload 参数却不发 body」的空体方法
   （rating comments/ratings、campaign、museum、ticket 等 36 个）→ 已修复 + 防回归闸
2. **裸 HubHttp 调 mixin 方法**：HubSession 曾用裸 `HubHttp` 调 `getMyProfile()`
   → AttributeError；会话模块只能走原始端点或组合门面
3. **限流伪装 404**：连发 ~70 请求后网关 502 非 JSON，形似 404；
   探测必须归类 throttled 并二遍 1.2s 慢速重探（实测 29 个假 missing 全部存在）
4. **同名方法覆盖**：MRO 同名即丢端点；TestHub 的「无方法覆盖」闸盯住
5. **模板字面量基址**：`${ratingConst0}` 等占位基址纯「/开头」正则抓不到；
   提取须解析常量取并集

## 常用命令

```bash
python tools/StudentHub/HubSession.py captcha
python tools/StudentHub/HubSession.py campus -a <学号> -p <密码> --code ab12
python tools/StudentHubClient.py --health
python tools/TestCases/TestHub.py
python tools/TestCases/TestHubSmoke.py
python tools/Build/gen_hub_api_md.py
python tools/Build/probe_hub_readonly.py
```

## 安全纪律

- token/手机号/他人主页不落仓库；会话在 `%LOCALAPPDATA%\AutoXMYZ\hub_session.json`
  （`AUTOMXYZ_HUB_SESSION` 可覆盖），验证码暂存 `hub_captcha_pending.json`
- **安全提示**：学社登录会把密码经学社服务器转发 CampusNet（站点设计），
  不可信网络下勿用学社登录态
- `reference/` ≤150KB（当前 ≈32KB）；测试报告写 `build_data`（`AUTOMXYZ_WORK`）不入库
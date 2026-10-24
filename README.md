# AutoXMYZ

厦门一中**双源站**工具集：校内系统（`xmyz.xmedu.cn`）**纯只读**查询 +
学生社区（`xmyzstudent.com`，下称「学社」）**功能完备**客户端。

## 两个源站

| 门面 | 源站 | 鉴权 | 能力 |
|---|---|---|---|
| `XMYZClient` | `xmyz.xmedu.cn`（Struts2） | JSESSIONID | 2606 端点读写均可用（政策 2026-10-24 修订） |
| `StudentHubClient` | `api.xmyzstudent.com/api/v2` | Bearer token | 284 REST + 2 WS，读写齐备 |

## xmyz 三个前端入口

| 入口 | 技术栈 | 角色 |
|---|---|---|
| `manager.html` | ExtJS 3.4，服务端驱动按需加载 | **桌面管理端**，学校门户「登录」按钮指向的正式入口 |
| `m2.html` | Vue 3 + Vant，hash 路由 | 移动端新版，待办审批 + 4 项委托功能 |
| `m.html` | Vue 2 + Vux | 移动端旧版，已被 m2 取代 |

三者共用同一 `JSESSIONID`（`Path=/`，同源），一份会话通吃。

### xmyz 端点枚举结果

合并去重后 **2606** 个唯一端点（只读 1176 / 写类 1430；2026-10-24 用真实会话
对线上重新对账）：

- **桌面端 489** —— 登录后由菜单树按当前账号权限下发，再按每个菜单节点携带的
  `action.jsFile` 定向抓取 **97 个模块**（1.5 MB）得到，是当前账号有权访问的实况
  （本次重抓 97/97 全命中，端点集与初版清单**零漂移**）
- **m2.html 2116** —— 前端已改版重建（rolldown 细粒度 chunk 2161 个/13.9 MB），
  端点面从 185 涨到 2116（本学年新增大量 activiti 工作流）；bundle 静态提取，
  能力面以运行时权限为准
- **m.html 10** —— legacy 懒加载，保留初版登记

端点层三方几乎不重叠（共有 0 个）；功能层互补：桌面端独占 `community`(111 社团)、
`elective`(96 选课)、`quality`(30 综评)、`volunteer`(19)；
m2 独占 `activiti/*`(72 审批流)、`archive/*`(23)——分工是设计好的。

## 学社功能域（284 端点）

账号/绑定/短信、门户横幅、年级考试绑定、文件上传、音乐与 QQ 音乐、站内消息、
**实时唱票**（REST + WS 快照）、投票征集、电子票务（抢票/核销/审核）、校园博物馆、
评分社区（74 端点，含投稿/评论/后台）、声音问答、校区楼宇时段、辩论场（WS）、
**纳新/准入**（2026-10 新增域：分组/成员/豁免/扫码 + 用户验证）。

2026-10-24 已对线上新版前端（index-D2vbWxba.js）重新对账：114 个 GET 全量免凭据
探测（公开 14 / 需登录 83 / 存在·需参数 17 / 缺失 0），鉴权态抽样返回真实数据。

## 用法

```bash
# xmyz 校内系统
python tools/Access/LoginSession.py password -u <学号> -p <密码>   # 登录
python tools/XMYZClient.py --health                                 # 会话自检
python tools/TestCases/TestApiReadOnly.py                           # 只读 35 项

# 学社
python tools/StudentHub/HubSession.py captcha                       # ① 取验证码图
python tools/StudentHub/HubSession.py campus -a <校园网账号> -p <密码> --code ab12  # ② 提交
python tools/StudentHubClient.py --health                           # 会话自检

# 审计（离线）
python tools/TestCases/TestHub.py
python tools/TestCases/TestContract.py
```

```python
import sys; sys.path.insert(0, "tools")
from XMYZClient import XMYZClient
c = XMYZClient()
c.status(); c.menuTree(); c.quality(); c.myScores(); c.transcript()
c.growthRecords(); c.myCommunities(); c.myVolunteerActivities(); c.inbox()

from StudentHubClient import StudentHubClient
h = StudentHubClient()
h.healthCheck()
h.getAdminTallyActivities()                    # 唱票活动列表
h.voteAdminTallyCandidates(candidateId, 10)    # 录票 +10
h.searchRatingItems("食堂")                     # 评分社区
```

## 红线

**xmyz 读写均可用（2026-10-24 修订）。** 早年 `_guard` 拦截已解除；
`tools/endpoint_kind.py` 的读写分类保留为文档口径（1176 读 / 1430 写）。
写纪律：只写本人数据、可逆优先、不碰他人密码与审批流——服务端权限仍是最终边界。

**学社功能完备。** 站点为学生自建平台，写操作是需求本身（唱票、审核、发布）；
传输层不设拦截，但删除类方法名显式含 delete，`HubEndpoints.is_write(path, method)`
仅作文档标注。端点事实唯一来源 `tools/StudentHub/HubEndpoints.py`，
清单见 `reference/hub-api.md`。

## 构建中踩到的坑

1. **端点分类不能用正则硬拼** —— 旧实现每分支后接 `\.action$`，
   `approve` 只匹配到 `approvedComplete` 前 7 字母就断，**漏判 88 个写端点**。
2. **默认构造必须自己读会话文件** —— 曾写成 `elif cookie:`，无参构造静默以未登录身份运行；
   而未登录时只读端点照样返回 200，于是「测试全绿」而一条真实数据都没取到。
   学社侧同坑：公开端点未登录也 200，本人数据 401，半绿假象更隐蔽。
3. **`loggedIn` 不能判会话** —— 登录后该字段直接消失，`== False` 判永远误报未登录。
   xmyz 判据是 profile 有 `loginName`；学社判据是 `/user/profile` 有 `username`。
4. **响应有两类** —— 除 `{"total":n,"data":[],"success":true}` 信封外，
   还有裸数组/裸对象（`dict!getTree`、`grade!loadTree` 等），只认信封会误报 5 个 FAIL。
   学社信封是 `{code, message, data}` 且**业务失败也是 HTTP 200**。
5. **`send` 同名两义** —— `attachment!send` 是下载（读），
   `short-message-detail!send` 是真发短信（写），须按 namespace 分流。
6. **学社端点提取不能用单一正则** —— 管理端基址是模板字面量
   `` `${ratingConst0}/...` ``（约 50 端点不以 `/` 开头），
   纯「以 / 开头」的匹配全部漏掉；必须解析常量后取**并集**再对账。
7. **分类器不能逐个枚举，要有后缀通则** —— 新版 m2 的上百个工作流动作
   （officeApprovalComplete / noticeComplete / deptLeaderComplete…）若靠
   WRITE_EXACT 枚举必漏；改为 `WRITE_SUFFIX = (Complete, Approval, Save,
   Create, Update)` 通则后一次归位。另外 merge 曾内置第二套 WRITE_HINT
   正则算 kind（违反单一来源红线），已废除。
8. **网关限流会伪装成 404/500** —— 连发 ~70 请求后 xmyz/学社都会 502/超时，
   探测必须二遍慢速重探（学社实测 29 个假 missing 复测全部存在）。

完整清单与探测结果见 [`reference/api.md`](reference/api.md)（xmyz）与
[`reference/hub-api.md`](reference/hub-api.md)（学社）。

## 依赖

`requests`、`rapidocr-onnxruntime`（验证码 OCR，可选）、`numpy` + `Pillow`、
`websocket-client`（学社 WS 快照，可选）。

## 红线与隐私

账号信息、凭据、导出文件不入库。`reference/.session.json` 是**占位模板**，
登录后由脚本覆写，提交前请确认内容已脱敏。
学社会话（`hub_session.json`）与验证码暂存（`hub_captcha_pending.json`）
一律写在仓库外用户目录。
入库文档禁止出现真实姓名与真实 token，一律写「某学生」。

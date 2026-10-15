---
name: AutoXMYZ
description: 厦门一中信息校园综合应用系统（xmyz.xmedu.cn）只读查询工具集。Use when the user mentions xmyz、厦一中、一中校园、综合素质评价、成绩单、成绩查询、成长记录、志愿者、社团、电子成绩单、待办审批、校园短信、菜单树，或要查询本人的综评记录、成绩、成长记录、社团与志愿活动、短信通知、通知公告。
---

# 厦门一中信息校园综合应用系统（xmyz.xmedu.cn）使用指南

> **使用范围与红线**：本技能**纯只读**。仅用于快捷查询本人数据，
> 不得用于*攻击、压力测试、窥探隐私*；不得用于发布*涉黄、涉暴、危害国家安全、颠覆国家统一的内容*；
> 发现越权或泄露类问题时*只上报、不封装*。
> 任何**写操作**（提交、审批、删除、上传、改密码）**一律不在能力范围内**，
> 由 `Access/HttpTransport.py::_guard` 强制拦截。
> 含未成年人个人信息——*账号信息、凭据、导出文件不入库、不外传*。

目标站：`https://xmyz.xmedu.cn`（Struts2 后端，`模块!方法.action`）
纯 HTTP 完成全部读操作，无需浏览器。

---

## 三个前端入口

| 入口 | 技术栈 | 角色 |
|---|---|---|
| `manager.html` | ExtJS 3.4，服务端驱动按需加载 | **桌面管理端**，学校门户「登录」按钮指向的正式入口 |
| `m2.html` | Vue 3 + Vant，hash 路由 | 移动端新版，待办审批 + 4 项委托功能 |
| `m.html` | Vue 2 + Vux | 移动端旧版，已被 m2 取代 |

三者**共用同一 `JSESSIONID`**（`Path=/`，同源），一份会话通吃。

合并去重后 **683** 个唯一端点（只读 360 / 写类 323）。
**端点层几乎不重叠**（三方共有 0 个）——三个前端各写各的 Action 名；
功能层互补，桌面端没有 `activiti/*` 审批流，移动端没有 `quality/*` 综评面板。

---

## 登录

```bash
# ① 优先：有读图能力走 vision（实测 100%）
python tools/Access/LoginSession.py vision                                   # 取验证码图
python tools/Access/LoginSession.py vision -u <学号> -p <密码> --code ab12   # 看图后提交

# ② 无读图能力：OCR 变体池投票
python tools/Access/LoginSession.py password -u <学号> -p <密码> --retry 6

# ③ 浏览器已登录：直接复制会话，免验证码
python tools/Access/LoginSession.py jsessionid --jsessionid <JSESSIONID>

# 无凭据探测端点可达性
python tools/Access/LoginSession.py check
```

会话落在 `reference/.session.json`。

**有读图能力却去用 OCR 是浪费；无读图能力却去用 vision 则会卡在 `--code`。**

---

## 使用

```python
import sys; sys.path.insert(0, "tools")
from XMYZClient import XMYZClient

c = XMYZClient()                  # 自动读 reference/.session.json
c = XMYZClient(token="<JSESSIONID>")

c.status()                        # 本人账号与学籍摘要
c.menuTree()                      # 有权访问的菜单树（端点清单权威来源）
c.quality()                       # 综合素质评价总表
c.myScores()                      # 我的成绩
c.transcript()                    # 电子成绩单
c.growthRecords()                 # 我的成长记录
c.myCommunities()                 # 我参与的社团
c.myVolunteerActivities()         # 我参与的志愿活动
c.inbox()                         # 短信收件箱
c.schoolTermCombo()               # 学期下拉
```

分页方法（`myScores` / `quality` / `inbox` / `growthRecords` …）返回 `(rows, summary)`，
内部按桌面端契约 `start` + `limit` 循环，上限 2000 行。

```bash
python tools/XMYZClient.py --health     # 会话自检
python tools/XMYZClient.py --summary    # 跨域摘要
```

---

## 命令速查

```bash
python tools/TestCases/TestApiReadOnly.py                  # 只读全量 35 项
python tools/TestCases/TestApiReadOnly.py --limit 20       # 冒烟
python tools/TestCases/TestApiReadOnly.py --report r.json  # 出报告
python tools/TestCases/TestContract.py                     # 契约与红线审计（离线）
```

---

## 端点与分页契约

- 桌面端分页参数是 `start` + `limit`（`Config.js` 里 `LIMIT=60`），**不是** m2 的 `page`/`pageSize`
- 响应有两类，**都要能处理**：
  - 信封型 `{"total": n, "data": [...], "success": true}`
  - **裸数组 / 裸对象**（`dict!getTree`、`grade!loadTree`、`recipient!statInfo`、`community!loadTree`）
- 业务失败是 `{"success": false, "message": "..."}`，**`success:false` 不等于端点不可用**
- `system/parameter!getParameterValue.action` 返回 AES-128-ECB 密文，密钥 `Tk8IVNJ8B75nHDgb`
- 字典清单约 400 个 `dictCode`，见 `reference/api.md`

完整端点清单、来源前端、只读探测结果见 **`reference/api.md`**。

---

## 注意事项

- **写操作一律不做**。需要提交、审批、删除、改密码时，如实告知不在能力范围内，
  不要尝试绕过 `_guard`。
- `account/user!resetPassword.action`（重置他人密码）是教师常规功能，但**本技能不封装**。
- 会话会过期，报「会话无效」就重新登录，不要试图换参数绕过。
- 单账号、串行、限速 ≥180ms，遇 4xx/429 立即停手。
- 探测未知端点时 `id` 一律用不存在的 `-1`，`limit=1`，**不要遍历真实 id**。
- 入库文档里禁止出现真实姓名，一律写「某学生」。
- `reference/` 体积上限 150 KB：原始 JSON（含姓名、学号、会话）留在本机临时目录，不入库。
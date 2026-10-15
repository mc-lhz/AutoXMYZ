# AutoXMYZ

厦门一中信息校园综合应用系统（`xmyz.xmedu.cn`）**纯只读**查询工具集。

## 三个前端入口

| 入口 | 技术栈 | 角色 |
|---|---|---|
| `manager.html` | ExtJS 3.4，服务端驱动按需加载 | **桌面管理端**，学校门户「登录」按钮指向的正式入口 |
| `m2.html` | Vue 3 + Vant，hash 路由 | 移动端新版，待办审批 + 4 项委托功能 |
| `m.html` | Vue 2 + Vux | 移动端旧版，已被 m2 取代 |

三者共用同一 `JSESSIONID`（`Path=/`，同源），一份会话通吃。

## 枚举结果

合并去重后 **683** 个唯一端点（只读 359 / 写类 324）：

- **桌面端 489** —— 登录后由菜单树按当前账号权限下发，再按每个菜单节点携带的
  `action.jsFile` 定向抓取 **97 个模块**（1.5 MB）得到。
  所以这一列**是当前账号有权访问的**，不是静态猜测。
- **m2.html 185** —— 前端 bundle 静态提取。
- **m.html 7** —— 基本已被 m2 取代。

**端点层几乎不重叠**（三方共有 0 个）：三个前端各写各的 Action 名。
同一个「通知」，桌面端是 `message/message-grid!setRead.action`，
m2 是 `office/notification-detail!delete.action`。

功能层互补而非替代：桌面端独占 `community`(111 社团)、`elective`(96 选课)、
`quality`(30 综评)、`volunteer`(19)；m2 独占 `activiti/*`(72 审批流)、
`archive/*`(23)，**桌面端一个都没有**。桌面端菜单里有 4 项主动跳 m2
（通知公告查看、初高中信息提交、选科）—— 分工是设计好的。

## 用法

```bash
python tools/Access/LoginSession.py password -u <学号> -p <密码>   # 登录
python tools/XMYZClient.py --health                                 # 会话自检
python tools/TestCases/TestApiReadOnly.py                           # 只读 35 项
python tools/TestCases/TestContract.py                              # 契约审计（离线）
```

```python
import sys; sys.path.insert(0, "tools")
from XMYZClient import XMYZClient
c = XMYZClient()
c.status(); c.menuTree(); c.quality(); c.myScores(); c.transcript()
c.growthRecords(); c.myCommunities(); c.myVolunteerActivities(); c.inbox()
```

## 红线

**纯只读。** 写操作由 `Access/HttpTransport.py::_guard` 在发请求前强制拦截，
判定逻辑唯一来源是 `tools/endpoint_kind.py`（已用全量 683 端点校验：
359 只读全放行、324 写端点全拦）。需要提交、审批、删除、改密码时如实说明不在能力范围内。

## 构建中踩到的坑

1. **端点分类不能用正则硬拼** —— 旧实现每分支后接 `\.action$`，
   `approve` 只匹配到 `approvedComplete` 前 7 字母就断，**漏判 88 个写端点**。
2. **默认构造必须自己读会话文件** —— 曾写成 `elif cookie:`，无参构造静默以未登录身份运行；
   而未登录时只读端点照样返回 200，于是「测试全绿」而一条真实数据都没取到。
3. **`loggedIn` 不能判会话** —— 登录后该字段直接消失，`== False` 判永远误报未登录。
4. **响应有两类** —— 除 `{"total":n,"data":[],"success":true}` 信封外，
   还有裸数组/裸对象（`dict!getTree`、`grade!loadTree` 等），只认信封会误报 5 个 FAIL。
5. **`send` 同名两义** —— `attachment!send` 是下载（读），
   `short-message-detail!send` 是真发短信（写），须按 namespace 分流。

完整清单与探测结果见 [`reference/api.md`](reference/api.md)。

## 依赖

`requests`、`rapidocr-onnxruntime`（验证码 OCR）、`numpy` + `Pillow`。

## 红线与隐私

账号信息、凭据、导出文件不入库。`reference/.session.json` 是**占位模板**，
登录后由脚本覆写，提交前请确认内容已脱敏。
入库文档禁止出现真实姓名，一律写「某学生」。

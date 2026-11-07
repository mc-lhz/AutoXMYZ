传输层：会话建立、读写调用、分页 + `XmyzError`。

**`_call` 是唯一出口，读写均放行。** 能力政策 2026-10-24 由仓库所有者修订：
早年的纯只读 `_guard` 已解除；`endpoint_kind.kind()` 保留为文档/统计口径。
实际可写范围由服务端账号权限决定，客户端不越权、不枚举他人数据、
不碰他人密码与审批流。

方法：`get` / `post` / `destroy`（Ext CRUD 契约：`data=<单对象JSON含id>`，全站 !destroy 通用，
growth-record 实测；传数组会报「id不能为空」）/ `paged`（分页 `start`+`limit`）/ `login` / `loadCookie` / `_bindUser`。

⚠️ 两个踩过的坑：

1. `loggedIn` 字段不能用来判会话。未登录时返回 `{"loggedIn":false}`，
   登录后该字段**直接消失**，`get()` 于是返回 `None`——用 `== False` 判会误报未登录，
   用 `== True` 判则永远失败。判据是 profile 里有没有 `loginName` / `id`。

2. `__init__` 默认路径必须自己读会话文件。曾写成 `elif cookie:`，
   于是无参构造（门面最常见的用法）**静默不加载会话**，直接以未登录身份跑完全部方法；
   而未登录时多数只读端点照样返回 200，于是「测试全绿」，实则一条真实数据都没取到。

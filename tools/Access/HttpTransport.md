传输层：会话建立、只读调用、分页 + `XmyzError` / `WriteDenied`。

**`_call` 是唯一出口，能力红线守在这里。** `_guard` 在发请求前拦下所有写语义端点
（`WRITE_DENY_PREFIX`，60 余个动词前缀），命中即抛 `WriteDenied`。
少数名字含动词但语义为读的（`attachment!send`、`!export`、`setRead`）在 `READ_ALLOW` 豁免。

方法：`get` / `post` / `paged`（桌面端分页 `start`+`limit`）/ `login` / `loadCookie` / `_bindUser`。

⚠️ 两个踩过的坑：

1. `loggedIn` 字段不能用来判会话。未登录时返回 `{"loggedIn":false}`，
   登录后该字段**直接消失**，`get()` 于是返回 `None`——用 `== False` 判会误报未登录，
   用 `== True` 判则永远失败。判据是 profile 里有没有 `loginName` / `id`。

2. `__init__` 默认路径必须自己读会话文件。曾写成 `elif cookie:`，
   于是无参构造（门面最常见的用法）**静默不加载会话**，直接以未登录身份跑完全部方法；
   而未登录时多数只读端点照样返回 200，于是「测试全绿」，实则一条真实数据都没取到。

# Calendar — 个人日程（日历网格）

> ⚠️ **create 契约未解**（2026-10-25）：`calendar!create` 是 Ext.ensible
> EventStore 的 create 出口，服务端要 `data=<JSON 事件记录>`，但字段名组合
> （大小写 / 时间格式）四次尝试均静默拒绝（success:false,message:null）。
> 读、destroy（data=单对象含 id）已验证可用。**解锁方式**：浏览器日历页新建
> 一条日程时 F12 → Network 复制该 POST 载荷，一次即可定死格式。
> `gridCreate/gridUpdate/gridDestroy`（列表视图编辑）格式可能不同，同理待抓。

 — 日常办公：个人日程（日历网格）与分类消息查看

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `createCalendar` | `office/calendar!create.action` | POST |
| `destroyCalendar` | `office/calendar!destroy.action` | POST |
| `exportCalendar` | `office/calendar!export.action` | GET |
| `gridCreateCalendar` | `office/calendar!gridCreate.action` | POST |
| `gridDestroyCalendar` | `office/calendar!gridDestroy.action` | POST |
| `gridReadCalendar` | `office/calendar!gridRead.action` | POST |
| `gridUpdateCalendar` | `office/calendar!gridUpdate.action` | POST |
| `importCalendar` | `office/calendar!imp.action` | POST |
| `readCalendar` | `office/calendar!read.action` | GET |
| `updateCalendar` | `office/calendar!update.action` | POST |

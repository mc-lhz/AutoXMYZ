# PsychAppointment — 心理咨询预约：预约、时间下拉、明细

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `createAppointment` | `psychological/appointment!create.action` | POST |
| `createByTeacherAppointment` | `psychological/appointment!createByTeacher.action` | POST |
| `destroyAppointment` | `psychological/appointment!destroy.action` | POST |
| `exportAppointment` | `psychological/appointment!export.action` | GET |
| `importAppointment` | `psychological/appointment!imp.action` | POST |
| `readAppointment` | `psychological/appointment!read.action` | GET |
| `readAppointmentByRequest` | `psychological/appointment!readByRequest.action` | GET |
| `readAppointmentByTeacher` | `psychological/appointment!readByTeacher.action` | GET |
| `updateAppointment` | `psychological/appointment!update.action` | POST |
| `loadAppointmentDetail` | `psychological/appointment-detail!load.action` | GET |
| `saveAppointmentDetail` | `psychological/appointment-detail!save.action` | POST |
| `getComboStoreAppointmentTime` | `psychological/appointment-time!getComboStore.action` | GET |
| `getComboStoreByRequestAppointmentTime` | `psychological/appointment-time!getComboStoreByRequest.action` | GET |

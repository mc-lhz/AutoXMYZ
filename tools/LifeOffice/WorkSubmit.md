# WorkSubmit — 作业查看及提交：内容/附件的保存与提交

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `getComboStoreByMemberCommunity` | `community/community!getComboStoreByMember.action` | GET |
| `getComboStoreLesson` | `community/lesson!getComboStore.action` | GET |
| `loadWorkCardWork` | `community/work!load.action` | GET |
| `saveAttachmentWorkCardWork` | `community/work!saveAttachment.action` | POST |
| `saveContentWorkCardWork` | `community/work!saveContent.action` | POST |
| `saveWorkDetail` | `community/work-detail!save.action` | POST |
| `findWorkByStudentClassWork` | `edu/class-work!findWorkByStudent.action` | GET |
| `saveStudentWorkDetail` | `edu/student-work-detail!save.action` | POST |

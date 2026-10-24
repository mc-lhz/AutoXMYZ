# CategoryMessage — 日常办公：个人日程（日历网格）与分类消息查看

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `getSubCategoryMessageCategory` | `message/category!getSubCategory.action` | GET |
| `findReadByParentMessageGrid` | `message/message-grid!findReadByParent.action` | GET |
| `findReadByStudentMessageGrid` | `message/message-grid!findReadByStudent.action` | GET |
| `readMessageGridByCategory` | `message/message-grid!readByCategory.action` | GET |
| `setReadMessageGrid` | `message/message-grid!setRead.action` | POST |

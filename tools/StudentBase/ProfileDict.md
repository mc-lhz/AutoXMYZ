学生端基础数据：本人档案、字典、学期、班级、网络磁盘。
对应前缀 `account/` `system/` `edu/`。

- 身份：`status` / `profile` / `menuTree` / `readSimpleUser` /
  `readTeacherByParent` / `readStudentAndTeacherByParent` / `readBaseByClassTeacher`
- 字典：`comboStore` / `comboStoreCacheable` / `dictTree` / `schoolTermCombo` /
  `classCombo` / `gradeCombo` / `subjectCombo`
- 结构树：`gradeTree` / `classTreeByClassTeacher` / `parentCombo` / `classStudent` /
  `dormitoryStudent` / `teacherSimple`
- 其他：`weather` / `networkFolders` / `networkFiles`

`menuTree()` 是端点清单的**权威来源**：按当前账号权限下发，节点带 `action.jsFile`。

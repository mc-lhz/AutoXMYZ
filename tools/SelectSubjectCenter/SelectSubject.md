# SelectSubject — 选科（3+1+2）

入口在新版 m2（Vue）移动端，桌面菜单没有该模块。12 个端点全量封装 + 2 个便捷件。

## 方法

| 方法 | 端点 | 写 | 说明 |
|---|---|---|---|
| `getSelectSubjectState()` | `select-subject!getComboStoreByStudentOrParent` | | 状态 + 我的 selectSubjectResult |
| `getSubjectCombo(part1/part2)` | `select-subject!getComboStore` | | 科目下拉（物理/历史类；再选科目） |
| `getCombinationCombo()` | `select-subject!getCombinationComboStore` | | 组合下拉 |
| `getSelectSubjectDetail(id)` | `select-subject-result-detail!loadId` | | 我的明细（科目名/签名/时间） |
| **`mySelectSubject()`** | （便捷组合） | | 状态+明细汇总，含签名 id |
| **`signatureImageUrl(id)`** | （URL 构造） | | 签名图片直链（`attachment!send`） |
| **`selectSubjectReportUrl(id)`** | （URL 构造） | | 确认表 PDF（`report.action`，生成式） |
| `saveSelectSubject(...)` | `select-subject-result-detail!save` | ✓ | 提交选科；签名参数为 **dataURL** |
| `confirmSelectSubject(...)` | `select-subject-result-detail!confirm` | ✓ | 确认（confirm=true 后不可改） |
| `saveSelectSubjectById(id, ...)` | `select-subject-result-detail!saveById` | ✓ | 按 id 修改 |
| `getSelectSubjectResults(**kw)` | `select-subject-result!read` | | ⚠️ 全量列表含他人（2 万+），本人勿用 |
| `getSelectSubjectResultsByClassTeacher` | `...!readByClassTeacher` | | 班主任向 |
| `getNotSelectedList` / `...ByClassTeacher` | `not-select-subject!read[...]` | | 未选科管理向 |

## 实测契约（2026-10-25）

- 表单字段：`subject1Id`（物理类/历史类）、`subject2Id`（选科1）、`subject3Id`（选科2）、
  `studentSignatureData` / `parentSignatureData`（canvas dataURL）
- 签名图片：明细里的 `studentSignatureId` / `parentSignatureId` → `system/attachment!send.action?id=`
- 实践样例：思明2025级高一选科 → 物化生，2026-07-10 确认，双签名在档
# ScoreTrend — 成绩趋势分析与导出

把 `transcript` 全量场次解析成「科目 × 场次 × 分数/段位%」矩阵，输出 xlsx 或控制台表。

## 用法

```python
import sys; sys.path.insert(0, "tools")
from XMYZClient import XMYZClient
from LifeOffice.ScoreTrend import collectTrend, toXlsx, toConsole
c = XMYZClient()
trend = collectTrend(c)                     # 全量场次解析
print("\n".join(toConsole(trend)))          # 控制台摘要（只列真实考试）
toXlsx(trend, "成绩趋势.xlsx")               # 矩阵导出（分数 + 段位% 交替行）
```

## 解析规则（14 场实测归纳）

- 条目形 `<科目>:<值>`，值尾 `_` 剥离；位次三种写法（`段次:70%` / `段次%:19%` / `百分比:56%`）统一折算
- 赋分科目独立成列：化学(赋分) / 生物(赋分)
- 无「分数+百分比」对的场次（报名号/考场/身份证类信息表）判为非考试，`isRealExam` 过滤
- 非成绩条目（姓名外的裸键值）进 `other` 不丢弃

## 注意

- 每场一次 `getTranscriptByStudent` 请求，14 场约 5 秒；批量重跑注意限速
- xlsx 依赖 `openpyxl`

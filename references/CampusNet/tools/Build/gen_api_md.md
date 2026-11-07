建库阶段五：由 endpoints.json + validation.json 生成 `reference/api.md`。

api.md 是本仓库唯一的参考文档：端点清单（按 namespace 分组）、
来源前端、只读实测判定、分页与信封契约、登录契约。

脚本刻意把 360 行的清单压到 63 KB，且不含任何真实姓名/学号。

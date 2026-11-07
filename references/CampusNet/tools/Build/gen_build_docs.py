#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tools/Build/ 的同名 md 说明（AGENTS.md 要求每个 py 都有同名 md）。"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

D = r"C:\Users\Administrator\.config\opencode\skills\AutoXMYZ\tools\Build"

DOCS = {
"login591.py": """建库阶段一：登录。直接复用 591iqAutomatic 的 `Access/LoginToken.py`
（`ocrCaptcha` / `newSession` / `portalLogin`），因为 xmyz.xmedu.cn 与
591iq.cn **是同一个门户**，验证码特征一致（4~5 位、纯小写、一次性）。

产出会话与菜单树，是后续所有步骤的前置。

依赖：`IQ_SKILL` 环境变量指向 591iqAutomatic 目录（默认 `~/.config/opencode/skills/591iqAutomatic`）。
""",

"fetch_modules.py": """建库阶段二：按菜单树抓桌面端模块。

菜单树每个节点带 `action.jsFile`（`|` 分隔的 JS 路径）与 `className`，
桌面端靠 `Ext.ux.ScriptMgr` 动态插入这些脚本 —— 所以**菜单树直接给出了要抓什么**，
不需要猜目录、也不需要扫全站。

实测：97 个文件全部命中，1.5 MB，耗时数秒。
并发 6 + 三次重试 + 已存在则跳过（断点续传）。

产出：`<work>/js/**` 与 `<work>/desktop_endpoints.json`
（489 个端点，含来源 jsFile 与所属菜单名）。
""",

"merge_endpoints.py": """建库阶段三：三方端点合并。

读取 desktop（菜单树 + 97 模块）、m2.html 主 bundle、m.html 主 bundle，
去重合并成一份 `endpoints.json`，每条带 `sources`（来自哪个前端）、
`kind`（读/写，由 `endpoint_kind` 判定）、`menus`（所属菜单）、`files`。

⚠️ 抽取正则必须含连字符：`[A-Za-z0-9_\\-/]+!`。早期漏了 `-`，
`growth-record` 被截成 `record`，端点数从 491 少算成 159。

产出 683 个唯一端点（只读 359 / 写类 324）。
""",

"probe_readonly.py": """建库阶段四：只读端点全量探测。

对 359 个只读端点各发一次 GET + POST，`start=0&limit=1`，
`id` 一律用不存在的 `-1`（保证即使端点语义含删除也只会命中「无此记录」），
限速 180ms。实测 813 秒。

判定口径见 `tools/TestCases/TestApiReadOnly.md`：解析出 JSON 即 ALIVE，
空数组也算（端点通、无数据 ≠ 不可用）。

⚠️ 本脚本**只跑 kind == 'read' 的端点**，写端点一律跳过 ——
判定复用 `endpoint_kind`，与运行时守卫同源。

产出：`<work>/validation.json`
""",

"gen_api_md.py": """建库阶段五：由 endpoints.json + validation.json 生成 `reference/api.md`。

api.md 是本仓库唯一的参考文档：端点清单（按 namespace 分组）、
来源前端、只读实测判定、分页与信封契约、登录契约。

脚本刻意把 360 行的清单压到 63 KB，且不含任何真实姓名/学号。
""",

"gen_docs.py": """工具：为 `tools/` 下每个 .py 生成同名 .md 说明。

AGENTS.md 硬性要求「每个 .py 都有同名 .md」。新增模块后跑一次即可补齐。

注意：本脚本会**覆盖**已有 .md，改完文档别直接跑，先把文案回填进这里的 DOCS 字典。
`XMYZClient.py` 是豁免项（门面），无需生成。
""",

"scan_sensitive.py": """入库前敏感串扫描：找出不可外传的凭据与个人信息。

检测项：会话 id、学号、密码片段、真实姓名、userId、cookie 原文。

⚠️ 检测模式**不写明文真值**，运行时由字符元组 `_PARTS` 拼出 ——
否则这个「防泄漏扫描器」本身就成了泄漏源，真值直接躺在源码里。
（与 `TestContract.no_credential_in_source` 同一个问题的两面）

同样地，扫描时跳过自身，避免自我判定的噪声。

用法：python scan_sensitive.py <目录> [<目录> ...]
""",
}


def main():
    n = 0
    for fn, body in DOCS.items():
        p = os.path.join(D, fn[:-3] + ".md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(body)
        n += 1
        print("  %s" % os.path.basename(p))
    print("生成 %d 个 md" % n)


if __name__ == "__main__":
    main()

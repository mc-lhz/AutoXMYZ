# PackAggregate — 聚合打包（单包 AutoXMYZ.zip）

来源 `git ls-files`（仓库根，cwd 相对），排除 `.git`/`.github`/`dist`/`build_data`/
`__pycache__`/`*.pyc`/验证码/state/导出 xlsx/图片。
产物根目录结构：`SKILL.md`、`AGENTS.md`、`README.md`、`VERSION`、`tools/`、`references/`。

打包后自检必备：三个 `references/<Sub>/SUBSKILL.md` + `tools/Login.py`。

```bash
python -B tools/Release/PackAggregate.py     # → dist/AutoXMYZ.zip
```

"""聚合打包：仓库 → dist/AutoXMYZ.zip（单包，含三子技能与统一登录）。

文件来源 `git ls-files`（cwd 相对），排除产物/缓存/验证码/导出；
产物根目录结构：SKILL.md / AGENTS.md / README.md / VERSION / tools/ / references/。
"""
import fnmatch
import os
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKG_NAME = "AutoXMYZ.zip"

EXCLUDE_PREFIXES = (".git/", ".github/", "dist/", "build_data/")
EXCLUDE_GLOBS = (
    "__pycache__/*", "*.pyc", "*.pyo", "*.state.json", "*.vision.png",
    "jcaptcha*", "vl_*", "591iq_*.json", "*ApiReadOnlyReport.json",
    "*ApiDump.txt", "*.xlsx", "*.jpg", "*.png",
)
MUST_HAVE = ("SKILL.md", "AGENTS.md", "README.md", "VERSION",
             "tools/Login.py", "references/CampusNet/SUBSKILL.md",
             "references/XmyzStudent/SUBSKILL.md", "references/XinYiWo/SUBSKILL.md")


def excluded(rel):
    if rel.startswith(EXCLUDE_PREFIXES):
        return True
    name = os.path.basename(rel)
    return any(fnmatch.fnmatch(rel, g) or fnmatch.fnmatch(name, g)
               for g in EXCLUDE_GLOBS)


def collect():
    r = subprocess.run(["git", "-C", ROOT, "ls-files"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit("[pack] 不在 git 仓库或 git 不可用")
    got = []
    for rel in r.stdout.split("\n"):
        rel = rel.strip().replace("\\", "/")
        if not rel or excluded(rel):
            continue
        p = os.path.join(ROOT, *rel.split("/"))
        if os.path.isfile(p):
            got.append((rel, p))
    return sorted(got)


def main():
    out = os.path.join(ROOT, "dist")
    os.makedirs(out, exist_ok=True)
    dst = os.path.join(out, PKG_NAME)
    files = collect()
    if not files:
        raise SystemExit("[pack] 没有可打包的文件")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, p in files:
            z.write(p, rel)
    with zipfile.ZipFile(dst) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
    miss = [m for m in MUST_HAVE if m not in names]
    if miss:
        raise SystemExit("[pack] 包内缺必备文件: %s" % miss)
    size = os.path.getsize(dst)
    print("[pack] %s ← %d 文件 / %.0f KB" % (dst, len(names), size / 1024.0))
    for m in MUST_HAVE:
        print("   ✓", m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
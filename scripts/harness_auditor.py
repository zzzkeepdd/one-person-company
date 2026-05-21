"""Harness Auditor — 看门大爷，合规闸门。纯 stdlib。"""
import sys
from pathlib import Path

def find_file_named(proj_dir, keyword):
    """项目目录下搜文件名含 keyword 的文件。"""
    for f in proj_dir.rglob("*"):
        if f.is_file() and keyword.lower() in f.name.lower():
            return f
    return None

def file_contains(path, keywords):
    """文件内容是否含任一关键词。"""
    if not path or not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return any(kw.lower() in text for kw in keywords)

def main(proj_root, harness_root):
    proj = Path(proj_root).resolve()
    reports = list(proj.rglob("*"))
    failures = []

    # === 所有项目必查 ===
    cq = find_file_named(proj, "code-qa")
    fq = find_file_named(proj, "func-qa")
    if not cq: failures.append("缺 code-qa 报告")
    if not fq: failures.append("缺 func-qa 报告")

    const = Path(harness_root) / "references/constitution/management-rules.md"
    if not const.is_file():
        failures.append("宪法文件不存在")
    else:
        ct = const.read_text(encoding="utf-8", errors="ignore").lower()
        for kw in ["m01", "c08", "c09"]:
            if kw not in ct:
                failures.append(f"宪法缺 {kw.upper()}")

    comp = find_file_named(proj, "complexity")
    if comp:
        comp_text = comp.read_text(encoding="utf-8", errors="ignore").lower()
    else:
        failures.append("缺复杂度分级结果")
        comp_text = ""

    # === 条件检查 ===
    ui_kw = ["用户可见产品", "网页", "前端", "gui", "移动端"]
    is_ui = any(kw.lower() in comp_text for kw in ui_kw)

    if is_ui:
        browser_kw = ["浏览器实操", "screenshot", "截图", "375px"]
        if fq and not file_contains(fq, browser_kw):
            failures.append("func-qa 报告缺浏览器实操痕迹")
        if "简单" in comp_text:
            failures.append("用户可见产品不能是简单级")
    else:
        print("跳过浏览器检查")

    if failures:
        print(f"不通过 — {len(failures)} 项缺失：")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("通过，可以交付")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Harness Auditor — 看门大爷，合规闸门。纯 stdlib。"""
import sys
import argparse
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

def check_debate_output(harness_root):
    """检查 debate-output.schema.json 和 validate_debate_output.py 存在。"""
    schema = Path(harness_root) / "references/constitution/debate-output.schema.json"
    script = Path(harness_root) / "scripts/validate_debate_output.py"
    return schema.is_file() and script.is_file()

def check_vague_words(harness_root):
    """检查 vague-words.txt 和 check_testability.py 存在。"""
    words = Path(harness_root) / "references/constitution/vague-words.txt"
    script = Path(harness_root) / "scripts/check_testability.py"
    return words.is_file() and script.is_file()

def check_manifest_validation(harness_root):
    """检查 execution-manifest.schema.json 和 validate_execution_manifest.py 存在。"""
    schema = Path(harness_root) / "references/constitution/execution-manifest.schema.json"
    script = Path(harness_root) / "scripts/validate_execution_manifest.py"
    return schema.is_file() and script.is_file()

def main():
    parser = argparse.ArgumentParser(description="Harness Auditor v3.0")
    parser.add_argument("--pipeline", choices=["l1", "l2", "l3"], required=True,
                        help="管道级别: l1/l2/l3")
    parser.add_argument("proj_root", help="项目根目录")
    parser.add_argument("harness_root", help="Harness根目录")
    args = parser.parse_args()

    proj = Path(args.proj_root).resolve()
    harness = Path(args.harness_root).resolve()
    pipeline = args.pipeline
    failures = []

    # === 所有管道必查 ===
    cq = find_file_named(proj, "code-qa")
    fq = find_file_named(proj, "func-qa")
    if not cq: failures.append("缺 code-qa 报告")
    if not fq: failures.append("缺 func-qa 报告")

    # L1: code-qa 和 func-qa 必须独立（不同文件）
    if pipeline == "l1":
        if cq and fq and cq.resolve() == fq.resolve():
            failures.append("L1 要求 code-qa 和 func-qa 为独立文件，不能合并")
        if not check_manifest_validation(harness):
            failures.append("L1 缺执行清单验证基础结构")

    # L2: 缩减版 QA 可接受（只检查存在），但必须独立
    if pipeline == "l2":
        if cq and fq and cq.resolve() == fq.resolve():
            failures.append("L2 要求 code-qa 和 func-qa 为独立文件，不能合并")

    # L3: 完整版 QA
    if pipeline == "l3":
        if cq and fq and cq.resolve() == fq.resolve():
            failures.append("L3 要求 code-qa 和 func-qa 为独立文件，不能合并")

    # === v3.0 新增：节点门基础结构检查 ===
    if not check_debate_output(harness):
        failures.append("缺辩论输出 schema 或验证脚本（debate-output.schema.json + validate_debate_output.py）")
    if not check_vague_words(harness):
        failures.append("缺模糊词黑名单或可测性检查脚本（vague-words.txt + check_testability.py）")

    # === 宪法检查 ===
    const = harness / "references/constitution/management-rules.md"
    if not const.is_file():
        failures.append("宪法文件不存在")
    else:
        ct = const.read_text(encoding="utf-8", errors="ignore").lower()
        for kw in ["m01", "c08", "c09"]:
            if kw not in ct:
                failures.append(f"宪法缺 {kw.upper()}")
        # v3.0: 原子组列检查
        if "原子组" not in ct and "atomic" not in ct:
            failures.append("宪法缺原子组列（v3.0 必需）")

    # === 复杂度分级检查 ===
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
        print(f"通过 [{pipeline.upper()} 管道]，可以交付")

if __name__ == "__main__":
    main()

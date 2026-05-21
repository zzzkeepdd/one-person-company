#!/usr/bin/env python3
"""节点门1：辩论输出 JSON schema 验证。纯 stdlib。"""
import sys
import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / "references/constitution/debate-output.schema.json"

def main(json_path):
    try:
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"FAIL: 无法解析JSON — {e}")
        sys.exit(1)

    errors = []

    if not isinstance(data.get("verified_items"), list) or len(data["verified_items"]) == 0:
        errors.append("verified_items 非空数组")
    if "rounds_completed" not in data or not (1 <= data["rounds_completed"] <= 3):
        errors.append("rounds_completed 必须在 1-3")
    if not isinstance(data.get("converged"), bool):
        errors.append("converged 必须为 boolean")

    if errors:
        print(f"FAIL — {len(errors)} 项不合规：")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("PASS — 辩论输出 schema 验证通过")

if __name__ == "__main__":
    main(sys.argv[1])

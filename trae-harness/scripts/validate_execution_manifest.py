#!/usr/bin/env python3
"""节点门3：执行清单完整性自检。纯 stdlib。"""
import sys
import json
import hashlib
from pathlib import Path

def main(manifest_path):
    mf = Path(manifest_path)
    if not mf.is_file():
        print(f"FAIL: 清单文件不存在 — {manifest_path}")
        sys.exit(1)

    try:
        data = json.loads(mf.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: JSON解析失败 — {e}")
        sys.exit(1)

    errors = []

    tasks = data.get("tasks", [])
    if not tasks:
        errors.append("tasks 为空，至少需要1个任务")

    for i, t in enumerate(tasks):
        for field in ["id", "描述", "验收标准ID", "文件范围", "任务类型"]:
            if field not in t or not t[field]:
                errors.append(f"任务[{i}] 缺字段: {field}")
        if isinstance(t.get("任务类型"), str) and t["任务类型"] not in ("new", "modify", "delete"):
            errors.append(f"任务[{i}] 无效任务类型: {t['任务类型']}")

    # spec_checksum 验证
    spec_path = data.get("full_spec_path", "")
    checksum = data.get("spec_checksum", "")
    if spec_path and checksum:
        spec_file = mf.parent / spec_path
        if not spec_file.is_file():
            errors.append(f"full_spec_path 指向的文件不存在: {spec_path}")
        else:
            actual = hashlib.sha256(spec_file.read_bytes()).hexdigest()
            if actual != checksum:
                errors.append(f"spec_checksum 不匹配: 期望={checksum[:16]}..., 实际={actual[:16]}...")
    else:
        errors.append("缺 full_spec_path 或 spec_checksum")

    if errors:
        print(f"FAIL — {len(errors)} 项不合规：")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("PASS — 执行清单完整性自检通过")

if __name__ == "__main__":
    main(sys.argv[1])

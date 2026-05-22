#!/usr/bin/env python3
"""节点门1：辩论输出 JSON schema + 维度覆盖 + 攻击点硬计数验证。纯 stdlib。v3.1"""
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

    # --- 基础 schema 验证 ---
    if not isinstance(data.get("verified_items"), list) or len(data["verified_items"]) == 0:
        errors.append("verified_items 非空数组")
    if "rounds_completed" not in data or not (1 <= data["rounds_completed"] <= 3):
        errors.append("rounds_completed 必须在 1-3")
    if not isinstance(data.get("converged"), bool):
        errors.append("converged 必须为 boolean")

    # --- v3.1: 攻击点硬计数 ---
    attacks = data.get("attacks", [])
    if isinstance(attacks, list) and len(attacks) > 0:
        total_attacks = len(attacks)
    else:
        # 降级：无 attacks 字段时从 must_fix + rejected_challenges 推算
        total_attacks = 0
        if isinstance(data.get("must_fix"), list):
            total_attacks += len(data["must_fix"])
        if isinstance(data.get("rejected_challenges"), list):
            total_attacks += len(data["rejected_challenges"])

    # --- v3.1: 攻击点评分验证 ---
    if isinstance(attacks, list):
        high_score_count = sum(1 for a in attacks if isinstance(a, dict) and a.get("score", 0) >= 3)
        low_score_count = sum(1 for a in attacks if isinstance(a, dict) and a.get("score", 0) <= 0)
        if low_score_count > 0:
            errors.append(f"攻击点评分含 ≤0 分项 ({low_score_count} 条)，需重新评分")
    else:
        # 无 attacks 字段时从 must_fix 推断: 至少要有攻击点
        high_score_count = 0  # 不可验证，跳过

    # --- v3.1: 维度覆盖率 ---
    if "dimensions_covered" in data and isinstance(data["dimensions_covered"], list):
        covered_dims = [d for d in data["dimensions_covered"]
                        if isinstance(d, dict) and d.get("status") == "covered"]
        dim_total = len(data["dimensions_covered"])
        dim_covered = len(covered_dims)

        if dim_total == 0:
            errors.append("dimensions_covered 为空，无可验证维度")
        elif dim_covered < dim_total:
            uncovered = [d.get("name", "?") for d in data["dimensions_covered"]
                         if isinstance(d, dict) and d.get("status") != "covered"]
            errors.append(f"维度覆盖率 {dim_covered}/{dim_total}，未覆盖: {uncovered}")

        # 攻击点硬计数: ≥ 维度数 × 2
        min_attacks = dim_total * 2
        if total_attacks < min_attacks:
            errors.append(f"攻击点不足: {total_attacks} < {min_attacks}（维度数{dim_total}×2）")

        # 高评分攻击点至少 1 条
        if attacks and high_score_count < 1:
            errors.append("缺少直击核心的攻击点（score ≥ 3 的至少 1 条）")

    if errors:
        print(f"FAIL — {len(errors)} 项不合规：")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        dim_info = ""
        if "dimensions_covered" in data:
            dim_info = f"，维度覆盖 {dim_covered}/{dim_total}"
        attack_info = f"，攻击点 {total_attacks}"
        print(f"PASS — 辩论输出验证通过{attack_info}{dim_info}")


if __name__ == "__main__":
    main(sys.argv[1])

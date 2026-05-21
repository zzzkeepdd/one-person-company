#!/usr/bin/env python3
"""节点门2：验收标准可测性检查。grep 模糊词黑名单。纯 stdlib。"""
import sys
from pathlib import Path

BLACKLIST = Path(__file__).parent.parent / "references/constitution/vague-words.txt"

def main(spec_path):
    spec = Path(spec_path)
    if not spec.is_file():
        print(f"FAIL: 文件不存在 — {spec_path}")
        sys.exit(1)

    bad_words = set(
        line.strip() for line in BLACKLIST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    )

    text = spec.read_text(encoding="utf-8", errors="ignore")
    hits = [(w, text.lower().count(w.lower())) for w in bad_words if w.lower() in text.lower()]

    if hits:
        print(f"FAIL — 发现模糊词：")
        for word, count in hits:
            print(f"  - \"{word}\" (出现{count}次)")
        sys.exit(1)
    else:
        print("PASS — 验收标准无可测性模糊词")

if __name__ == "__main__":
    main(sys.argv[1])

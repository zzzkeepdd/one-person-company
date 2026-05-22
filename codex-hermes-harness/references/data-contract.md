# JSON 接口数据契约 v2.0

Codex+Hermes Harness v4.0 适用。

## 契约表

| 接口 | 生产者 | 消费者 | 方向 |
|------|--------|--------|------|
| clarify 输出 | Hermes | Codex | Hermes → Codex |
| context 输出 | Hermes | Codex | Hermes → Codex |
| gate 输出 | Hermes | Codex | Hermes → Codex |
| retrospect 输出 | Hermes | Codex | Hermes → Codex |
| 执行清单 JSON | Codex | Codex (自身) | Codex 内部 |

## clarify 输出 Schema

```json
{
  "dimension": "string",
  "boundary": {
    "do": "一句话定义该维度要做什么",
    "dont": "一句话定义该维度不做什么"
  },
  "testable_attacks": [
    {
      "point": "攻击点描述",
      "suggested_test": "如何用测试验证此攻击点"
    }
  ],
  "preventive_attacks": [
    {
      "point": "攻击点描述",
      "check_item": "代码审查时的检查项"
    }
  ],
  "verdict": [
    {
      "attack": "攻击点引用",
      "ruling": "must_handle|can_defer|ignore",
      "reasoning": "一句话"
    }
  ],
  "priority": "high|medium|low"
}
```
总输出 ≤400 token。

## context 输出 Schema

```json
{
  "related_memories": ["≤3条，每条一句话"],
  "pitfalls": [
    {"scenario": "场景", "consequence": "后果"}
  ],
  "relevant_rules": ["≤3条宪法约束，每条一行"]
}
```
总输出 ≤300 token。

## gate 输入/输出 Schema

输入：
```json
{
  "phase_id": "G1|G2|G3|G4-1|G4-2|G5|G6|G7",
  "payload": { /* phase 特定数据 */ }
}
```

输出：
```json
{
  "pass": true|false,
  "reason": "失败原因（不含修复建议）"
}
```

## retrospect 输入/输出 Schema

输入：
```json
{
  "manifest_json": { /* 执行清单 */ },
  "acceptance_report": { /* 验收报告 */ }
}
```

输出（≤300 token）：
```json
{
  "deviations": ["产出的偏差"],
  "violations": ["触发的宪法条目"],
  "lessons": ["新教训，≤3条"]
}
```
副作用：memory.write、skill.update、gate_rules.update。

## 演进规则

- 字段废弃：标记 deprecated，保留 2 版本后移除
- 枚举值扩展：下游接受未知值，按默认路径处理
- Breaking change：开新版本号，旧版本平行运行 30 天

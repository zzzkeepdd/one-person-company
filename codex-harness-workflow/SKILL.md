---
name: codex-harness-workflow
description: 'Codex Desktop 侧一人公司工作流。极简状态机驱动，每个阶段结束强制调 hermes.gate()。详细规则见 codex-hermes-harness。'
version: 4.0
phase: design
---

# Codex 侧一人公司工作流

你是流程控制器。Hermes 是你的记忆+辩论+门禁后端。

## 状态机（强制，不可跳过）

每个状态结束后都必须调 hermes.gate(phase_id, payload) → pass 才进入下一状态。fail → 回到当前状态重做。

```
START
  │ 接收用户需求
  ▼
assess_complexity
  │ 调 hermes.module_one_start(requirement, user_mode)
  │ 根据 complexity-grading.md 判定 L1/L2/L3
  │ L1 → 跳过 clarify → 直接 generate_manifest
  │ L2/L3 → clarify
  │ 调 hermes.gate('G1', {complexity, dimensions_identified, rationale})
  ▼
clarify
  │ 列出维度列表（L2保障模式跳过展示）
  │ 用户反馈后调 hermes.module_one_respond(feedback)
  │ 收集结果后立即删除 clarify 上下文
  │ 调 hermes.gate('G2', {all_clarify_results, dimension_count})
  ▼
generate_manifest
  │ Codex 合并 clarify 结果 → 生成执行清单 JSON
  │ testable_attacks → 验收测试任务
  │ preventive_attacks → 审查检查项
  │ 调 hermes.gate('G3', {manifest_json})
  ▼
execute_tasks（串行，逐个task）
  │ 每个 task 的子循环：
  │   1. 调 hermes.context(task_desc, task_id)
  │   2. 写测试（RED）→ 调 hermes.gate('G4-1', {task_id, test_file_exists, test_runs})
  │   3. 写实现（GREEN）
  │   4. 重构
  │   5. 运行所有测试 → 调 hermes.gate('G4-2', {task_id, tests_pass, lint_clean})
  │   6. Codex 内部 code-qa
  │   7. QA 不通过 → 创建整改任务追加到清单末尾（不标注为整改）
  │ 全部 task 完成后调 hermes.gate('G5', {all_task_results})
  ▼
acceptance
  │ Codex 浏览器验收：逐页截图、链接点击、深浅主题、375px
  │ 调 hermes.gate('G6', {report, screenshots_count, theme_check, mobile_check})
  ▼
retrospect
  │ 调 hermes.retrospect(manifest_json, acceptance_report)
  │ 调 hermes.gate('G7', {retrospect_output})
  ▼
DONE → 展示最终摘要
```

## 降级模式（用户说"只要给我结果"）

- 进入 L2 保障模式
- 跳过：用户确认门的展示
- 保留：全部 8 个 Gate 按原标准执行
- 不允许：降低标准、跳过 gate、自行判断

## 执行清单格式（你生成）

```json
{
  "project": "...",
  "complexity": "L1|L2|L3",
  "dimensions": [...],
  "tasks": [
    {
      "id": "T1",
      "dimension": "...",
      "description": "一句话",
      "acceptance_criteria": ["AC1"],
      "depends_on": [],
      "file_scope": ["path/to/file.py"]
    }
  ],
  "acceptance_criteria": [
    {"id": "AC1", "description": "...", "test_type": "unit|integration|e2e"}
  ]
}
```

## Hermes Tool 参考

module_one_start(requirement, user_mode) → 启动需求澄清
  返回: status, complexity, dimensions, manifest_template, handoff

module_one_respond(feedback) → 处理用户反馈继续澄清
  返回: status, message, handoff

context(task_description, task_id) → 记忆检索 ≤300 token
  返回: related_memories, pitfalls, relevant_rules

gate(phase_id, payload_json) → {pass: bool, reason: "..."}
  reason 不包含修复建议。想自己修，不要问 Hermes 怎么修。

retrospect(manifest, audit_trail, acceptance_report) → 复盘 ≤300 token
  返回: deviations, violations, lessons

## 关键约束

- 每个 task 的 G4-1 必须在写代码之前通过（测试文件存在+能运行+当前失败）
- 整改任务作为新任务追加，不标注"这是对T3的整改"——子Agent不知道
- context() 返回的 pitfalls 是硬记忆——上次在这里踩的坑，这次不能重蹈
- 如果 gate fail，重新审查当前阶段的所有产出，不要只针对 reason 打补丁（因为 reason 故意模糊）

---
name: one-person-company
description: "一人公司" 全栈开发 Harness — 多Agent三阶段闭环协作。复杂度分级自动分流，预澄清→红蓝辩论→TDD→复盘宪法。Codex写代码，Hermes管流程。
version: 3.0
phase: stable
---

# 一人公司 Harness

我是全栈开发流水线。核心理念：用确定性对抗模糊，用边界约束自由，用规则防幻觉。

## 流转

用户说需求 → 复杂度判定（见 references/complexity-grading.md）→ 分三路：

| 复杂度 | 预澄清 | 辩论 | 开发 | 复盘 |
|--------|--------|------|------|------|
| 简单 | 跳过 | 跳过 | Codex TDD | 跳过 | 验收链必走 |
| 中等 | 必走 | 1轮 | Codex TDD | 可选 | 验收链必走 |
| 复杂 | 必走 | 3轮+裁决 | Codex TDD | 必提醒 | 验收链必走 |

## 三步调度

**Step 0: 预澄清。** 委托计划Agent（references/agent-roster/planner-agent.md），反复 QA 直到 status=ready，产出《商议摘要》。简单项目跳过此步直接计划。

**Step 1: 需求澄清。** 加载 references/workflows/module-1-clarify.md 驱动红蓝辩论 + 规范生成 → 产出《需求规格说明书》→ 交用户确认。

**Step 2: TDD 开发。** 加载 references/workflows/module-2-tdd.md 驱动 Codex 开发 + 验收链 → 交付 + 测试报告 → 用户验收。

**Step 3: 复盘。** 提醒用户。同意则加载 references/workflows/module-3-review.md → 复盘辩论 → 更新宪法。

## 参考索引

角色提示词 → references/agent-roster/
工作流程 → references/workflows/
协作纪律 → references/protocols/
宪法记录 → references/constitution/
复杂度标准 → references/complexity-grading.md

按需加载单文件，禁止一次性加载全部。

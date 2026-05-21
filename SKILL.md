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

| 管道 | 复杂度 | 预澄清 | 辩论 | 开发 | QA | 复盘 |
|------|--------|--------|------|------|----|------|
| L1 | 简单 | 1轮 | 跳过 | Hermes直接写 | code-qa+func-qa独立 | 跳过 |
| L2 | 中等 | 必走 | 1轮（裁判可扩至2轮） | Codex TDD | code-qa+func-qa独立（缩减版） | 可选 |
| L3 | 复杂 | 必走 | 2轮+裁决 | Codex TDD | code-qa+func-qa独立（完整版） | 必提醒 |

- 验收链（code-qa + func-qa）所有管道不可跳过、不可合并
- L1 QA 失败 ≥2 次自动降级 L2

## JSON 接口（跨模块强制）

| 接口 | Schema | 流向 | 定位 |
|------|--------|------|------|
| 辩论输出 | debate-output.schema.json | 裁判→裁决→规范 | 节点门1验证 |
| 执行清单 | execution-manifest.schema.json | 模块一→模块二 | 节点门3验证 |

信息瓶颈：模块二启动只收执行清单 JSON（~200 token），不注入原始需求/辩论历史。按需通过 full_spec_path 回查规范。

## 节点门

| 节点 | 脚本 | 触发时机 |
|------|------|----------|
| 辩论结束 | validate_debate_output.py | 模块一产出辩论JSON后 |
| 规范完成 | check_testability.py | 规范生成后 |
| 模块二启动 | validate_execution_manifest.py | 执行清单注入前 |
| 验收结束 | harness_auditor.py --pipeline | 验收链完成后 |

## 三步调度

**Step 0: 预澄清。** 委托计划Agent（references/agent-roster/planner-agent.md），反复 QA 直到 status=ready，产出《商议摘要》。L1 项目 1 轮后直接进入开发。

**Step 1: 需求澄清。** 加载 references/workflows/module-1-clarify.md 驱动红蓝辩论 + 规范生成 → 产 JSON 辩论输出 + 《需求规格说明书》→ 节点门1+2 → 交用户确认。

**Step 2: TDD 开发。** 加载 references/workflows/module-2-tdd.md → 节点门3 → 按管道分发 → 验收链 → 审计闸门 → 交付。

**Step 3: 复盘。** 提醒用户。同意则加载 references/workflows/module-3-review.md → 复盘辩论 → 自动生成宪法草案至 proposals.md。

## 宪法半自动

复盘辩论后 → 裁决Agent 自动生成宪法条款草案 → 写入 constitution/proposals.md。用户确认后合并至 management-rules.md。超 25 条自动提醒瘦身。

## 参考索引

角色提示词 → references/agent-roster/
工作流程 → references/workflows/
协作纪律 → references/protocols/
宪法记录 → references/constitution/
复杂度标准 → references/complexity-grading.md
JSON 契约 → references/constitution/data-contract.md

按需加载单文件，禁止一次性加载全部。

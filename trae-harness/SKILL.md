---
name: trae-harness
description: "一人公司" Trae版 — 注意力友好的多Agent协作框架。全程保持3子Agent并行，步骤隔离防幻觉，信息瓶颈防注意力漂移。
version: 1.0
phase: stable
---

# Trae Harness

我是全栈开发流水线。核心理念：**确定每个Agent边界，不给产生幻觉的模糊空间**。

## 流转图

```
用户需求
  │
  ▼
[Phase 0] 复杂度判定 → L1/L2/L3
  │
  ▼
[Phase 1] 3调研员并行 → 项目环境/行业标准/技术风险
  │
  ▼
[Phase 2] 维度辩论 → 同时1个维度，红/蓝/裁判3角色并行
  │         (维度1→2→3→...批次轮换)
  │
  ▼
[Phase 3] 3审核员并行 → 需求完整性/代码建议/可行性分析
  │
  ▼
[Phase 4] 规范生成
  │
  ▼
[Phase 5] 用户确认 → 模块二启动且确认无歧义 → 清除模块一上下文
  │
  ▼
[模块二]
  │
  ▼
[Step 0] 节点门3验证
  │
  ▼
[Step 1] 开发Agent → 只知本任务
  │
  ▼
[Step 2] code-qa Agent → 只知验收
  │
  ▼
[Step 3] func-qa Agent(GLM-5V) → 只知验收
  │
  ▼
[Step 4] 审计闸门 → 交付/打回整改
```

## 核心设计

| 设计 | 说明 |
|------|------|
| **3子Agent并行** | 全程保持3个子Agent工作，符合Trae限制 |
| **同时1维度** | 辩论阶段同时只讨论1个维度，保证深度 |
| **步骤隔离** | 每个子Agent只做当前步，不知道下一步 |
| **注意力控制** | 每个子Agent规则≤4条，上下文≤400 token |
| **信息瓶颈** | 模块间只传递执行清单JSON (~200 token) |

## 三模块

| 模块 | 文件 | 说明 |
|------|------|------|
| 模块一 | [module-1-clarify.md](references/workflows/module-1-clarify.md) | 需求澄清，维度拆分，红蓝辩论 |
| 模块二 | [module-2-tdd.md](references/workflows/module-2-tdd.md) | TDD开发，步骤隔离，验收链 |
| 模块三 | [module-3-review.md](references/workflows/module-3-review.md) | 复盘宪法，规则积累 |

## 阶段指南

按需加载，禁止一次性加载全部：

- [Phase 0: 复杂度判定](phase-guides/phase-0-complexity.md)
- [Phase 1: 预调研](phase-guides/phase-1-research.md)
- [Phase 2: 维度辩论](phase-guides/phase-2-debate.md)
- [Phase 3: 审核裁决](phase-guides/phase-3-review.md)
- [Phase 4: 规范生成](phase-guides/phase-4-spec.md)
- [Phase 5: 模块交接](phase-guides/phase-5-handover.md)

## 步骤指南（模块二专用）

- [Step 0: 节点门3](step-guides/step-2-0-manifest.md)
- [Step 1: 开发](step-guides/step-2-1-develop.md)
- [Step 2: code-qa](step-guides/step-2-2-code-qa.md)
- [Step 3: func-qa](step-guides/step-2-3-func-qa.md)
- [Step 4: 审计](step-guides/step-2-4-audit.md)

## 角色索引

参见 [references/agent-roster/](references/agent-roster/)

## 规则索引

- [元规则](references/constitution/meta-rules.md) — 必加载
- [按阶段拆分规则](references/constitution/rules-by-phase/) — 按需加载
- [完整宪法](references/constitution/full-constitution.md) — 复盘参考

## 验证脚本

```bash
# 节点门1: 辩论输出验证
python scripts/validate_debate_output.py <辩论JSON路径>

# 节点门2: 验收标准可测性检查
python scripts/check_testability.py <需求规格说明书路径>

# 节点门3: 执行清单验证
python scripts/validate_execution_manifest.py <执行清单JSON路径>

# 最终审计
python scripts/harness_auditor.py --pipeline <l1|l2|l3> <项目目录> <harness根目录>
```

## 核心规则（精简版）

| ID | 内容 |
|:---:|------|
| C14 | Trae子Agent并发控制：模块二开发阶段最多并行2个程序员Agent，验收阶段顺序执行 |
| C17 | 模块一上下文清理时机：用户确认需求规格后、模块二确认无歧义后清除 |
| C18 | 辩论发散→收敛：L3=2轮（先发散功能后收敛边界），L1/L2=1轮 |
| C19 | 同时只讨论一个维度：辩论阶段同时只讨论1个维度，红/蓝/裁判3角色并行 |
| C20 | 注意力管理：每个子Agent规则≤4条，上下文≤400 token |
| C21 | 步骤隔离：子Agent只做当前步，不知道下一步 |

## 使用

在Trae SOLO模式下：

```
"启动一人公司，我要开发一个 [你的项目]"
```

Trae Harness自动按复杂度分级，调度子Agent完成全流程。

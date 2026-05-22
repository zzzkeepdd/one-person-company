# Trae Harness

> "一人公司" Trae版 — 注意力友好的多Agent协作框架

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

## 核心理念

**确定每个Agent边界，不给产生幻觉的模糊空间。**

通过以下设计实现：
- **步骤隔离**：每个子Agent只做当前步，不知道下一步
- **注意力控制**：每个子Agent规则≤4条，上下文≤400 token
- **信息瓶颈**：模块间只传递执行清单JSON (~200 token)
- **全程3子Agent**：符合Trae并发限制，保持效率

## 与原版Harness的区别

| 维度 | 原版Harness (Hermes+Codex) | Trae Harness |
|------|---------------------------|--------------|
| **平台** | Hermes(规划) + Codex(执行) | Trae SOLO Agent单平台 |
| **子Agent机制** | delegate_task跨平台 | Trae自定义Agent调用 |
| **并发控制** | 无明确限制 | 全程保持3子Agent并行 |
| **辩论方式** | 多维度并行辩论 | 同时只讨论1个维度，红/蓝/裁判3角色并行 |
| **注意力管理** | 信息瓶颈~200 token | 规则拆分+步骤隔离+上下文控制 |
| **视觉验收** | Codex浏览器自动化 | GLM-5V视觉模型分析截图 |

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     SOLO Agent（主Agent，常驻）                │
│                    不负责执行，只负责调度和聚合                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │子Agent A│          │子Agent B│          │子Agent C│
   │(并行)   │          │(并行)   │          │(并行)   │
   └─────────┘          └─────────┘          └─────────┘

模块一：需求澄清
├── Phase 0: 复杂度判定（主Agent）
├── Phase 1: 3调研员并行（项目环境/行业标准/技术风险）
├── Phase 2: 维度辩论（同时1维度，红/蓝/裁判3角色并行）
├── Phase 3: 3审核员并行（完整性/代码建议/交叉验证）
├── Phase 4: 规范生成
└── Phase 5: 用户确认 → 清除上下文 → 进入模块二

模块二：TDD开发
├── Step 0: 节点门3验证
├── Step 1: 开发Agent（只知本任务）
├── Step 2: code-qa Agent（只知验收）
├── Step 3: func-qa Agent（GLM-5V，只知验收）
└── Step 4: 审计闸门 → 交付/整改

模块三：复盘宪法（主Agent内化）
```

## 快速开始

### 1. 安装Trae
下载并安装 [Trae IDE](https://www.trae.ai/)

### 2. 配置Trae Harness
将本仓库复制到Trae的skills目录：
```bash
cp -r trae-harness ~/.trae/skills/
```

### 3. 启动开发
在Trae SOLO模式下输入：
```
"启动一人公司，我要开发一个 [你的项目描述]"
```

Trae Harness会自动：
1. 判定复杂度（L1/L2/L3）
2. 拆分维度并并行调研
3. 红蓝辩论（同时1维度，3角色并行）
4. 审核裁决（3审核员并行，含代码建议）
5. 生成规范并用户确认
6. TDD开发（步骤隔离，GLM-5V视觉验收）
7. 复盘宪法（可选）

## 核心设计

### 1. 全程3子Agent并行
- 符合Trae试用版3并发限制
- 每个阶段保持3个子Agent满载工作
- 维度>3时采用批次轮换

### 2. 同时只讨论1个维度
- 保证辩论深度，避免注意力分散
- 红队、蓝队、裁判3角色物理隔离，确保公正
- L1/L2=1轮（收敛边界），L3=2轮（发散→收敛）

### 3. 步骤隔离
- 每个子Agent只做当前步骤
- 不知道下一步是什么
- 整改后的任务作为新任务派发，子Agent不知道是整改

### 4. 注意力控制
- 规则按阶段拆分，每个子Agent只加载≤4条
- 上下文≤400 token
- 模块间信息瓶颈：执行清单JSON ~200 token

### 5. GLM-5V视觉验收
- UI产品必须使用GLM-5V视觉模型验收
- 截图→视觉分析→产出报告

## 目录结构

```
trae-harness/
├── SKILL.md                    # 入口文件
├── README.md                   # 本文件
├── phase-guides/               # 阶段指南（6份，极简）
│   ├── phase-0-complexity.md
│   ├── phase-1-research.md
│   ├── phase-2-debate.md
│   ├── phase-3-review.md
│   ├── phase-4-spec.md
│   └── phase-5-handover.md
├── step-guides/                # 步骤指南（模块二专用，5份）
│   ├── step-2-0-manifest.md
│   ├── step-2-1-develop.md
│   ├── step-2-2-code-qa.md
│   ├── step-2-3-func-qa.md
│   └── step-2-4-audit.md
├── references/
│   ├── agent-roster/           # Agent角色卡
│   │   ├── trae-coordinator.md
│   │   ├── researcher.md
│   │   ├── debater.md
│   │   ├── reviewer.md
│   │   ├── spec-generator.md
│   │   ├── developer.md
│   │   ├── code-qa.md
│   │   └── func-qa.md
│   ├── constitution/
│   │   ├── meta-rules.md       # 元规则（1条，必加载）
│   │   ├── rules-by-phase/     # 按阶段拆分规则
│   │   └── full-constitution.md # 完整宪法（复盘参考）
│   └── workflows/              # 三模块流程
│       ├── module-1-clarify.md
│       ├── module-2-tdd.md
│       └── module-3-review.md
└── scripts/                    # 验证脚本
    ├── validate_debate_output.py
    ├── check_testability.py
    ├── validate_execution_manifest.py
    └── harness_auditor.py
```

## 规则体系

### 元规则（所有子Agent必加载）
| ID | 内容 |
|:---:|------|
| M01 | 任何流程指令必须附带产出物和验证机制，否则视为软建议。 |

### 核心规则（按阶段拆分加载）
| ID | 内容 | 适用阶段 |
|:---:|------|---------|
| C08 | 同时只讨论一个维度 | Phase 2 |
| C10 | 裁判评分1-5分，至少1个≥3分 | Phase 2 |
| C13 | 审核员必须给出代码可行性建议 | Phase 3 |
| C17 | 信息瓶颈：执行清单≤200 token | Phase 4 |
| C20 | 上下文清理时机：模块二确认无歧义后 | Phase 5 |
| C22 | 步骤隔离：子Agent只做当前步 | 模块二 |

完整规则参见 [references/constitution/full-constitution.md](references/constitution/full-constitution.md)

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

## 适用场景

| 场景 | 推荐管道 | 说明 |
|------|---------|------|
| 简单脚本/工具 | L1 | ≤3文件，单一技术栈 |
| Web应用/API | L2 | 中等复杂度，完整流程 |
| 复杂系统/多模块 | L3 | 完整流程+强制复盘 |

## 注意事项

1. **不要一次性加载全部规则**：按需加载当前阶段规则
2. **不要提前清理上下文**：模块二确认无歧义后才清理模块一
3. **不要跳过节点门**：每个节点门必须通过才能继续
4. **不要让子Agent知道下一步**：保持步骤隔离

## 贡献

欢迎提交Issue和PR，共同完善Trae Harness。

## 许可

MIT License

---

**核心理念**：用确定性对抗模糊，用边界约束自由，用规则防幻觉。

# 一人公司 Harness v4.0 (One-Person Company)

> Codex Desktop + Hermes MCP. Codex does the work and collects evidence. Hermes holds the memory and passes judgment.
> Codex 负责做事和采证。Hermes 负责记忆和裁决。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## v4.0 Highlights / 亮点

| Feature | What |
|---------|------|
| **Codex Desktop 入口** | 用户在 Codex IDE 里说需求，Codex 路由到 Hermes 做模块一和三，自己执行模块二 |
| **Hermes MCP Server** | 5 个 MCP tool：`module_one_start` `module_one_respond` `context` `gate` `retrospect`。stdio 启动，毫秒级响应 |
| **8 个 Gate 硬闸门** | G1-G7 由 Hermes 裁决，Codex 必须调用才能进入下一阶段。不调 gate = 不能继续 |
| **信息瓶颈** | Hermes → Codex 每次传输 ≤400 token。Codex 不知道辩论过程，Hermes 不知道代码细节 |
| **盲区对抗** | Codex 和 Hermes 是两套独立系统——天然盲区，红蓝辩论不再同一模型自说自话 |
| **降级不降 Gate** | 用户说"只要结果"只跳过确认门，8 个 Gate 按原标准执行 |
| **复盘闭环** | 模块二产出完整 audit_trail → Hermes 偏差分析 + 教训写入长记忆 + 返回 lesson_summary |

---

## Experiment Data / 实验数据

> 实验平台：Trae + deepseek-v4-pro。方法论相同，结论适用于 Codex + Hermes。

| 版本 | 名称 | A 组通过率 | B 组通过率 | 质量差值 |
|:---:|------|:---:|:---:|:---:|
| v1 | 原始 A/B 对照 | N/A (0/6 audit) | N/A (6/6 audit) | 无法量化 |
| v2 | 独立测试驱动 | 92% (72/78) | 99% (77/78) | **+6%** |
| v3 | 编排器强制执行 | 90% (36/40) | **100% (40/40)** | **+10%** |

| 复杂度 | A 组通过率 | B 组通过率 | 提升 |
|:---:|:---:|:---:|:---:|
| L1 | 94% | 100% | +6% |
| L2 | 100% | 100% | 0% |
| L3 | 79% | 100% | **+21%** |

**核心结论：复杂度越高，Harness 提升越大。** v2 辩论阶段发现的 24 个攻击点中，5 个被独立测试印证为真实可复现缺陷。v3 编排器强制 4 道质量门 → B 组 40/40 全过。

实验仓库：[trae-harness-experiments](https://github.com/zzzkeepdd/trae-harness-experiments)

---

## Why / 为什么

直接把需求丢给 AI，它会写代码，但也会幻觉、跳测试、自由发挥。"一人公司"不写代码，它**管理写代码的 AI**。

Throw requirements directly at AI — you get code, and hallucinations, skipped tests, unchecked edge cases. This harness doesn't write code. It *manages* the AI that writes code.

---

## Architecture / 架构

```
用户 ──需求──→ Codex Desktop（入口 + 编码引擎）
                  │
                  │ MCP 协议（毫秒级）
                  ▼
        ┌─────────────────────┐
        │   Hermes（后端大脑）  │
        │                     │
        │  5 个 MCP Tool：     │
        │  · module_one_start │
        │  · module_one_respond│
        │  · context          │
        │  · gate (G1-G7)     │
        │  · retrospect       │
        │                     │
        │  内部能力：          │
        │  · 长记忆 + 会话搜索 │
        │  · 宪法引擎         │
        │  · 子 Agent 并行    │
        └─────────────────────┘
```

三模块归属：

| 模块 | 领地 | 控制者 |
|------|------|:---:|
| 模块一：需求澄清 | Hermes | Hermes |
| 模块二：TDD 开发 | Codex | Codex |
| 模块三：复盘归档 | Hermes | Hermes |

Codex 是门口的服务员——收需求、路由、展示结果。Hermes 是后端大脑——记忆、辩论、门禁、复盘。

---

## 8 Gates / 八道闸门

全部由 Hermes 执行检查，Codex 只看到 `{pass, reason, required_fix}`。

| Gate | 位置 | 检查内容 | fail 行为 |
|:----:|------|------|------|
| G1 | 模块一辩论后 | 攻击点数 ≥ 维度×2，≥1 条 ≥3 分 | 回退补充辩论 |
| G2 | 规范生成后 | 无模糊词，测试任务对应，无循环依赖 | 回退修复规范 |
| G3 | 每 task 写完测试后 | 测试文件存在且能运行 | 回退重写测试 |
| G4 | 每 task 写完实现后 | 所有测试通过 + lint 无新增 | 回退修复 |
| G5 | 所有 task 完成后 | 每 task 有 G3+G4 记录，无遗留整改 | 回退处理 |
| G6 | 浏览器验收后 | ≥3 页截图 + 主题各≥1 + 移动端≥1 | 回退补充 |
| G7 | 复盘完成后 | 偏差非空 + 教训≥1 + 宪法已记录 | 回退补充 |

---

## 5 MCP Tools

| Tool | 输入 | 输出 |
|------|------|------|
| `module_one_start` | requirement, user_mode | status=ready, manifest |
| `module_one_respond` | feedback, user_mode | status, manifest (update) |
| `context` | task_description, task_id | related_memories, pitfalls, relevant_rules (≤300 token) |
| `gate` | gate_id, evidence | pass, reason, required_fix |
| `retrospect` | manifest, audit_trail, acceptance_report | lesson_summary (≤300 token) |

---

## Execution Loop / 执行闭环

```
用户需求
→ Codex 调 module_one_start(requirement, user_mode)
→ Hermes 返回 manifest
→ Codex 按 manifest.tasks 逐个执行 TDD：
    → 调 context(task_description, task_id)
    → RED 写测试 → 调 gate("G3", evidence)
    → GREEN 写实现 → 调 gate("G4", evidence)
    → REFACTOR → 内部 code-qa
    → 不通过 → 创建整改任务追加到末尾
→ 全部 task 完成 → 调 gate("G5", all_states)
→ Codex 浏览器验收 → 调 gate("G6", acceptance_data)
→ 调 retrospect(manifest, audit_trail, acceptance_report)
→ Hermes 写入长期记忆，返回 lesson_summary
→ Codex 展示 lesson_summary 给用户
```

---

## Quick Start / 快速开始

**前置：** Hermes + Codex Desktop + MCP 连通。

```bash
# 1. 把 harness skill 放到 Hermes skills 目录
cp -r one-person-company ~/.hermes/skills/

# 2. 把 Codex workflow skill 放到 Codex 配置目录
cp codex-harness-workflow/SKILL.md ~/.codex/AGENTS.md

# 3. 注册 Hermes Harness MCP server 到 Codex
codex mcp add hermes-harness -- python harness_mcp_server.py

# 4. 重启 Codex Desktop
```

然后在 Codex 里直接说需求即可。

---

## File Structure / 文件结构

```
one-person-company/
├── SKILL.md                        # Hermes 侧 v4.0 完整 skill
├── README.md                       # 本文件
├── codex-harness-workflow/
│   └── SKILL.md                    # Codex 侧 AGENTS.md 内容
├── codex-hermes-harness/
│   └── SKILL.md                    # 架构设计文档
├── references/
│   ├── gate-definitions.md         # 8 个 Gate 详细定义
│   ├── data-contract.md            # manifest / audit_trail 数据契约
│   ├── harness-mcp-server.md       # MCP server 部署说明
│   ├── codex-mcp-setup.md          # Codex MCP 配置指南
│   ├── trae-experiment-results.md  # Trae 实验完整数据
│   ├── v4-pitfalls.md              # v4 已知陷阱
│   ├── agent-roster/               # Agent 角色定义
│   ├── workflows/                  # 流程文件
│   ├── protocols/                  # 协议定义
│   └── constitution/               # 宪法规则
├── scripts/
│   ├── validate_debate_output.py
│   ├── check_testability.py
│   └── validate_execution_manifest.py
└── harness_mcp_server.py           # MCP server 主程序
```

---

## Modules / 三大模块

### 模块一：需求澄清（Hermes 领地）

复杂度分流 → 维度拆分 → 预调研 → 逐维度红蓝辩论 → Gate 1 → 审核裁决 → 规范生成 → Gate 2 → 用户确认 → 产出 manifest.json

### 模块二：TDD 开发（Codex 领地）

按 manifest.tasks 串行执行。每 task：调 context → 写测试 → Gate 3 → 写实现 → Gate 4 → 重构 → code-qa。全完成后 Gate 5 → 浏览器验收 → Gate 6 → 产出 audit_trail + acceptance_report

### 模块三：复盘归档（Hermes 领地）

偏差分析 → 攻击点印证 → 宪法对照 → 教训提取 → 写入 memory → Gate 7 → 返回 lesson_summary

---

## Lessons Learned / 踩过的坑

| # | 教训 |
|---|------|
| 1 | **15 个绿色测试 ≠ 能用的产品。** 测试必须验证行为，不是文件存在 |
| 2 | **Agent 会跳过验收链。** 解法：硬闸门（gate），不调就不能继续 |
| 3 | **复盘可能误判。** 复盘裁判必须交叉验证验收报告，不能只看表面 |
| 4 | **UX 产品需要浏览器级测试。** 截图+点击+主题切换+移动端，非代码验收 |
| 5 | **复杂度分级需要"用户可见"维度。** 浏览器可见 → 至少 L2 |
| 6 | **无交付物 + 无验证器 = 软建议。** 每条规则必须有具体交付物和验证方法 |
| 7 | **串行辩论让无聊但关键的维度被跳过。** 解法：维度拆分 + 并行子 Agent |
| 8 | **文件协议轮询 → 分钟级延迟。** v4.0 改 MCP，毫秒级响应 |

---

## Philosophy / 核心哲学

> Fight ambiguity with determinism. Constrain freedom with boundaries. Prevent hallucinations with rules.
> 用确定性对抗模糊，用边界约束自由，用规则防止幻觉。

> Real Harness ≠ 墙上守则。真正的 Harness 是流水线上的感应器和挡板——不靠 AI 自觉，靠硬性验证。

> Codex 负责做事和采证。Hermes 负责记忆和裁决。

---

## FAQ

**Q: 必须用 Codex Desktop？**
A: v4.0 基于 Codex Desktop + Hermes MCP。方法论平台无关，可移植到其他 IDE/Agent 组合。

**Q: Token 消耗？**
A: Hermes 侧低成本模型，Codex 侧高能力模型。辩论增加的低成本 Token 减少下游昂贵返工。≥3 模块的项目净正向。

**Q: 什么项目适合？**
A: 需求相对明确、对质量有要求的项目。个人工具到多模块应用。L1 管道支持小脚本。不适合一次性单行命令。

**Q: 为什么叫"一人公司"？**
A: 你 + AI 团队 = 一家公司。你是 CEO。Hermes 是你的幕僚长 (记忆 + 裁决)。Codex 是你的工程部 (做事 + 采证)。

---

## Roadmap / 后续计划

- [x] v4.0: Codex Desktop + Hermes MCP, 8 Gates, 5 MCP Tools
- [ ] v4.1: 完整红蓝辩论（模块一 true debate，非 stub）
- [ ] v4.2: Gate 规则自动进化（复盘 → 更新 gate 检查逻辑）
- [ ] v4.3: Skill 自动更新（复盘 → 自动创建/更新 skill）
- [ ] v4.4: 视觉验收自动化（截图对比 + 差异检测）
- [ ] v5.0: 多项目并行 + 跨项目教训迁移

---

## License

MIT

---

If this saves you from the pits we fell into, give it a ⭐.
如果这个项目帮你绕开了我们踩过的坑，给个 ⭐。

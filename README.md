# 一人公司 Harness v4.0 (One-Person Company)

> Codex Desktop 入口 + Hermes 后端。Codex 做编码和验收，Hermes 做记忆和裁决。
> Codex Desktop as entry point + Hermes as backend. Codex codes & verifies. Hermes remembers & judges.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## v4.0 核心变化 / What Changed

v3.x 是 Hermes 指挥 Codex——Hermes 做全部流程控制，Codex 被动执行，靠文件轮询通信（分钟级延迟）。

v4.0 反转：Codex Desktop 作为用户入口，Hermes 作为 MCP 后端服务。毫秒级实时通信，8 个 Gate 硬约束。

| | v3.x | v4.0 |
|---|------|------|
| 入口 | Hermes 聊天窗口 | Codex Desktop |
| 通信 | 文件轮询（cronjob，~1min延迟） | MCP 协议（毫秒级） |
| 流程控制 | Hermes 全控 | Hermes 控模块一/三，Codex 控模块二 |
| Gate | 文档里的建议（88%被跳过） | Hermes 执行的硬约束（不可跳过） |
| 记忆 | Hermes 内部 | Hermes 内部，Codex 不可见 |
| 编码 | Codex 被动执行 | Codex 主动控制 TDD 全流程 |

---

## Why / 为什么

直接把需求丢给 AI，它会写代码，但也会幻觉、跳测试、自由发挥。"一人公司"不写代码，它**管理写代码的 AI**。

v2 实验数据：
- 无 Harness：测试通过率 92%，2 安全漏洞，1 功能 bug
- 有 Harness：测试通过率 99%，0 漏洞，0 功能 bug
- 辩论阶段发现的 24 个攻击点中，5 个被独立测试印证为真实可复现缺陷

---

## Architecture / 架构

```
用户 (在 Codex Desktop 里说话)
  │
  ▼
┌──────────────────────────────────────┐
│          Codex Desktop               │
│  入口 + 模块二 (TDD编码+浏览器验收)   │
│                                      │
│  5 个 MCP Tool 调用 Hermes：          │
│    module_one_start → manifest       │
│    context → 记忆+踩坑               │
│    gate(G3-G6) → pass/fail           │
│    retrospect → 复盘归档              │
└──────────┬───────────────────────────┘
           │ MCP 协议 (stdio, 毫秒级)
           ▼
┌──────────────────────────────────────┐
│          Hermes (后端)               │
│  模块一 (需求澄清) + 模块三 (复盘)    │
│                                      │
│  内部能力：                           │
│    维度辩论 (红/蓝/裁判 3 角色)       │
│    长记忆 (跨会话)                    │
│    8 个 Gate 裁决                     │
│    宪法硬约束                         │
└──────────────────────────────────────┘
```

**锚点：Codex 负责做事和采证。Hermes 负责记忆和裁决。**

---

## v1.0 实现状态

| 能力 | 状态 |
|------|------|
| module_one_start 返回 manifest | v1.0 简化版（不做完整红蓝辩论） |
| G1/G2 结构校验 | v1.0 |
| G3-G7 硬约束 | v1.0 |
| context 记忆检索 | v1.0 |
| retrospect 复盘+记忆写入 | v1.0 |
| 完整维度辩论+用户确认 | v1.1 规划 |
| Gate 规则自动进化 | v1.1 规划 |

---

## 8 个 Gate (全在 Hermes 执行)

| Gate | 位置 | 检查 | fail 后果 |
|------|------|------|-----------|
| G1 | 辩论后 | 攻击点≥维度数×2，≥1个≥3分 | 回退补辩论 |
| G2 | 规范后 | 无模糊词，testable有对应测试 | 回退修规范 |
| G3 | 写测试后 | 测试文件存在+能运行 | 回退写测试 |
| G4 | 写实现后 | 所有测试通过+lint无新增 | 回退修复 |
| G5 | 全部task后 | 每task有G3+G4记录 | 回退处理 |
| G6 | 验收后 | ≥3页截图+深浅主题+375px | 回退补充 |
| G7 | 复盘后 | 偏差非空+≥1教训+宪法记录 | 回退补充 |

Gate 铁律：检查逻辑在 Hermes 内部，Codex 不知道规则细节。fail 只返回"哪里不满足"，不说"怎么修"。用户"只要结果"跳过确认门，但不降任何 Gate 标准。

---

## Quick Start / 快速开始

**前置要求：** Hermes + Codex CLI + MCP 配置

```bash
# 1. 添加 Hermes Harness MCP server 到 Codex
codex mcp add hermes-harness -- \
  C:\Users\Administrator\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe \
  C:\Users\Administrator\AppData\Local\hermes\hermes-agent\harness_mcp_server.py

# 2. 把 Codex workflow skill 放到 Codex 配置目录
cp codex-harness-workflow/SKILL.md ~/.codex/AGENTS.md

# 3. 重启 Codex Desktop
# 4. 在 Codex 里说需求，自动走闭环
```

---

## 执行闭环 / Execution Loop

```
用户需求
→ Codex 调 module_one_start(requirement, user_mode)
→ Hermes 返回 manifest
→ Codex 按 manifest.tasks 逐个执行 TDD
→ 每个 task 前调 context(task)
→ RED 写测试 → 调 gate("G3")
→ GREEN 写实现 → 调 gate("G4")
→ 全部 task 完成 → 调 gate("G5")
→ 浏览器验收 → 调 gate("G6")
→ 调 retrospect(manifest, audit_trail, acceptance_report)
→ Hermes 写入长期记忆 + 返回 lesson_summary
→ Codex 展示 lesson_summary 给用户
```

---

## 5 个 MCP Tool

| Tool | 签名 | 返回 |
|------|------|------|
| module_one_start | (requirement, user_mode) | {status:"ready", manifest, complexity} |
| module_one_respond | (feedback, user_mode) | {status, manifest} |
| context | (task_description, task_id) | {memories[], pitfalls[], rules[]} |
| gate | (gate_id, evidence) | {pass, reason, required_fix} |
| retrospect | (manifest, audit_trail, acceptance_report) | {summary, lesson_summary, violations} |

---

## 模块边界

- Hermes 不写代码，不直接改项目文件，不执行测试，不操作浏览器。
- Codex 不保留长期记忆，不修改 Gate 规则，不裁决自己是否通过 Gate。
- Codex 内部 subagent 不对 Hermes 暴露。
- Hermes 只能通过 Codex 提交的 evidence/audit_trail/acceptance_report 观察执行结果。

---

## Trae 实验数据 / Experiment Results

v2 独立测试（消除循环论证）：

| | A组 (无 Harness) | B组 (Harness) | 差值 |
|---|----|----|------|
| 测试通过率 | 92% | 99% | +6% |
| 功能性 bug | 1 | 0 | -1 |
| 安全漏洞 | 2 | 0 | -2 |
| 核心功能缺失 | 1 | 0 | -1 |

辩论阶段 24 个攻击点中，v2 测试印证 5 个为真实可复现缺陷。

---

## 踩过的坑 / Lessons Learned

1. 88% 的 Phase 在真实执行中被跳过——因为门是文档不是 tool。v4.0：全部 Gate 由 Hermes 硬执行。
2. 单 Agent 内化毁了对抗性。v4.0：红/蓝/裁判用不同 system prompt，Hermes 和 Codex 天然盲区。
3. 用户说"只要结果"→ 全部防御崩塌。v4.0：L2 保障模式，保留全部 Gate。
4. 验证脚本只检查格式不检查实质。v4.0：G4 检查测试是否通过，G6 检查截图数量。
5. 测试先行原则从未遵守。v4.0：G3 检查测试文件存在，不通过拒绝 code-qa。
6. 复盘从未触发。v4.0：retrospect 是闭环最后一步，G7 检查复盘产出。

---

## FAQ

**Q: Token 成本？**
A: Hermes 侧用低成本模型，Codex 侧用高能力模型。辩论增加的低成本 Token 显著减少下游昂贵返工。

**Q: 必须用 Hermes + Codex？**
A: 当前基于这两个平台，但 Harness 是平台无关的纯文本规则，可移植。

**Q: 为什么叫"一人公司"？**
A: 你一个人 + 一支 AI 团队 = 一家公司。你是 CEO，Hermes 是参谋长，Codex 是工程部。

---

## License

MIT

---

如果这个项目帮你绕开了我们踩过的坑，给个 ⭐。
If this saves you from the pits we fell into, give it a ⭐.

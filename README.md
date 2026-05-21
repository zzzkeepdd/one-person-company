# 一人公司 Harness v3.1 (One-Person Company)

> A reusable AI collaboration harness that makes Hermes + Codex work like a real dev team.
> 一个可复用的 AI 协作编排框架，让你的 Hermes + Codex 像一支真正的开发团队那样工作。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## v3.1 Highlights / 亮点

| Feature | What |
|---------|------|
| **维度拆分 + 并行辩论** | 需求拆分为 3-7 独立维度，每个维度独立子Agent并行辩论——防 AI 注意力偏斜遗漏 |
| **攻击点评分** | 每攻击点打分（1擦边球→5颠覆），至少 1 条直击核心（≥3分），硬计数不可水 |
| **领域模板** | 量化平台/Web全栈/CLI工具/数据管道 四套维度模板——笼统需求自动注入默认值，改错优于填空 |
| **JSON 标准接口** | 模块间强制 JSON schema，辩论输出 + 执行清单双校验 |
| **信息瓶颈** | 模块一→模块二只传 ~200 token JSON，按需回查 spec |
| **三级管道 (L1/L2/L3)** | L1 超轻（Hermes直写不调Codex）→ L2 辩论1轮 → L3 完整流程 |
| **节点门 + 宪法 v1.4** | 五道硬闸门 + C11 维度强制覆盖 + 半自动草案生成 |

---

## v3.0 → v3.1 改进动机

v3.0 的模块一仍是串行辩论——所有需求维度混在一起，AI 注意力被"有趣"维度（策略逻辑/AI信号）抢走，跳过"无聊但关键"的维度（本金输入框/风控滑块），导致 V4 量化平台遗漏两个明确需求。

v3.1 解法：维度拆分 + 并行辩论 + 攻击点评分。每个维度独立子Agent只处理一亩三分地，不会被其他维度抢注意力。攻击点硬计数+评分防"水"攻击点。笼统需求匹配领域模板注入默认值。

---

## Why / 为什么

Throwing requirements directly at AI gets you code — and hallucinations, skipped tests, and unchecked edge cases. "One-Person Company" is a battle-tested multi-agent harness that doesn't write code. It *manages* the AI that writes code, through three mandatory phases:

直接把需求丢给 AI，它会写代码，但也会幻觉、跳测试、自由发挥。"一人公司"不写代码，它**管理写代码的 AI**，通过三个强制阶段：

| Phase | What / 内容 |
|-------|-------------|
| **Red-Blue Debate (红蓝对抗)** | Attack the spec before a line of code exists — find holes, not after |
| **Test-Driven Development** | Integration + E2E tests are the only definition of "done" |
| **Retrospective + Constitution (复盘宪法)** | Every failure writes a rule. Violations accumulate consequences. |

---

## Philosophy / 核心哲学

> Fight ambiguity with determinism. Constrain freedom with boundaries. Prevent hallucinations with rules.
> 用确定性对抗模糊，用边界约束自由，用规则防止幻觉。

> Real Harness ≠ 墙上守则。真正的 Harness 是流水线上的感应器和挡板——不靠 AI 自觉，靠硬性验证。
> A real harness isn't a poster on the wall. It's sensors and gates on the assembly line — not relying on AI self-discipline, but on hard verification.

---

## Skill vs Harness — What's the difference? / 和普通 Skill 有什么区别？

A **Skill** is a long document the AI reads once and may selectively ignore — like an employee handbook left on a desk. A **Harness** is a pipeline where each stage loads only the current step's instructions. The AI doesn't know what comes next, so it can't skip ahead. Paired with the auditor script, no deliverable = no green light.

**Skill** 是一份长文档，AI 一次性读完，可以选择性忽略——像桌上摆的员工手册。**Harness** 每个阶段只加载当前步骤的指令，AI 不知道下一步是什么，无法跳步。配合审计脚本，不产出交付物就不放行。

| | Skill | Harness |
|---|-------|---------|
| Structure | One long file | Entry (40 lines) + 25 focused files |
| AI sees | Everything at once | Only the current stage |
| Enforcement | Self-discipline | Hard gates + auditor script |
| Skip possible? | Yes — AI can "understand" and jump | No — only current step's instructions exist |

---

## Architecture / 架构

```
User / 用户
├── Domain Template Match ── 领域模板注入默认值 (v3.1)
├── PlannerAgent ──── Pre-clarification ──── QA rounds until ready
├── Dimension Split ── 3-7 独立维度 (v3.1)
│      ├── [维度1] delegate_task → 子Agent A (红蓝+裁判+评分)
│      ├── [维度2] delegate_task → 子Agent B
│      ├── [维度3] delegate_task → 子Agent C
│      ├── [维度4] delegate_task → 子Agent D
│      └── [维度5] delegate_task → 子Agent E
├── Dimension Aggregation ── 聚合+跨维度冲突检查 (v3.1)
│      ├── validate_debate_output.py (节点门1: JSON schema + 维度覆盖 + 攻击点评分)
│      └── check_testability.py (节点门2: 验收标准可测性)
├── SpecGenerator ── Spec + Acceptance Criteria
├── Codex Dev Team ── TDD ──── AI Programmer + Executor + Frontend
│      ├── validate_execution_manifest.py (节点门3: 执行清单校验)
│      ├── Code QA (integration tests)
│      └── Func QA (E2E tests + browser walkthrough)
│      └── harness_auditor.py ── 最终闸门 (--pipeline l1/l2/l3)
└── RetroJudge ── Retro Debate ── Prosecution vs Defense → Constitution update
                            └── proposals.md (草案暂存 → 人工确认 → 合并进宪法)
```

Hermes (DeepSeek V4) plans and reviews. Codex (GPT-5.5) executes code. Connected via MCP protocol with shared project folder as state hub.

Hermes (DeepSeek V4) 负责规划和审核，Codex (GPT-5.5) 负责代码执行。通过 MCP 协议连接，共享项目文件夹作为状态中枢。

> Platform-agnostic pure-text methodology. Core rules work on any multi-agent or single-model setup.
> 平台无关的纯文本方法论，核心规则可移植到任何多 Agent 或单一模型环境。

---

## Quick Start / 快速开始

**Prerequisites / 前置要求：** [Hermes](https://github.com/nousresearch/hermes) desktop + [Codex CLI](https://github.com/openai/codex) + MCP configured between them.
[Hermes](https://github.com/nousresearch/hermes) 桌面端 + [Codex CLI](https://github.com/openai/codex) + 两者间配好 MCP。

```bash
# If using Hermes, place this under its skills directory
# Hermes 用户：放到 skills 目录下
cp -r one-person-company ~/.hermes/skills/

# Or /new to reload. Then invoke:
# 然后调用：
"Hermes, 启动一人公司，我要开发一个 [your project]"
```

---

## Structure / 项目结构

```
one-person-company/
├── SKILL.md                        # Entry — 3-step dispatch (≤40 lines)
├── schemas/                        # v3.0 JSON 接口定义
│   ├── debate-output.schema.json   # v3.1: +dimensions_covered +attacks
│   └── execution-manifest.schema.json
├── references/
│   ├── agent-roster/               # 14 agent prompts + rules + red lines
│   ├── workflows/                  # Module 1-3 step-by-step flows
│   ├── protocols/                  # Communication, lifecycle, handover
│   ├── domain-templates.md         # v3.1: 领域维度模板（量化/Web/CLI/ETL）
│   ├── data-contract.md            # v3.0 JSON 接口数据契约
│   ├── vague-words.txt             # v3.0 模糊词黑名单
│   └── constitution/               # Management rules + proposals.md
├── scripts/
│   ├── harness_auditor.py          # 最终闸门 (--pipeline l1/l2/l3)
│   ├── validate_debate_output.py   # 节点门1 (v3.1: +维度覆盖+攻击点评分)
│   ├── check_testability.py        # 节点门2
│   └── validate_execution_manifest.py  # 节点门3
├── pipelines/                      # v3.0 管道配置
│   ├── l1-light.md
│   ├── l2-standard.md
│   └── l3-full.md
└── README.md                       # You're here
```

---

## Three Modules / 三大模块

### Module 1: Requirement Clarification (Red-Blue Debate)
### 模块一：需求澄清（红蓝对抗）

**v3.1: 维度拆分 + 并行辩论。** 预澄清后按领域模板拆分为 3-7 个独立维度，每个维度启动独立子Agent并行辩论。子Agent只处理本维度——不被其他维度抢注意力。攻击点硬计数（≥维度数×2）+ 评分（至少1条≥3分直击核心）。维度聚合时检查跨维度冲突。

Before any code, stress-test the spec. Blue builds the plan. Red attacks every edge case (network failure, empty input, race conditions). Analyst fact-checks disputes. Judge converges within 3 rounds. Output: JSON schema-validated debate result → 节点门1/2 check.

写代码前先拷问需求。蓝队构建方案，红队攻击边界条件，分析师核查事实分歧，裁判 3 轮内收敛。输出经 JSON schema 校验的辩论结果 → 节点门1/2检查。

### Module 2: Test-Driven Development
### 模块二：测试驱动开发

Receives ~200 token execution manifest (not full spec). Code QA runs integration tests first. Func QA runs E2E tests + browser walkthrough (for UI products). Both reports must exist. Multiple agents collaborate — developer writes, QA reviews independently. **Auditor script verifies all reports before delivery — no reports, no release.**

接收 ~200 token 执行清单（非完整 spec）。代码验收先跑集成测试，功能验收跑端到端测试 + 浏览器实操。多 Agent 合作——开发写、验收独立审。**审计脚本验证所有报告存在后才放行。**

### Module 3: Retrospective & Constitution
### 模块三：复盘与宪法

After delivery, optionally run a retro debate (L3: mandatory reminder, skippable). If preventable, AI drafts a rule to proposals.md. User approves → merges into constitution. Constitution auto-injected into future prompts. Violations accumulate: 3rd = special warning, 5th = severe warning.

交付后可选择复盘辩论（L3：强制提醒但可跳过）。可预防问题由 AI 起草规则到 proposals.md，用户确认后合并进宪法。宪法自动注入后续提示词。违规累计：第 3 次特别提醒，第 5 次严重警告。

---

## Lessons Learned / 踩过的坑

| # | Lesson / 教训 |
|---|---------------|
| 1 | **15 green tests ≠ working product.** Unit tests passed but templates weren't rendering, tags pages 404'd. Tests must verify *behavior*, not just file existence. |
| 2 | **Agents skip the acceptance chain if allowed.** Hermes coordinator ran `pytest`, saw green, declared done — without ever calling code-qa or func-qa. Solution: hard gate (auditor script). |
| 3 | **Retros can misdiagnose.** First retro blamed "external force" for a skipped acceptance chain. Retro judge must cross-check the acceptance reports, not just trust the surface story. |
| 4 | **UX products need browser-level testing.** `subprocess.run(['mdblog', 'build'])` != a real user clicking links in a browser. Func QA now requires browser automation walkthroughs for UI products. |
| 5 | **Complexity grading needs a "user-visible" dimension.** If a human sees the output in a browser, it's at least medium — no shortcuts on acceptance. |
| 6 | **No deliverable + no verifier = soft suggestion, not a rule.** Every rule in the harness now requires a concrete deliverable and verification method (Meta-Rule M01). |
| 7 | **Serial debate loses boring-but-critical requirements.** AI attention is captured by "interesting" dimensions (strategy logic, AI signals) and silently skips "boring" ones (input boxes, sliders). Solution: dimension split + parallel sub-agents per dimension (v3.1). |

---

## Human Touchpoints / 人机交互点

The harness is mostly autonomous, but stops at 3 points for your input:
大部分流程自动化，但会在 3 个节点停下等你：

1. **Pre-clarification** — PlannerAgent asks 2-5 questions about your requirements / 计划Agent 提问澄清需求
2. **Spec confirmation** — After debate + spec generation, you review and approve / 辩论后确认《需求规格说明书》
3. **Retrospective** — After delivery, you decide whether to run a retro / 交付后你是否要复盘

---

## FAQ

**Q: Token cost?**
A: Hermes side uses low-cost models (DeepSeek V4). Codex side uses high-capability (GPT-5.5). The debate's extra token spend reduces expensive downstream rework. Net positive on any project with >3 modules.
Hermes 侧用低成本模型，Codex 侧用高能力模型。辩论增加的低成本 Token 能显著减少下游昂贵返工。

**Q: Must I use Hermes + Codex?**
A: Currently implemented on these two, but the harness is platform-agnostic text rules. Adaptable to any multi-agent or single-model environment.
目前基于这两个平台，Harness 是平台无关的纯文本规则，可移植。

**Q: What projects fit?**
A: Projects with clear-ish requirements and quality demands. Personal tools to multi-module apps. Now with L1 pipeline for small scripts (≤3 files, single tech stack). NOT for throwaway one-liners.
需求相对明确、对质量有要求的项目。现在 L1 管道支持小脚本（≤3 文件，单一技术栈）。不适合一次性单行命令。

**Q: Why "One-Person Company"? / 为什么叫"一人公司"？**
A: You + an AI team = a company. You're the CEO. Hermes is your chief of staff. Codex is your engineering department.
你一个人 + 一支 AI 团队 = 一家公司。

---

## Roadmap / 后续计划

- [x] JSON 标准接口 (v3.0)
- [x] 信息瓶颈 ~200 token (v3.0)
- [x] 三级管道 L1/L2/L3 (v3.0)
- [x] 节点门 + 宪法半自动 (v3.0)
- [x] 维度拆分 + 并行辩论 + 攻击点评分 (v3.1)
- [ ] Lightweight automated visual acceptance for frontend
- [ ] Skill templates for more project types
- [ ] Community-shared constitution rules

---

## License

MIT

---

If this saves you from the pits we fell into, give it a ⭐.
如果这个项目帮你绕开了我们踩过的坑，给个 ⭐。

# 一人公司 (One-Person Company)

> A reusable AI collaboration harness that makes Hermes + Codex work like a real dev team.
> 一个可复用的 AI 协作编排框架，让你的 Hermes + Codex 像一支真正的开发团队那样工作。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
├── PlannerAgent ──── Pre-clarification ──── QA rounds until ready
│      ├── DebateJudge + Red + Blue + Analyst ── Module 1
│      └── SpecGenerator ── Spec + Acceptance Criteria
├── Codex Dev Team ── TDD ──── AI Programmer + Executor + Frontend
│      ├── Code QA (integration tests)
│      └── Func QA (E2E tests + browser walkthrough)
│      └── Auditor Script ── hard gate: all reports present?
└── RetroJudge ── Retro Debate ── Prosecution vs Defense → Constitution update
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
├── SKILL.md                    # Entry — 3-step dispatch (≤40 lines)
├── references/
│   ├── agent-roster/           # 14 agent prompts + rules + red lines
│   ├── workflows/              # Module 1-3 step-by-step flows
│   ├── protocols/              # Communication, lifecycle, handover, cost budget, prerequisites
│   └── constitution/           # Management rules + violation records (dynamic)
├── scripts/
│   └── harness_auditor.py      # Hard gate: verifies all reports exist before delivery
└── README.md                   # You're here
```

---

## Three Modules / 三大模块

### Module 1: Requirement Clarification (Red-Blue Debate)
### 模块一：需求澄清（红蓝对抗）

Before any code, stress-test the spec. Blue builds the plan. Red attacks every edge case (network failure, empty input, race conditions). Analyst fact-checks disputes. Judge converges within 3 rounds. **Simple projects skip debate but still go through SpecGenerator.**

写代码前先拷问需求。蓝队构建方案，红队攻击边界条件，分析师核查事实分歧，裁判 3 轮内收敛。简单项目跳过辩论，但仍走规范生成。

### Module 2: Test-Driven Development
### 模块二：测试驱动开发

Integration tests + E2E tests are mandatory. Code QA runs integration tests first. Func QA runs E2E tests + browser walkthrough (for UI products). Both reports must exist. **Auditor script verifies all reports before delivery — no reports, no release.**

集成测试 + 端到端测试强制必过。代码验收先跑集成测试，功能验收跑端到端测试 + 浏览器实操。两份报告缺一不可。**审计脚本验证所有报告存在后才放行。**

### Module 3: Retrospective & Constitution
### 模块三：复盘与宪法

After delivery, optionally run a retro debate: prosecution argues "this was preventable" vs defense argues "one-time event." If preventable, a rule is written into the Management Constitution and auto-injected into future agent prompts. Violations accumulate: 3rd = special warning, 5th = severe warning.

交付后可选复盘辩论。可预防的问题写入管理宪法，下次自动注入 Agent 提示词。违规累计：第 3 次追加特别提醒，第 5 次严重警告。

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
A: Projects with clear-ish requirements and quality demands. Personal tools to multi-module apps. NOT for one-off 10-line scripts.
需求相对明确、对质量有要求的项目。不适合一次性脚本。

**Q: Why "One-Person Company"? / 为什么叫"一人公司"？**
A: You + an AI team = a company. You're the CEO. Hermes is your chief of staff. Codex is your engineering department.
你一个人 + 一支 AI 团队 = 一家公司。

---

## Roadmap / 后续计划

- Lightweight automated visual acceptance for frontend
- Skill templates for more project types
- Community-shared constitution rules

---

## License

MIT

---

If this saves you from the pits we fell into, give it a ⭐.
如果这个项目帮你绕开了我们踩过的坑，给个 ⭐。

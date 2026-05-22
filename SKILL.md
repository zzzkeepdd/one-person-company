---
name: one-person-company
description: '一人公司 全栈开发 Harness v4.0 — Codex Desktop入口+Hermes后端。Codex做编码+验收(模块二)，Hermes做记忆+辩论+门禁(模块一/三)。MCP协议实时通信，8个Gate硬约束。宪法v1.5含C01-C13+C27-C30实验修正。'
version: 4.0
phase: stable
---

# 一人公司 Harness v4.0

核心理念：用确定性对抗模糊，用边界约束自由，用规则防幻觉。用Gate防流程跳过。

**锚点：Codex 负责做事和采证。Hermes 负责记忆和裁决。**

## v1.0 实现状态

- module_one_start/respond 是简化版，不做完整红蓝辩论，直接返回 ready + manifest
- G1/G2 当前主要做结构校验（非真实辩论裁决）
- retrospect 做偏差分析+记忆写入，Gate 规则自动进化待 v1.1
- 完整维度辩论、Skill 自动更新 → v1.1+

## 架构总览

Codex Desktop = 用户入口 + 模块二（TDD编码+浏览器验收）控制者

Hermes = 模块一（需求澄清）+ 模块三（复盘归档）+ 全部8个Gate执行者

通信：MCP协议（harness_mcp_server.py），毫秒级实时响应，替代文件轮询

## 信息瓶颈

跨系统传输 ≤400 token/次。Hermes内部可转20万token推理，过边界时压缩。
Codex不知道辩论过程。Hermes不知道代码细节。盲区 = 天然对抗性保障。

## 三模块归属

| 模块 | 控制者 | Hermes内部 | Codex看到的 |
|------|--------|------------|-------------|
| 模块一 | Hermes | Phase 0-5 + Gate G1-G2 + 维度辩论 | 只拿到 manifest |
| 模块二 | Codex | 无（Codex自己控制） | TDD Step 0-5 + 调 Gate G3-G6 |
| 模块三 | Hermes | 偏差分析+宪法对照+教训→memory | 只拿到 lesson_summary |

## 8个Gate（全在Hermes执行）

| Gate | 位置 | 检查内容 | fail后果 |
|------|------|----------|----------|
| G1 | 模块一 辩论后 | 攻击点≥维度数×2，≥1个≥3分，所有维度有boundary | 回退补辩论 |
| G2 | 模块一 规范后 | 无模糊词，testable攻击点有对应测试，无循环依赖 | 回退修规范 |
| G3 | 模块二 写测试后 | 测试文件存在+能运行 | 回退写测试 |
| G4 | 模块二 写实现后 | 全部测试通过+lint无新增错误 | 回退修复 |
| G5 | 模块二 全部task后 | 每task有G3+G4记录，无遗留整改 | 回退处理 |
| G6 | 模块二 验收后 | ≥3页截图，深浅主题各≥1，375px移动端≥1 | 回退补充 |
| G7 | 模块三 复盘后 | 偏差非空，≥1条教训，宪法已记录 | 回退补充 |

Gate铁律：
- 检查逻辑在Hermes内部，Codex不知道规则细节（防预判绕过）
- fail只返回"哪里不满足"，不说"怎么修"（强制Codex重新推理）
- 用户"只要结果"跳过确认门，但不降任何Gate标准（L2保障模式）

## 5个MCP Tool

| Tool | 签名 | 返回 |
|------|------|------|
| module_one_start | `(requirement, user_mode)` | `{status:"ready", manifest, complexity}` |
| module_one_respond | `(feedback, user_mode)` | `{status, manifest}` |
| context | `(task_description, task_id)` | `{memories[], pitfalls[], rules[]}` |
| gate | `(gate_id, evidence)` | `{pass, reason, required_fix}` |
| retrospect | `(manifest, audit_trail, acceptance_report)` | `{summary, lesson_summary, violations}` |

## 复杂度分级

| 管道 | 判定 | 辩论 | 开发 | 复盘 |
|------|------|------|------|------|
| L1 | ≤3文件/单一技术栈/无用户产品/无新依赖 | 跳过 | Codex TDD | 跳过 |
| L2 | 中等（默认） | 必走1轮/维度 | Codex TDD | 可选 |
| L3 | 多系统/跨平台/复杂并发 | 必走2轮/维度 | Codex TDD | 强制 |

## 模块一详细流程（Hermes内部）

Phase 0：复杂度分流 → 搜索记忆 → 判定L1/L2/L3
Phase 0.5：维度拆分 → 领域模板强制覆盖
Phase 1：预调研 → 3调研员并行
Phase 2：逐维度并行辩论 → 红/蓝/裁判3角色，不同system prompt
  Gate G1：辩论质量门
Phase 3：审核裁决 → 3审核员并行
Phase 4：规范生成 → 产出 manifest（≤2000 token）
  Gate G2：规范质量门
Phase 5：handoff → manifest 交给 Codex

用户skip → L2保障模式（跳过确认但不降Gate）

## 模块二详细流程（Codex控制）

每个task串行：
  Step 0：调 context(task) → 获取记忆+踩坑+宪法约束
  Step 1：写测试（RED）→ 调 Gate G3
  Step 2：写实现（GREEN）→ 调 Gate G4
  Step 3：重构
  Step 4：内部code-qa → 不通过则追加整改任务（不标"整改"）

全部task后：
  调 Gate G5
  浏览器验收（Codex自己）：逐页截图+深浅主题+375px移动端
  调 Gate G6

## 模块三详细流程（Hermes内部）

消费 manifest + audit_trail + acceptance_report
  偏差分析：计划 vs 实际
  攻击点印证：哪些真的触发了
  宪法对照：条目触发计数
  教训提取 → 写入 MEMORY.md
  Gate G7：复盘质量门

输出 → lesson_summary ≤300 token（由Codex展示给用户）

## 用户降级规则

"只要结果"/"go ahead"/"不用问我"：
  跳过：维度确认交互、执行清单确认交互
  保留：全部8个Gate按原标准执行
  保留：模块三复盘完整执行

## 宪法（硬约束）

C01-C13 继承自 v3.x。新增实验修正：
  C27：测试即门 — 没有测试就没有交付
  C28：最小验证集合 — 每个验证脚本必须有golden negative测试
  C29：无用户模式降级保障 — 用户跳过确认时保留全部Gate
  C30：code-qa实效性 — 必须实际运行代码，不能仅代码审查

## Handoff 数据格式

模块一→模块二：manifest = `{project, tasks: [{id, dimension, description, acceptance_criteria, depends_on, testable_attacks, preventive_checks}]}`
模块二→模块三：audit_trail + acceptance_report

## 参考索引

- MCP Server：references/harness-mcp-server.md
- MCP 配置：references/codex-mcp-setup.md
- Gate定义：references/gate-definitions.md
- 数据契约：references/data-contract.md
- 复杂度：references/complexity-grading.md
- 维度模板：references/domain-templates.md
- Trae实验：references/trae-experiment-results.md
- GitHub推送：references/github-push-workflow.md

按需加载单文件，禁止一次性加载全部。

## 已知陷阱

### 流程陷阱（实验教训 — 致命级）

- 88%的Phase在真实执行中被跳过。根因：门是文档不是tool。v4.0解决了——所有Gate由Hermes的gate() tool硬执行。
- 单Agent内化毁了对抗性。v4.0：红/蓝/裁判用不同system prompt，Hermes和Codex是两个独立系统天然盲区。
- 用户说"只要结果"→全部防御崩塌。v4.0：L2保障模式，跳过确认但不降Gate。
- 验证脚本只检查格式不检查实质。v4.0：G4检查测试是否运行/pass，G6检查截图数量。
- 测试先行原则在实验中未遵守。v4.0：G3检查测试文件存在，不通过→拒绝code-qa。
- 复盘从未触发。v4.0：retrospect是Codex执行闭环的最后一步，G7检查复盘产出。

### 模块一陷阱

- L1判据严格（≤3文件/单一技术栈/无用户产品/无新依赖），不适用于框架级重构。
- 维度拆分是硬性要求（C11），即使只有一个维度也必须显式声明。
- 每个维度独立子Agent并行辩论，攻击点硬计数≥维度数×2，至少1条≥3分。
- 维度聚合后必须检查跨维度冲突（XCONFLICT）。

### GUI验收陷阱（C13 — 致命级）

- Hermes无视觉能力，不可用`python -c "import main"`代替GUI验收。
- 桌面GUI验收必须：启动界面→逐个标签页点击→每标签页截图。
- 常见遗漏：策略文件夹缺失、账户余额显示错误、设置滑块不可拖。
- PyQt QTableWidget列宽：状态列≥120px，阈值列≥140px，说明列用Stretch。

### V4代码修改前置检查（致命级）

- 修改前必须读取四份文档：踩坑经验手册.md、PROJECT_PLAN.md、PROJECT_LESSONS.md、PROJECT_BRAIN.md。
- 策略文件夹不需要手动"清理"。strategy_loader.py已内置过滤。
- 改坏main.py最快恢复：`git checkout HEAD -- main.py`。

### OKX 代理/直连策略

- 国内必须走代理优先。顺序：代理→备用域名→直连兜底。不要反转。
- "OKX API问题不是解决了嘛"=现有代理配置已工作，不是要改成直连。

### Codex 429限流

- 429不是Codex坏了，是API瞬时流量控制。等1-5分钟。不要反复重试。
- 预防：Codex任务之间加30秒间隔。

### 辩论评分基数（实验数据）

- v2实验：24攻击点中5个被独立测试印证为真实bug。
- 攻击点分两类：testable（可写测试）和preventive（设计约束）。
- L1: ≥3个攻击点，≥1个≥3分。L2: ≥4个，≥2个≥3分。L3: ≥5个，≥3个≥3分。

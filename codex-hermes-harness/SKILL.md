---
name: codex-hermes-harness
description: 'Codex+Hermes 一人公司 Harness v4.0 — Codex Desktop 作为入口和流程控制器，Hermes 作为记忆/辩论/门禁后端。8 Gate 硬约束，信息瓶颈 ≤400 token/次调用，状态机驱动不可跳过。'
version: 4.0
phase: design
---

# Codex + Hermes 一人公司 Harness v4.0

架构反转：Codex Desktop 是入口和编码引擎，Hermes 是记忆库+辩论引擎+门禁。

核心哲学不变：用确定性对抗模糊，用边界约束自由，用规则防幻觉。

## 两个角色的边界

Hermes 的职责（只做这三件事，不做其他）：
1. 记忆检索 —— context()：根据任务描述检索记忆+历史+宪法约束
2. 维度辩论 —— clarify()：单维度红蓝对抗辩论，输出攻击点+裁决
3. 门禁验证 —— gate()：检查每个阶段产出是否达标，不通过则拒绝进入下一阶段
4. 复盘归档 —— retrospect()：偏差分析+宪法对照+教训写入记忆

Codex 的职责（只做这三件事，不做其他）：
1. 用户交互 —— 接收需求、展示结果、请求确认
2. 流程控制 —— 按状态机驱动 Phase 0-5
3. 代码执行 —— TDD 开发、内部 QA、浏览器验收

边界规则：
- Codex 不保留长期记忆。所有"上次踩过的坑"由 Hermes 在 context() 时注入。
- Hermes 不碰代码。不生成执行清单（由 Codex 生成），不写代码，不做验收。
- 每次跨边界传输 ≤400 token。Hermes 内部可以并行跑 20 万 token 推理，但过边界时压缩。

## Hermes 暴露的五个 Tool（给 Codex 调用）

### module_one_start(requirement, user_mode)
启动模块一需求澄清。返回复杂度判定 + 维度列表 + 是否等待用户确认。
  user_mode: "normal"（正常交互）或 "just_result"（L2保障模式）

输入：原始需求文本、用户模式
内部：memory search + 复杂度分级 + 维度拆分
输出：
  {
    status: "ready" | "need_user_input",
    complexity: "L1"|"L2"|"L3",
    dimensions: [{name, rationale}],
    manifest_template: {...},  // v1.0 简化版，完整辩论 v1.1
    handoff: {note: "..."}
  }

### module_one_respond(feedback)
处理用户对模块一的反馈，继续澄清流程。
  在 module_one_start 返回 need_user_input 后调用。
  feedback 为 "skip"/"go"/"只要结果" 等 → 进入 L2 保障模式。
  正常反馈 → 产出执行清单模板。

输入：用户反馈文本
输出：{status, message, handoff}

### context(task_description, task_id)
输入：当前任务描述、任务 ID
内部：memory + session_search 精确检索
输出（≤300 token）：
  {
    related_memories: [≤3条, 每条一句话],
    pitfalls: [≤2条, 每条: 场景 + 后果],
    relevant_rules: [≤3条, 来自宪法, 每条一行]
  }

### gate(phase_id, payload_json)
输入：阶段 ID(G1-G7)、待验证数据
内部：对应 gate 的检查规则（见 Gate 定义）
输出：{pass: bool, reason: "一句话"}
不提供修复建议。Codex 不知道 gate 的具体检查逻辑，只知道 pass 或 fail。

### retrospect(manifest_json, acceptance_report_json)
输入：执行清单 JSON + 验收报告 JSON
内部：偏差分析、宪法对照、教训提取
输出（≤300 token）：{deviations, violations, lessons}
副作用：memory.write、skill.update、gate_rules.update（如果发现 gate 未拦住真实 bug）

## 状态机（Codex 侧硬编码）

Codex 加载本 skill 时，以下状态转换是强制执行的——不是建议，是状态机：

```
STATE: START
  → 接收用户需求
  → 进入 STATE: assess_complexity

STATE: assess_complexity
  → 调 hermes.module_one_start(requirement, user_mode)
  → 根据复杂度分级标准（见 references/complexity-grading.md）判定 L1/L2/L3
  → L1: 跳过 STATE: clarify → 直接进入 STATE: generate_manifest
  → L2/L3: 进入 STATE: clarify
  → 调 hermes.gate('G1', {complexity, dimensions_identified, rationale})

STATE: clarify
  → 列出维度列表，展示给用户（可选，L2 保障模式跳过展示）
  → 用户反馈后调 hermes.module_one_respond(feedback)
  → 用户确认维度列表后（L2 保障模式跳过确认），立即删除 clarify 上下文
  → 调 hermes.gate('G2', {all_clarify_results, dimension_count})

STATE: generate_manifest
  → Codex 自己合并所有 clarify 结果，生成执行清单 JSON
  → testable_attacks → 对应验收测试任务
  → preventive_attacks → 代码审查检查项
  → 调 hermes.gate('G3', {manifest_json})

STATE: execute_tasks
  → 按执行清单逐个 task 串行执行
  → 每个 task 的子状态机：
      SUBSTATE: load_context
        → 调 hermes.context(task_description, task_id)
      SUBSTATE: write_test
        → 写测试代码（RED 阶段）
        → 调 hermes.gate('G4-1', {task_id, test_file_exists, test_runs})
      SUBSTATE: write_code
        → 写实现代码（GREEN 阶段）
      SUBSTATE: refactor
        → 重构（REFACTOR 阶段）
      SUBSTATE: qa
        → 运行所有测试
        → 调 hermes.gate('G4-2', {task_id, tests_pass, lint_clean})
        → Codex 内部 code-qa
        → QA 不通过 → 创建整改任务追加到清单末尾（整改任务不知道自己是整改）
  → 所有 task 完成后调 hermes.gate('G5', {all_task_results})

STATE: acceptance
  → Codex 打开浏览器验收
  → 逐页截图、链接点击、深浅主题切换、375px 移动端
  → 调 hermes.gate('G6', {acceptance_report, screenshots_count, theme_check, mobile_check})

STATE: retrospect
  → 调 hermes.retrospect(manifest_json, acceptance_report)
  → 调 hermes.gate('G7', {retrospect_output})

STATE: DONE
  → 展示最终摘要给用户
```

## Gate 定义（8 个，由 Hermes 执行）

每个 gate 返回 {pass: bool, reason: "失败原因（不包含修复建议）"}

### G1：复杂度分级 → 维度拆分
检查：
- complexity 字段存在且为 L1/L2/L3 之一
- dimensions_identified ≥ 3 个，每个有一句话理由
- L3 标记有触发条件说明

### G2：维度辩论 → 清单生成
检查：
- 每个维度 attack_points ≥ 2
- 至少 1 个 attack 的 score ≥ 3
- 每个维度有 boundary.do + boundary.dont
- dimension_count = 原始维度数（覆盖率 100%）
- 无空 description 的 attack

### G3：清单生成 → 任务执行
检查：
- 每个 task 有验收标准（acceptance_criteria non-empty）
- 每个 testable attack 有对应测试任务
- depends_on 无循环依赖（拓扑排序通过）
- tasks count > 0

### G4-1：每个 task 测试编写 → 代码编写
检查：
- 测试文件存在
- 测试能运行（不要求通过，RED 阶段）
- 测试覆盖了本 task 的验收标准

### G4-2：每个 task 代码编写 → 下一个 task
检查：
- 所有测试通过
- lint 无新增错误（与 task 开始前对比）

### G5：所有 task 结束 → 验收
检查：
- 每个 task 有 G4-1 + G4-2 通过记录
- 无未处理的整改任务（清单中无 status=pending 的整改项）

### G6：验收结束 → 复盘
检查：
- 验收报告非空
- ≥3 个页面有截图证据
- 深色+浅色主题各 ≥1 张截图
- 移动端 375px ≥1 张截图

### G7：复盘结束 → 完成
检查：
- 偏差分析产出非空
- 至少 1 条教训已尝试写入 memory
- 宪法违规条目已记录

## 降级模式（L2 保障模式）

触发：用户说"只要结果"/"不用问我"/"go ahead"等跳过确认的指令

保留：
- 全部 8 个 Gate 按原标准执行
- Phase 0-5 完整流程
- 复盘归档

跳过：
- Phase 5 用户确认门（不再等待用户确认）
- 中间阶段的展示

不允许：
- 降低 gate 检查标准
- 跳过任何 gate
- Codex 自行判断"这个 gate 不重要"

## 宪法约束（从原 Harness 迁移）

见 references/constitution/management-rules.md

新增（基于 v2 实验结论）：

C27 测试即门：模块二 Step 1 产出的代码文件如果没有对应测试文件，G4-1 自动 fail，后续 Step 拒绝执行。

C28 最小验证集合：每个验证脚本必须包含至少一个"必定失败的输入"测试用例（golden negative case），并在框架 CI 中验证该失败被正确检出。

C29 无用户模式的降级保障：当用户显式跳过确认，系统自动进入 L2 保障模式——跳过确认门，但不跳过任何 gate。

C30 Gate 规则进化：复盘阶段发现 gate 未拦住的真实 bug → 更新对应 gate 的检查规则。gate 不是静态门槛，是会随项目复盘持续收紧的。

## 信息瓶颈设计（决定什么不传给谁）

Hermes 的盲区（不知道的）：
- Codex 写了什么代码
- 执行进度到哪了
- 验收结果（直到 retrospect 阶段）
- Codex 的 QA 过程

Codex 的盲区（不知道的）：
- 每个维度的完整辩论过程（只知道 clarify 返回的 ≤400 token）
- Hermes 记忆里不相关的内容（context() 只返回 ≤300 token 精确匹配）
- 宪法里跟当前任务无关的约束（context() 只返回 ≤3 条相关规则）
- Gate 的具体检查逻辑（只知道 pass/fail，不知道怎么判断的）
- 自己修改的代码以前是谁写的（除非 context() 返回了相关记忆）

## 执行清单格式（Codex 生成）

```json
{
  "project": "项目名",
  "complexity": "L1|L2|L3",
  "dimensions": ["维度1", "维度2"],
  "constitution_rules_triggered": ["C10", "C13"],
  "tasks": [
    {
      "id": "T1",
      "dimension": "维度1",
      "description": "一句话任务描述",
      "acceptance_criteria": ["AC1", "AC2"],
      "testable_attacks": ["attack_1", "attack_2"],
      "preventive_attacks": ["attack_3"],
      "depends_on": [],
      "file_scope": ["path/to/file.py"]
    }
  ],
  "acceptance_criteria": [
    {"id": "AC1", "description": "验收标准描述", "test_type": "unit|integration|e2e"}
  ]
}
```

## 参考索引

工作流程 → references/workflows/
宪法记录 → references/constitution/
复杂度标准 → references/complexity-grading.md
维度模板 → references/domain-templates.md
JSON 契约 → references/data-contract.md
Gate 检查规则 → references/gate-rules.md

## 已知陷阱

见原一人公司 Harness 的"已知陷阱"部分（全部保留）。

## 与原版的核心差异

1. 调用方向反转：Codex 主动调 Hermes（不是 Hermes 派发 Codex）
2. Gate 从"可选节点"变"状态机强制转换"
3. Hermes 不生成执行清单（Codex 自己生成，因为 Codex 是执行清单的消费者）
4. 验收归 Codex（浏览器实操），Hermes 只做复盘抽查
5. 信息瓶颈更激进：每次跨边界 ≤400 token，Gate 不暴露检查逻辑
6. 宪法由 Hermes 通过 context() 逐步注入，Codex 不知道完整宪法内容

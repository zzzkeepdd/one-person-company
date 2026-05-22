# Hermes Harness MCP Server

文件：`C:\Users\Administrator\AppData\Local\hermes\hermes-agent\harness_mcp_server.py`

启动方式：
```
python "C:/Users/Administrator/AppData/Local/hermes/hermes-agent/harness_mcp_server.py"
```

Codex MCP 配置（加到 Codex 的 MCP servers 列表）：
```json
{
    "hermes-harness": {
        "command": "python",
        "args": ["C:/Users/Administrator/AppData/Local/hermes/hermes-agent/harness_mcp_server.py"]
    }
}
```

## 5个MCP Tool

### module_one_start(requirement: str) -> JSON
启动模块一需求澄清。返回：
- status: "need_user_input" | "module_one_complete"
- complexity: "L1" | "L2" | "L3"
- dimensions: [{name, rationale}] 维度列表
- related_context: 记忆中的相关历史
- message: 给用户的确认消息

### module_one_respond(feedback: str) -> JSON
处理用户反馈，继续澄清。返回：
- 用户说"只要结果"→ L2保障模式（跳过确认但不跳Gate）
- 用户说"go"或确认维度 → 返回执行清单模板 + handoff信息

### context(task_description: str, task_id: str = "") -> JSON
取当前task的项目记忆+踩坑+宪法约束。返回：
- context: 文本 ≤300 token
- token_estimate: 估算token数
- memory_count, rules_count

### gate(gate_id: str, evidence: str) -> JSON
验证阶段产出。evidence是JSON string。返回：
- pass: bool
- reason: 一句话（通过）或失败原因（不提供修复建议）
- gate_id, gate_name

### retrospect(manifest: str, audit_trail: str = "", acceptance_report: str = "") -> JSON
模块三复盘。返回：
- status: "complete"
- deviations, violations, lessons: 剖析结果
- gate_evolution_notes: Gate规则进化建议
- memory_saved: bool
- summary: 给用户的文本摘要

副作用：写入 MEMORY.md、更新 skill

## 7个Gate

| Gate | phase_id | evidence格式 | 关键检查项 |
|------|----------|--------------|------------|
| G1 | 模块一辩论后 | {"dimensions": [{name,boundary,attacks}]} | 攻击点≥维度数×2，≥1个≥3分 |
| G2 | 模块一规范后 | {"tasks": [{id,description,acceptance_criteria,depends_on}]} | 无模糊词，testable攻击点有测试，无循环依赖 |
| G3 | 模块二测试后 | {"tests_exist": bool, "tests_run": bool} | 测试文件存在 |
| G4 | 模块二实现后 | {"all_tests_pass": bool, "lint_errors": int} | 全部测试通过，lint无新增 |
| G5 | 模块二全部后 | {"task_logs": [{task_id, G3, attempt_N}]} | 每task有G3+G4记录，无遗留整改 |
| G6 | 模块二验收后 | {"screenshots": int, "light_theme": bool, "dark_theme": bool, "mobile_375": bool} | ≥3页截图，主题各≥1，375px≥1 |
| G7 | 模块三复盘后 | {"deviations": list, "lessons": list, "constitution_checked": bool} | 偏差非空，≥1条教训，宪法已记录 |

## Handoff数据格式

### manifest.json（模块一→模块二）
```json
{
  "project": {"name": "...", "complexity": "L2"},
  "tasks": [
    {
      "id": "T1",
      "dimension": "维度名",
      "description": "具体描述（无模糊词）",
      "acceptance_criteria": ["可验证标准1"],
      "depends_on": [],
      "testable_attacks": [{"point": "...", "suggested_test": "test_xxx"}],
      "preventive_checks": [{"point": "...", "check_item": "review: xxx"}]
    }
  ]
}
```

### audit_trail.json（模块二→模块三）
```json
{
  "task_logs": [
    {
      "task_id": "T1",
      "G3": {"pass": true, "test_file": "...", "test_count": 5},
      "attempt_1": {"G4": {"pass": false, "failed_tests": 2}},
      "attempt_2": {"G4": {"pass": true, "all_pass": 7}},
      "code_qa": {"issues": 0},
      "final": "passed",
      "rework_count": 1
    }
  ],
  "summary": {"total_tasks": 12, "passed_first_attempt": 8, "rework_tasks": 4},
  "acceptance_report": {"screenshots": [...], "deviations": []}
}
```

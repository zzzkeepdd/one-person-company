# Gate定义 — 8个门禁的完整规则

## Gate执行原则

1. Hermes不告诉Codex解决方案：reason只说"哪里不满足"，不说"怎么修"
2. 门槛不随用户跳过而降低：L2保障模式保留全部Gate标准
3. Gate不可被Codex绕过：Codex workflow skill硬编码状态转换表
4. Gate规则持续进化：复盘发现漏网bug → 更新对应Gate检查规则
5. 唯一bypass方式：用户显式override（记录为宪法违规）

## G1 — 辩论质量门

位置：模块一 Phase 2（维度辩论）完成后
输入：{"dimensions": [{name,boundary,attacks:[{description,score}]}]}
检查：
  - 攻击点总数 ≥ 维度数 × 2
  - 每个维度有boundary定义
  - 所有attack有description（非空，非纯数字）
  - 至少1个attack score ≥ 3
fail示例：攻击点总数 3 < 维度数 2 × 2 = 4

## G2 — 规范质量门

位置：模块一 Phase 4（规范生成）完成后
输入：{"tasks": [{id,description,acceptance_criteria:[],depends_on:[]}]}
检查：
  - 无模糊词（合适/合理/足够/适当/酌情/尽量/可能/大概）
  - depends_on无循环依赖
  - depends_on引用的task_id存在
  - 每个task有acceptance_criteria（非空）

## G3 — 测试存在门

位置：模块二 每个task Step 1（写测试）完成后
输入：{"tests_exist": bool}
检查：
  - test文件存在（Codex上报）

## G4 — 实现质量门

位置：模块二 每个task Step 2（写实现）完成后
输入：{"all_tests_pass": bool, "lint_errors": int, "failed_tests": int}
检查：
  - 全部测试通过
  - lint无新增错误（lint_errors = 0）

## G5 — 模块完成门

位置：模块二 全部task完成后
输入：{"task_logs": [{task_id, G3:{pass}, attempt_1:{G4:{pass}}, ...}], "pending_rework": []}
检查：
  - 每个task有G3通过记录
  - 每个task有至少一个attempt的G4通过记录
  - pending_rework为空

## G6 — 验收质量门

位置：模块二 浏览器验收完成后
输入：{"screenshots": int, "light_theme": bool, "dark_theme": bool, "mobile_375": bool}
检查：
  - screenshots ≥ 3
  - light_theme = true
  - dark_theme = true
  - mobile_375 = true

## G7 — 复盘质量门

位置：模块三 复盘完成后
输入：{"deviations": list|int, "lessons": list|int, "constitution_checked": bool}
检查：
  - deviations非空（有偏差分析产出）
  - lessons ≥ 1（至少1条教训）
  - constitution_checked = true（宪法条目已记录）

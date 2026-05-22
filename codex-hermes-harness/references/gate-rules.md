# Gate 检查规则

每个 gate 在 Hermes 内部执行。Codex 调用 hermes.gate(phase_id, payload_json) → 返回 {pass: bool, reason: "失败原因"}。

Reason 不包含修复建议。Codex 不知道具体哪条规则没通过——只知道"边界不清晰"而不是"维度'缓存策略'缺少 boundary.dont 定义"。这种模糊性迫使 Codex 重新审查全部输出，而不是针对一点打补丁。

## G1：复杂度分级 → 维度拆分

```python
def gate_G1(payload):
    issues = []

    if "complexity" not in payload or payload["complexity"] not in ["L1", "L2", "L3"]:
        issues.append("复杂度分级缺失或无效")

    dims = payload.get("dimensions_identified", [])
    if len(dims) < 3:
        issues.append("维度数量不足")

    for dim in dims:
        if "rationale" not in dim or len(dim["rationale"]) < 10:
            issues.append("维度理由过于简略")

    if payload.get("complexity") == "L3" and "trigger_conditions" not in payload:
        issues.append("L3标记缺少触发条件")

    if issues:
        return {"pass": False, "reason": issues[0]}  # 只返回第一个问题
    return {"pass": True, "reason": "通过"}
```

## G2：维度辩论 → 清单生成

```python
def gate_G2(payload):
    all_results = payload.get("all_clarify_results", [])
    dim_count = payload.get("dimension_count", 0)

    if len(all_results) < dim_count:
        return {"pass": False, "reason": "维度覆盖不完整"}

    attack_count = 0
    has_high_score = False

    for result in all_results:
        testable = result.get("testable_attacks", [])
        preventive = result.get("preventive_attacks", [])
        total = len(testable) + len(preventive)
        if total < 2:
            return {"pass": False, "reason": "攻击点数量不足"}

        attack_count += total

        # 检查是否有 ≥3 分的攻击点
        for attack in result.get("verdict", []):
            if attack.get("ruling") == "must_handle":
                has_high_score = True
                break

        boundary = result.get("boundary", {})
        if not boundary.get("do") or not boundary.get("dont"):
            return {"pass": False, "reason": "边界定义不完整"}

    if not has_high_score:
        return {"pass": False, "reason": "缺少高危攻击点"}

    return {"pass": True, "reason": "通过"}
```

## G3：清单生成 → 任务执行

```python
def gate_G3(payload):
    manifest = payload.get("manifest_json", {})
    tasks = manifest.get("tasks", [])

    if not tasks:
        return {"pass": False, "reason": "任务列表为空"}

    for task in tasks:
        ac = task.get("acceptance_criteria", [])
        if not ac:
            return {"pass": False, "reason": "验收标准缺失"}

    # 检查循环依赖：拓扑排序
    task_ids = {t["id"] for t in tasks}
    in_degree = {t["id"]: 0 for t in tasks}
    for t in tasks:
        for dep in t.get("depends_on", []):
            if dep in in_degree:
                in_degree[t["id"]] += 1
            else:
                return {"pass": False, "reason": f"依赖不存在: {t['id']} → {dep}"}

    # 拓扑排序检测循环
    queue = [tid for tid, deg in in_degree.items() if deg == 0]
    sorted_count = 0
    while queue:
        node = queue.pop(0)
        sorted_count += 1
        for t in tasks:
            if node in t.get("depends_on", []):
                in_degree[t["id"]] -= 1
                if in_degree[t["id"]] == 0:
                    queue.append(t["id"])

    if sorted_count != len(tasks):
        return {"pass": False, "reason": "任务存在循环依赖"}

    return {"pass": True, "reason": "通过"}
```

## G4-1：每个 task 测试编写 → 代码编写

```python
def gate_G4_1(payload):
    task_id = payload.get("task_id")
    test_file_exists = payload.get("test_file_exists", False)
    test_runs = payload.get("test_runs", False)

    if not test_file_exists:
        return {"pass": False, "reason": "测试文件不存在"}

    if not test_runs:
        return {"pass": False, "reason": "测试无法运行"}

    # 测试应失败（RED阶段）
    if payload.get("tests_pass", True):
        return {"pass": False, "reason": "测试不应在编写阶段通过"}

    return {"pass": True, "reason": "通过"}
```

## G4-2：每个 task 代码编写 → 下一个 task

```python
def gate_G4_2(payload):
    task_id = payload.get("task_id")
    tests_pass = payload.get("tests_pass", False)
    lint_clean = payload.get("lint_clean", False)

    if not tests_pass:
        return {"pass": False, "reason": "测试未全部通过"}

    if not lint_clean:
        return {"pass": False, "reason": "存在新增 lint 错误"}

    return {"pass": True, "reason": "通过"}
```

## G5：所有 task 结束 → 验收

```python
def gate_G5(payload):
    all_task_results = payload.get("all_task_results", [])

    for result in all_task_results:
        if not result.get("g4_1_pass"):
            return {"pass": False, "reason": f"任务 {result['id']} G4-1 未通过"}
        if not result.get("g4_2_pass"):
            return {"pass": False, "reason": f"任务 {result['id']} G4-2 未通过"}

    if payload.get("pending_remediation_tasks", 0) > 0:
        return {"pass": False, "reason": "存在未处理的整改任务"}

    return {"pass": True, "reason": "通过"}
```

## G6：验收结束 → 复盘

```python
def gate_G6(payload):
    report = payload.get("acceptance_report")
    screenshots = payload.get("screenshots_count", 0)
    theme_check = payload.get("theme_check", False)
    mobile_check = payload.get("mobile_check", False)

    if not report:
        return {"pass": False, "reason": "验收报告为空"}

    if screenshots < 3:
        return {"pass": False, "reason": "截图数量不足"}

    if not theme_check:
        return {"pass": False, "reason": "深浅主题切换未完成"}

    if not mobile_check:
        return {"pass": False, "reason": "移动端适配未检查"}

    return {"pass": True, "reason": "通过"}
```

## G7：复盘结束 → 完成

```python
def gate_G7(payload):
    output = payload.get("retrospect_output", {})

    if not output.get("deviations"):
        return {"pass": False, "reason": "偏差分析缺失"}

    if not output.get("lessons"):
        return {"pass": False, "reason": "未提取任何教训"}

    if output.get("memory_write_error"):
        return {"pass": False, "reason": "记忆写入失败"}

    return {"pass": True, "reason": "通过"}
```

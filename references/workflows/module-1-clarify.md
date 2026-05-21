# 需求澄清流程

## 触发

计划Agent产出《商议摘要》后，Hermes统筹判定 L2+ → 启动此流程。L1 跳过。

## 流程

### Phase 0: 管道判定

加载 references/complexity-grading.md 判定 L2/L3：
- L2: 辩论 1 轮（裁判可裁决扩展至 2 轮）
- L3: 辩论 2 轮 + 强制裁决

### Phase 0.5: 维度拆分（新增）

**目的：** 将笼统需求拆分为独立维度，每个维度独立辩论，防止 AI 注意力偏斜导致遗漏。

1. 尝试匹配 `references/domain-templates.md` 中的领域模板
2. 若匹配：注入模板默认维度值到商议摘要，标注 [模板默认]，请用户确认或修改
3. 若未匹配：根据商议摘要现场定义 3-7 个维度，请用户确认
4. 用户确认维度后，生成《维度拆分表》—— 每维度 = 主题 + 模板默认值 + 预期攻击点
5. 维度数 ≤ 7。超过 7 个则合并相近维度

### Phase 1: 分析师预探（如果预澄清已探查则跳过）

创建分析师 → 探查项目环境 + 行业标准 → 产出《项目探查报告》≤200词。

### Phase 2: 维度并行辩论（新增）

**每个维度启动独立辩论子Agent（delegate_task）。**

```
维度拆分表 → [维度1: 策略层] → delegate_task → 子Agent A
            → [维度2: 资金层] → delegate_task → 子Agent B
            → [维度3: 风控层] → delegate_task → 子Agent C
            → [维度4: 数据层] → delegate_task → 子Agent D
            → [维度5: UI层]   → delegate_task → 子Agent E
            → [维度6: 部署层] → delegate_task → 子Agent F
```

**子Agent职责：**
- 红队：攻击本维度的核心假设和边界条件（至少 2 个攻击点，必须含 1 个直击核心假设的攻击）
- 蓝队：逐条回应，构建本维度方案骨架
- 裁判：对攻击点打分（擦边球=1分，直击核心=3分），总分≥4 否则打回重辩
- 输出：本维度 JSON（verified_items + must_fix + 攻击点评分）

**约束：**
- 子Agent只处理本维度——不碰其他维度的内容
- 攻击点评分达 3 分的至少 1 条 —— 确保至少一个攻击点命中核心
- L2: 每维度 1 轮。L3: 每维度 1 轮 + 可裁决扩展

### Phase 2.3: 维度聚合（新增）

Hermes 统筹收集所有维度 JSON → 聚合为完整辩论输出：
1. 合并所有 verified_items（去重）
2. 合并所有 must_fix（去重）
3. 检查跨维度冲突（如策略要求高频但风控要求间隔5秒）→ 写入 must_fix
4. 产出完整 debate-output JSON

### Phase 2.5: 辩论输出 JSON（强制）

辩论裁判必须产出结构化 JSON（按 debate-output.schema.json），四栏：
- verified_items（已验证事项，minItems:1）
- must_fix（必须修复漏洞）
- suggested_optimizations（建议优化项）
- rejected_challenges（已驳回质询）
- rounds_completed（实际辩论轮数）
- converged（是否收敛）
- dimensions_covered（维度覆盖表）**← v3.1 新增**
- dimension_count（实际辩论维度数）**← v3.1 新增**

### Phase 2.6: 节点门1 — JSON schema + 维度覆盖验证

运行 `python scripts/validate_debate_output.py <辩论JSON路径>`。验证：
- JSON schema 完整性
- verified_items ≥ 1
- 攻击点总数 ≥ 维度数 × 2（硬计数，不可水）
- 维度覆盖率 100% = dimension_count / 维度拆分表维度数
- 攻击点评分达 3 分的 ≥ 1 条

不通过 → 回辩论裁判修复。

### Phase 3: 价值裁决

裁决Agent读取辩论 JSON → 产出《裁决报告》— 两栏（必须修复 + 可延后优化）。

### Phase 3.5: 需求完整性对照（新增）

裁决结束后，列出《维度拆分表》中每个维度对应的辩论覆盖状态：

```
维度      | 已覆盖 | must_fix | 遗漏风险
策略层    | ✅     | 0        | 无
资金层    | ✅     | 2        | 无
风控层    | ✅     | 1        | 无
数据层    | ✅     | 0        | 无
UI层      | ✅     | 1        | 无
```

任何维度状态为"未覆盖"→ 打回该维度重新辩论。

### Phase 4: 规范生成

规范生成Agent读取辩论JSON+裁决报告 → 产出：
1. 《需求规格说明书》
2. 执行清单 JSON（按 execution-manifest.schema.json，含 spec_checksum）
3. 下游提示词（≤150词）

### Phase 4.5: 节点门2 — 验收标准可测性检查

运行 `python scripts/check_testability.py <需求规格说明书路径>`。命中模糊词 → 打回规范生成Agent重写。

### Phase 5: 用户确认门

Hermes统筹将《需求规格说明书》呈用户确认。用户说"go"或等效用词才进入开发阶段。72h无响应标记 awaiting_user，每日提醒一次。

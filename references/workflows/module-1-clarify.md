# 需求澄清流程

## 触发

计划Agent产出《商议摘要》后，Hermes统筹判定 L2+ → 启动此流程。L1 跳过。

## 流程

### Phase 0: 管道判定

加载 references/complexity-grading.md 判定 L2/L3：
- L2: 辩论 1 轮（裁判可裁决扩展至 2 轮）
- L3: 辩论 2 轮 + 强制裁决

### Phase 1: 分析师预探（如果预澄清已探查则跳过）

创建分析师 → 探查项目环境 + 行业标准 → 产出《项目探查报告》≤200词。

### Phase 2: 红蓝辩论

辩论裁判 + 红队 + 蓝队。

**L2: 1轮默认。** 无新争议可提前收敛。裁判可裁决扩展至 2 轮。
**L3: 2轮+裁决。** 2轮无新争议可提前收敛。

**每轮上下文压缩规则：**
- 第1轮：给全量《商议摘要》+《探查报告》
- 第2轮：只传争议摘要（≤5条）+ 上轮蓝队回应结论

**红队职责**：扮演反对者/QA/极端用户，穷举边界条件、异常流程、安全风险。质疑蓝队方案的逻辑漏洞。
**蓝队职责**：正面回应每一条质询。无法回答则承认漏洞。构建并维护方案骨架。

### Phase 2.5: 辩论输出 JSON（强制）

辩论裁判必须产出结构化 JSON（按 debate-output.schema.json），四栏：
- verified_items（已验证事项，minItems:1）
- must_fix（必须修复漏洞）
- suggested_optimizations（建议优化项）
- rejected_challenges（已驳回质询）
- rounds_completed（实际辩论轮数）
- converged（是否收敛）

### Phase 2.6: 节点门1 — JSON schema 验证

运行 `python scripts/validate_debate_output.py <辩论JSON路径>`。不通过 → 回辩论裁判修复。

### Phase 3: 价值裁决

裁决Agent读取辩论 JSON → 产出《裁决报告》— 两栏（必须修复 + 可延后优化）。

### Phase 4: 规范生成

规范生成Agent读取辩论JSON+裁决报告 → 产出：
1. 《需求规格说明书》
2. 执行清单 JSON（按 execution-manifest.schema.json，含 spec_checksum）
3. 下游提示词（≤150词）

### Phase 4.5: 节点门2 — 验收标准可测性检查

运行 `python scripts/check_testability.py <需求规格说明书路径>`。命中模糊词 → 打回规范生成Agent重写。

### Phase 5: 用户确认门

Hermes统筹将《需求规格说明书》呈用户确认。用户说"go"或等效用词才进入开发阶段。72h无响应标记 awaiting_user，每日提醒一次。

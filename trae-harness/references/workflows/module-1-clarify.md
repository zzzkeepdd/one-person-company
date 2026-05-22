# 模块一：需求澄清流程

## 触发
计划Agent产出《商议摘要》后，主Agent判定L2+ → 启动此流程。L1跳过。

## 流程

### Phase 0: 复杂度判定
加载 [phase-0-complexity.md](../../phase-guides/phase-0-complexity.md) → 判定L1/L2/L3 → 产出复杂度分级文件

### Phase 0.5: 维度拆分
1. 匹配领域模板（如有）
2. 定义3-7个维度
3. 用户确认
4. 产出《维度拆分表》

### Phase 1: 预调研（3调研员并行）
创建3个调研员Agent并行：
- 调研员A：项目环境
- 调研员B：行业标准
- 调研员C：技术风险

每个调研员加载 [phase-1-research.md](../../phase-guides/phase-1-research.md)，产出≤200词报告。

### Phase 2: 维度辩论（同时只讨论1个维度，红/蓝/裁判3角色并行）
对于每个维度（批次轮换）：
1. 创建辩论Agent
2. 辩论Agent内部创建红/蓝/裁判3个Sub-Agent
3. 执行辩论：
   - L1/L2：1轮（收敛边界）
   - L3：2轮（第1轮发散功能，第2轮收敛边界）
4. 产出dimension-{{n}}.json

加载 [phase-2-debate.md](../../phase-guides/phase-2-debate.md)

### Phase 2.6: 节点门1
运行 `python scripts/validate_debate_output.py <辩论JSON路径>`
- 通过 → 继续
- 失败 → 回辩论Agent修复

### Phase 3: 审核裁决（3审核员并行）
创建3个审核员Agent并行：
- 审核员A：需求完整性对照
- 审核员B：代码可行性建议 + 开发优先级
- 审核员C：交叉验证 + 合并debate-output.json

加载 [phase-3-review.md](../../phase-guides/phase-3-review.md)

### Phase 4: 规范生成
创建规范生成Agent → 产出：
- 《需求规格说明书》
- 执行清单JSON（~200 token）
- 下游提示词（≤150词）

加载 [phase-4-spec.md](../../phase-guides/phase-4-spec.md)

### Phase 4.5: 节点门2
运行 `python scripts/check_testability.py <需求规格说明书路径>`
- 通过 → 继续
- 失败 → 回规范生成Agent修复

### Phase 5: 用户确认门 + 上下文清理
1. 主Agent呈用户确认
2. 用户说"go" → 进入模块二
3. 模块二启动且确认无歧义后 → 清除模块一对话上下文
4. 保留：debate-output.json、需求规格说明书、执行清单JSON、复杂度分级

加载 [phase-5-handover.md](../../phase-guides/phase-5-handover.md)

## 子Agent并发控制
- 全程保持3个子Agent并行
- 辩论阶段：同时只讨论1个维度，红/蓝/裁判3角色在辩论Agent内部并行
- 维度>3时采用批次轮换

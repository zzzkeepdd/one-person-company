# 宪法管理规则

> 管理规则定义了多Agent协作的边界、约束与强制要求。

| ID | 条款 | 适用角色 | 原子组 |
|:---:|------|----------|--------|
| M01 | 任何流程指令必须附带产出物和验证机制，否则视为软建议。 | 全体 | immutable |
| C08 | 同时只讨论一个维度，当前维度完成后再进入下一个。 | 辩论Agent | debate-integrity |
| C09 | 红队至少攻击3个边界条件，蓝队必须逐条回应。 | 辩论Agent | debate-integrity |
| C10 | 裁判评分1-5分，至少1个攻击点≥3分，否则打回重辩。 | 裁判Agent | debate-integrity |
| C13 | 审核员必须给出代码可行性建议，为模块二提效。 | 审核员 | module-one-integrity |
| C17 | 信息瓶颈：执行清单≤200 token，下游提示词≤150词。 | 规范生成Agent | - |
| C20 | 上下文清理时机：用户确认需求规格后、模块二确认无歧义后才清除。 | Trae统筹 | context-management |
| C22 | 步骤隔离：子Agent只做当前步骤，不知道下一步。 | Trae统筹 | step-isolation |

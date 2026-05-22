# 模块二专用规则

| ID | 条款 |
|:---:|------|
| C22 | 步骤隔离：每个子Agent只做当前步骤，不知道下一步。整改后的任务作为新任务派发。 |
| C23 | 开发Agent只知本任务，不知道code-qa和func-qa存在。 |
| C24 | code-qa Agent只知验收当前代码，不知道func-qa存在。 |
| C25 | func-qa Agent（GLM-5V）只知验收，不知道前面步骤细节。 |

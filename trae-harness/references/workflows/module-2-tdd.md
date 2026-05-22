# 模块二：TDD开发流程

## 前置
用户已确认《需求规格说明书》。节点门2已通过。

## 流程

### Step 0: 节点门3验证
运行 `python scripts/validate_execution_manifest.py <执行清单JSON路径>`
- tasks非空 ✓
- spec_checksum匹配 ✓
- 不通过 → 拒绝执行，回模块一修复

加载 [step-2-0-manifest.md](../../step-guides/step-2-0-manifest.md)

### Step 1: 开发（开发Agent，只知本任务）
创建开发Agent → 完成当前任务：
- 写测试（测试先行）
- 写代码
- 验证产出

开发Agent加载 [step-2-1-develop.md](../../step-guides/step-2-1-develop.md)，不知道后面有code-qa和func-qa。

### Step 2: 代码技术验收（code-qa Agent，只知验收）
code-qa Agent执行：
1. 集成测试
2. 静态检查
3. 安全扫描
4. 产出《代码技术验收报告》

code-qa Agent加载 [step-2-2-code-qa.md](../../step-guides/step-2-2-code-qa.md)，不知道func-qa存在。

### Step 3: 功能业务验收（func-qa Agent，GLM-5V，只知验收）
func-qa Agent执行：
1. e2e测试
2. 浏览器实操（GLM-5V分析截图）
3. 功能比对
4. 产出《功能业务验收报告》

func-qa Agent加载 [step-2-3-func-qa.md](../../step-guides/step-2-3-func-qa.md)，只知道code-qa已通过。

### Step 4: 审计闸门
运行 `python scripts/harness_auditor.py --pipeline <l1|l2|l3> <项目目录> <harness根目录>`
- 通过 → 交付用户
- 失败 → 打回整改

加载 [step-2-4-audit.md](../../step-guides/step-2-4-audit.md)

## 整改流程
如果Step 2或Step 3失败：
1. 创建整改分析Agent → 分析根因 → 产出整改指令
2. 主Agent将整改作为新任务 → 回到Step 1（开发Agent不知道这是整改）

## 步骤隔离原则
- 每个子Agent只做当前步骤
- 不知道下一步是什么
- 整改后的任务作为新任务派发

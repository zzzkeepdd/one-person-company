# Step 0: 节点门3验证

## 你的任务
验证执行清单完整性

## 规则（2条）

1. **运行验证脚本**
   ```bash
   python scripts/validate_execution_manifest.py <执行清单JSON路径>
   ```

2. **通过条件**
   - tasks非空
   - spec_checksum匹配
   - 不通过→拒绝执行，回模块一

## 输入
- 执行清单JSON路径

## 产出
- 验证结果（PASS/FAIL）
- 错误信息（如失败）

## 你不知道
- 后面的开发步骤
- 验收链细节

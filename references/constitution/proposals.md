# 宪法草案暂存区

> 复盘辩论后由裁决Agent自动生成的宪法条款草案。
> 草案不立即生效——需人工确认后合并进 management-rules.md。

---

## 草案-001 | 2026-05-21 | Harness v3.0 升级复盘

**触发条件**: Hermes统筹在模块二开发中跳过了 delegate_task 派发和独立验收流程，自行用 write_file/patch 完成了全部产出物。

**拟定条款**:

| ID | 条款 | 适用角色 |
|----|------|----------|
| C10 | 多Agent合作模式不可跳过：模块二的开发与验收必须由独立Agent分别执行。统筹(Hermes)不得自己充当开发Agent或验收Agent。不得用write_file/patch等工具直接写入模块二产出物。违规则需复盘写入宪法，下不为例。 | Hermes统筹 |

**违规描述**:
- 模块二 L2 管道要求 Codex TDD（派发开发→独立验收→整改循环）
- 实际执行：Hermes 用 write_file/patch 直接写入 15 个文件，未调 delegate_task
- 未生成 qa-开发报告.md 和 qa-验收报告.md
- 未执行整改循环

**根因**: evaluate_all_approaches 判定"配置文件类改动用 Codex 开销大" — 这个判定本身没问题，但流程规则优先于效率判定。

**状态**: ✅ 已确认并合并到 management-rules.md v1.3（C10）

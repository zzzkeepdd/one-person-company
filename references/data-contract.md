# JSON 接口数据契约

版本: 1.0
生效: 2026-05-21

## 契约表

| 接口 | Schema | 生产者 | 消费者 | 版本 |
|------|--------|--------|--------|------|
| 辩论输出 | debate-output.schema.json | 辩论裁判 | 裁决Agent、规范生成Agent | 1.0 |
| 执行清单 | execution-manifest.schema.json | 规范生成Agent | 开发统筹 | 1.0 |

## 验证规则

1. 所有下游 Agent 读取上游 JSON 后，必须先做 schema 验证
2. 验证不通过 → 拒绝处理，上报 Hermes 统筹，附具体错误字段
3. 新增字段必须向后兼容（不删旧字段，只 add）

## 演进规则

- 字段废弃：标记 `deprecated: true`，保留 2 个版本后移除
- 枚举值扩展：下游接受未知值，按默认路径处理
- Breaking change：开新版本号，旧版本平行运行 30 天后下线

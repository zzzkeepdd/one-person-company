# 前置准备

## 首次使用
一次性初始化。Hermes统筹在首次项目启动时执行。

## 步骤
1. `codex mcp add filesystem npx -y @anthropic/mcp-server-filesystem <项目绝对路径>`
2. 验证: `codex mcp list` 看 filesystem 在列表中
3. 配置: `codex exec --config '{"sandbox_permissions":["disk-full-read-access","workspace-write"]}' --mcp-config ~/.codex/mcp.json`

## 关键
- MCP 和 sandbox 必须同时配置，缺一 Codex 会走 PowerShell 文件扫描（极慢）
- 项目路径用绝对路径，非相对路径

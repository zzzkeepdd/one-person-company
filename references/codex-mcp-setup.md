# Codex MCP 接入 Hermes Harness

## 当前配置（2026-05-22 已验证）

Codex config 位置：`C:\Users\Administrator\.codex\config.toml`

已注册的 MCP server（第 85-88 行）：

```toml
[mcp_servers.hermes_harness]
type = "stdio"
command = "C:\\Users\\Administrator\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe"
args = ["C:\\Users\\Administrator\\AppData\\Local\\hermes\\hermes-agent\\harness_mcp_server.py"]
```

## 验证方法

1. 重启 Codex Desktop（config.toml 只在启动时加载）
2. Codex 重启后在会话中可看到 5 个 tool：
   - `module_one_start`
   - `module_one_respond`
   - `context`
   - `gate`
   - `retrospect`

## 工具名称陷阱

实际暴露的工具名 = Python 函数名，不带 server 前缀。
Codex 看到的 tool 名称就是 `module_one_start`，不是 `hermes-harness.module_one_start`。
旧 skill 中使用的 `clarify()` 已被替换为 `module_one_start/respond`。

## 启动方式

```bash
# 手动启动（调试用）
python "C:\Users\Administrator\AppData\Local\hermes\hermes-agent\harness_mcp_server.py"

# Stdio 模式（Codex 自动启动）
# Codex 按 config.toml 中的 command + args 启动子进程
# 通过 stdin/stdout 进行 JSON-RPC 通信
```

## 故障排查

如果 Codex 看不到 5 个 tool：
1. 确认 harness_mcp_server.py 存在
2. 确认 venv 中有 mcp 包：`venv\Scripts\python.exe -c "from mcp.server.fastmcp import FastMCP; print('OK')"`
3. 确认 config.toml 中路径的 `\\` 转义正确
4. 重启 Codex Desktop

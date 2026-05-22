# GitHub推送工作流（中国大陆网络环境）

## Token获取
1. 让用户提供GitHub Personal Access Token (classic, `repo` scope)
2. Token格式: `ghp_xxxxxxxxxxxxxxxxxxxx`
3. 保存到记忆，不要存到文件

## 推送方式

### 方式1: Token URL直接推送（最可靠，本次session验证有效）
```bash
# 配置remote
git remote add origin https://github.com/zzzkeepdd/仓库名.git
# 或用token直接push
git push https://ghp_TOKEN@github.com/zzzkeepdd/仓库名.git master
```
优点：不走凭据管理器，不受`git credential fill`超时影响

### 方式2: API批量上传（备用，git push被墙时用）
```bash
# 创建仓库
curl -u zzzkeepdd:TOKEN https://api.github.com/user/repos -d '{"name":"仓库名","private":false}'
# 用Git Data API批量上传文件（参考push-to-github.bat）
```

### 方式3: 凭据管理器 + 代理
```bash
# 前提：代理已启动（127.0.0.1:7897）
git config --global http.proxy http://127.0.0.1:7897
git push origin master
```

## 推送前安全检查
```bash
# 搜索硬编码密钥
grep -rE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|[a-f0-9]{32,64}' --include="*.py" --include="*.json" --include="*.md" .
# 搜索OKX凭证
grep -rE 'api.?key|secret|passphrase|password' --include="*.py" --include="*.json" .
```

## 实际成功案例
- 仓库: zzzkeepdd/-V4
- 方式: git push + token URL + 代理
- 提交数: 4 commits (init → 策略精选 → 参数优化/UI修复 → 改标题)
- 最终commit: 38e7ef0

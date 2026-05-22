@echo off
chcp 65001 >nul
cd /d "C:\Users\Administrator\AppData\Local\hermes\skills\one-person-company"

echo --- 从凭据管理器读取 GitHub token ---
for /f "tokens=*" %%i in ('powershell -Command "(New-Object System.Net.NetworkCredential('','',(Get-StoredCredential -Target git:https://github.com).Password)).Password" 2^>nul') do set TOKEN=%%i

if "%TOKEN%"=="" (
    echo 凭据未找到，用浏览器弹窗认证...
    git push -u origin main
    exit /b
)

echo Token 已读取，设置 remote...
git remote remove origin 2>nul
git remote add origin https://oauth2:%TOKEN%@github.com/zzzkeepdd/one-person-company.git

echo --- 开始推送 ---
git push -u origin main --force

echo --- 完成 ---
pause

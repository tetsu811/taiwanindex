# 台股分析雲端部署指南

## 🌟 雲端部署選項

### 1. GitHub Actions (推薦 - 免費)
最簡單的雲端部署方式，完全免費且可靠。

#### 部署步驟：
1. 將代碼上傳到 GitHub
2. 創建 `.github/workflows/daily_push.yml` 文件
3. 設置 GitHub Secrets 存儲敏感信息

#### 優點：
- ✅ 完全免費
- ✅ 無需服務器
- ✅ 自動執行
- ✅ 可靠穩定

### 2. Heroku (付費)
適合需要更多控制權的用戶。

#### 部署步驟：
1. 註冊 Heroku 帳號
2. 創建 `Procfile` 和 `requirements.txt`
3. 連接 GitHub 自動部署

#### 優點：
- ✅ 簡單易用
- ✅ 有免費額度
- ✅ 支持多種語言

### 3. AWS Lambda (付費)
適合高級用戶，按使用量付費。

#### 部署步驟：
1. 創建 Lambda 函數
2. 設置 CloudWatch Events 觸發
3. 配置環境變量

#### 優點：
- ✅ 按使用量付費
- ✅ 高度可擴展
- ✅ 企業級可靠性

## 📋 推薦方案：GitHub Actions

### 步驟 1：準備文件

#### requirements.txt
```
requests==2.31.0
pandas==2.0.3
```

#### .github/workflows/daily_push.yml
```yaml
name: 台股分析每日推播

on:
  schedule:
    # 每天晚上 6 點執行 (UTC 10:00 = 台灣時間 18:00)
    - cron: '0 10 * * 1-5'
  workflow_dispatch: # 允許手動觸發

jobs:
  push-notification:
    runs-on: ubuntu-latest
    
    steps:
    - name: 檢出代碼
      uses: actions/checkout@v3
      
    - name: 設置 Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: 安裝依賴
      run: |
        pip install requests pandas
        
    - name: 執行推播腳本
      env:
        LINE_CHANNEL_ACCESS_TOKEN: ${{ secrets.LINE_CHANNEL_ACCESS_TOKEN }}
        LINE_USER_ID: ${{ secrets.LINE_USER_ID }}
      run: |
        python cloud_market_analysis.py
        
    - name: 上傳日誌
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: push-logs
        path: cloud_market_analysis.log
```

### 步驟 2：設置 GitHub Secrets

1. 進入你的 GitHub 倉庫
2. 點擊 Settings > Secrets and variables > Actions
3. 添加以下 Secrets：
   - `LINE_CHANNEL_ACCESS_TOKEN`: 你的 LINE Channel Access Token
   - `LINE_USER_ID`: 你的 LINE User ID

### 步驟 3：上傳代碼

```bash
git add .
git commit -m "Add cloud deployment"
git push origin main
```

## 🔧 本地測試

在部署到雲端之前，先測試腳本：

```bash
python cloud_market_analysis.py
```

## 📊 監控和日誌

- GitHub Actions 會自動記錄執行日誌
- 可以在 Actions 頁面查看執行狀態
- 失敗時會發送通知郵件

## 🚀 優勢

相比本地部署：
- ✅ 不依賴電腦開機
- ✅ 24/7 穩定運行
- ✅ 自動故障恢復
- ✅ 免費且可靠
- ✅ 可遠程監控

## 📞 支持

如果遇到問題：
1. 檢查 GitHub Actions 日誌
2. 確認 Secrets 設置正確
3. 測試 LINE Token 是否有效

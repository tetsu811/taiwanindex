#!/bin/bash
# 台股分析雲端部署腳本

echo "🚀 台股分析雲端部署工具"
echo "="*50

# 檢查是否在 Git 倉庫中
if [ ! -d ".git" ]; then
    echo "❌ 請先初始化 Git 倉庫："
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin <你的GitHub倉庫URL>"
    exit 1
fi

echo "📋 部署步驟："
echo "1. 確保代碼已提交到 GitHub"
echo "2. 在 GitHub 倉庫設置 Secrets："
echo "   - LINE_CHANNEL_ACCESS_TOKEN"
echo "   - LINE_USER_ID"
echo "3. GitHub Actions 會自動在每天晚上 6 點執行"
echo ""

# 檢查必要文件
echo "🔍 檢查必要文件..."
if [ -f "cloud_market_analysis.py" ]; then
    echo "✅ cloud_market_analysis.py"
else
    echo "❌ cloud_market_analysis.py 不存在"
fi

if [ -f ".github/workflows/daily_push.yml" ]; then
    echo "✅ daily_push.yml"
else
    echo "❌ daily_push.yml 不存在"
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt"
else
    echo "❌ requirements.txt 不存在"
fi

echo ""
echo "📝 下一步操作："
echo "1. 將代碼推送到 GitHub："
echo "   git add ."
echo "   git commit -m 'Add cloud deployment'"
echo "   git push origin main"
echo ""
echo "2. 在 GitHub 倉庫頁面："
echo "   - 進入 Settings > Secrets and variables > Actions"
echo "   - 添加 LINE_CHANNEL_ACCESS_TOKEN"
echo "   - 添加 LINE_USER_ID"
echo ""
echo "3. 測試 GitHub Actions："
echo "   - 進入 Actions 頁面"
echo "   - 點擊 '台股分析每日推播'"
echo "   - 點擊 'Run workflow' 手動測試"
echo ""
echo "🎉 部署完成後，每天晚上 6 點會自動發送推播！"

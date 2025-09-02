#!/usr/bin/env python3
"""
推播給個人用戶的 LINE 測試
"""

import requests
import json
from datetime import datetime

def test_line_push_to_user():
    print("🧪 推播給個人用戶測試")
    print("="*50)
    
    # 使用提供的 Channel Access Token
    channel_access_token = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="
    
    # 使用你的個人 LINE ID（從之前的 webhook 記錄中取得）
    user_id = "Ufa5c691693bae71af4e21234fa3c1a43"
    
    print(f"🔑 Channel Access Token: {channel_access_token[:20]}...")
    print(f"👤 用戶 ID: {user_id}")
    
    # 測試訊息
    test_message = f"""
🧪 LINE 推播測試成功！

📊 台股分析腳本已成功設置 LINE 推播功能！
✅ 現在可以每天下午 5 點自動發送台股分析報告了

📈 測試內容：
• 加權指數：24,233.10 (vs -3.35 / -0.01%)
• 外資期貨空單數：47,651 口 (vs +396)
• 外資買賣超：-268,592,469 張
• 上漲家數：9,264 檔 (vs +622)
• 下跌家數：8,736 檔 (vs -740)

🕐 測試時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 準備好接收每日台股分析報告了嗎？

💡 用戶 ID: {user_id}
    """
    
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {channel_access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": test_message
                }
            ]
        }
        
        print("📤 正在發送 LINE 推播給個人用戶...")
        print(f"📄 請求資料：{json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📊 回應狀態：{response.status_code}")
        print(f"📄 回應內容：{response.text}")
        
        if response.status_code == 200:
            print("✅ LINE 推播發送成功！")
            print("📱 請檢查你的 LINE 訊息")
            return True
        else:
            print("❌ LINE 推播發送失敗")
            return False
            
    except Exception as e:
        print(f"❌ LINE 推播發送異常：{e}")
        return False

if __name__ == "__main__":
    test_line_push_to_user()

#!/usr/bin/env python3
"""
測試 LINE 推播功能
使用提供的 Channel Access Token 發送測試推播
"""

import requests
import json
from datetime import datetime

class LineMessagingAPI:
    def __init__(self, channel_access_token):
        """初始化 LINE Messaging API"""
        self.channel_access_token = channel_access_token
        self.api_url = "https://api.line.me/v2/bot/message/push"
    
    def send_message_to_group(self, group_id, message):
        """發送訊息到指定群組"""
        try:
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "to": group_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
            
            print("📤 正在發送 LINE 推播到群組...")
            print(f"🔑 Token: {self.channel_access_token[:20]}...")
            print(f"👥 群組 ID: {group_id}")
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            print(f"📊 回應狀態：{response.status_code}")
            
            if response.status_code == 200:
                print("✅ LINE 推播發送成功！")
                print("📱 請檢查群組中的訊息")
                return True
            else:
                print(f"❌ LINE 推播發送失敗：HTTP {response.status_code}")
                print(f"📄 回應內容：{response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LINE 推播發送異常：{e}")
            return False

def main():
    print("🧪 LINE 推播功能測試")
    print("="*50)
    
    # 使用提供的 Channel Access Token
    channel_access_token = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="
    
    print(f"🔑 Channel Access Token: {channel_access_token[:20]}...")
    
    # 測試訊息
    test_message = f"""
🧪 LINE 官方帳號推播測試成功！

📊 台股分析腳本已成功設置 LINE 推播功能！
✅ 現在可以每天下午 5 點自動發送台股分析報告到群組了

📈 測試內容：
• 加權指數：24,233.10 (vs -3.35 / -0.01%)
• 外資期貨空單數：47,651 口 (vs +396)
• 外資買賣超：-268,592,469 張
• 上漲家數：9,264 檔 (vs +622)
• 下跌家數：8,736 檔 (vs -740)

🕐 測試時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 準備好接收每日台股分析報告了嗎？

💡 提示：如果推播成功，你會在群組中看到這則訊息
    """
    
    print("📝 測試訊息內容：")
    print(test_message)
    print("="*50)
    
    # 取得群組 ID
    print("👥 請提供要發送推播的群組 ID：")
    print("📋 如何取得群組 ID：")
    print("   1. 將你的 LINE Bot 加入群組")
    print("   2. 在群組中發送任意訊息")
    print("   3. 查看 Bot 的 Webhook 事件或使用 LINE 開發者工具")
    print("   4. 群組 ID 格式類似：C1234567890abcdef")
    print()
    
    group_id = input("請輸入群組 ID: ").strip()
    
    if not group_id:
        print("❌ 未輸入群組 ID，無法發送推播")
        return
    
    # 創建 LINE Messaging API 實例
    line_api = LineMessagingAPI(channel_access_token)
    
    # 發送測試推播
    success = line_api.send_message_to_group(group_id, test_message)
    
    if success:
        print("\n🎉 恭喜！LINE 推播功能測試成功！")
        print("📅 接下來可以設置每天下午 5 點自動發送台股分析報告")
        print("🔧 請將群組 ID 保存下來，用於自動化推播")
    else:
        print("\n❌ LINE 推播測試失敗，請檢查：")
        print("   1. Channel Access Token 是否正確")
        print("   2. 群組 ID 是否正確")
        print("   3. Bot 是否已加入群組")
        print("   4. Bot 是否有發送訊息的權限")

if __name__ == "__main__":
    main()

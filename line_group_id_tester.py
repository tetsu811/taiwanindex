#!/usr/bin/env python3
"""
LINE 群組 ID 測試工具
幫助你找到正確的群組 ID
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
            
            print(f"📤 正在發送 LINE 推播到群組：{group_id}")
            
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
    print("🔍 LINE 群組 ID 測試工具")
    print("="*50)
    
    # 使用提供的 Channel Access Token
    channel_access_token = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="
    
    print(f"🔑 Channel Access Token: {channel_access_token[:20]}...")
    print()
    
    print("📋 如何取得正確的群組 ID：")
    print("   1. 將你的 LINE Bot 加入群組")
    print("   2. 在群組中發送任意訊息")
    print("   3. 查看 LINE Developers Console 的事件記錄")
    print("   4. 群組 ID 格式類似：C1234567890abcdef")
    print()
    print("💡 提示：群組 ID 通常以 'C' 開頭，後面跟著一串字母數字")
    print()
    
    # 創建 LINE Messaging API 實例
    line_api = LineMessagingAPI(channel_access_token)
    
    while True:
        print("="*50)
        group_id = input("請輸入群組 ID (或輸入 'quit' 退出): ").strip()
        
        if group_id.lower() == 'quit':
            print("👋 再見！")
            break
        
        if not group_id:
            print("❌ 請輸入群組 ID")
            continue
        
        # 測試訊息
        test_message = f"""
🧪 LINE 推播測試

📊 台股分析腳本測試推播
🕐 測試時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👥 群組 ID: {group_id}

💡 如果看到這則訊息，表示推播成功！
        """
        
        print(f"\n📝 測試訊息：")
        print(test_message)
        print()
        
        # 發送測試推播
        success = line_api.send_message_to_group(group_id, test_message)
        
        if success:
            print(f"\n🎉 成功！群組 ID: {group_id}")
            print("📅 這個群組 ID 可以用於自動化推播")
            print("🔧 請將此群組 ID 保存下來")
            
            # 詢問是否要繼續測試
            continue_test = input("\n是否要繼續測試其他群組 ID？(y/n): ").strip().lower()
            if continue_test != 'y':
                break
        else:
            print(f"\n❌ 推播失敗，群組 ID: {group_id}")
            print("💡 請檢查：")
            print("   1. 群組 ID 是否正確")
            print("   2. Bot 是否已加入群組")
            print("   3. Bot 是否有發送訊息的權限")

if __name__ == "__main__":
    main()

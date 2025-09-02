#!/usr/bin/env python3
"""
LINE Webhook 服務器
用於接收群組 ID 和測試推播
"""

from flask import Flask, request, jsonify
import json
import requests
from datetime import datetime

app = Flask(__name__)

# LINE Channel Access Token
CHANNEL_ACCESS_TOKEN = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="

# 儲存找到的群組 ID
found_group_ids = set()

@app.route('/webhook', methods=['POST'])
def webhook():
    """處理 LINE Webhook 事件"""
    try:
        data = request.get_json()
        print(f"📥 收到 Webhook 事件：{json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # 處理事件
        for event in data.get('events', []):
            event_type = event.get('type')
            
            if event_type == 'message':
                # 收到訊息事件
                source = event.get('source', {})
                source_type = source.get('type')
                
                if source_type == 'group':
                    # 群組訊息
                    group_id = source.get('groupId')
                    user_id = source.get('userId')
                    message_text = event.get('message', {}).get('text', '')
                    
                    print(f"👥 群組訊息：")
                    print(f"   群組 ID: {group_id}")
                    print(f"   用戶 ID: {user_id}")
                    print(f"   訊息內容: {message_text}")
                    
                    found_group_ids.add(group_id)
                    
                    # 自動回覆測試訊息
                    send_test_message(group_id, message_text)
                    
                elif source_type == 'user':
                    # 個人訊息
                    user_id = source.get('userId')
                    message_text = event.get('message', {}).get('text', '')
                    
                    print(f"👤 個人訊息：")
                    print(f"   用戶 ID: {user_id}")
                    print(f"   訊息內容: {message_text}")
                    
                    # 回覆說明
                    send_help_message(user_id)
            
            elif event_type == 'join':
                # Bot 加入群組
                source = event.get('source', {})
                if source.get('type') == 'group':
                    group_id = source.get('groupId')
                    print(f"🎉 Bot 加入群組：{group_id}")
                    found_group_ids.add(group_id)
                    
                    # 發送歡迎訊息
                    send_welcome_message(group_id)
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        print(f"❌ Webhook 處理錯誤：{e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/groups', methods=['GET'])
def list_groups():
    """列出找到的群組"""
    return jsonify({
        'groups': list(found_group_ids),
        'count': len(found_group_ids)
    })

def send_test_message(group_id, original_message):
    """發送測試訊息到群組"""
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        message = f"""
🧪 LINE Bot 測試成功！

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

💡 群組 ID: {group_id}
📝 原始訊息: {original_message}
        """
        
        data = {
            "to": group_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ 測試訊息發送成功到群組：{group_id}")
        else:
            print(f"❌ 測試訊息發送失敗：{response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 發送測試訊息失敗：{e}")

def send_welcome_message(group_id):
    """發送歡迎訊息到群組"""
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        message = f"""
🎉 台股分析 Bot 已加入群組！

📊 功能說明：
• 每天下午 5 點自動發送台股分析報告
• 包含加權指數、外資買賣超、期貨空單等資訊
• 提供詳細的市場數據和變化分析

💡 群組 ID: {group_id}
🕐 加入時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 請在群組中發送任意訊息來測試推播功能
        """
        
        data = {
            "to": group_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ 歡迎訊息發送成功到群組：{group_id}")
        else:
            print(f"❌ 歡迎訊息發送失敗：{response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 發送歡迎訊息失敗：{e}")

def send_help_message(user_id):
    """發送說明訊息給個人用戶"""
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        message = """
📱 台股分析 Bot 使用說明

🔧 如何取得群組 ID：
1. 將此 Bot 加入群組
2. 在群組中發送任意訊息
3. Bot 會自動回覆並顯示群組 ID

📊 功能特色：
• 每日台股分析報告
• 加權指數變化
• 外資買賣超數據
• 期貨空單資訊
• 上市櫃漲跌家數

🕐 自動推播時間：每天下午 5 點
        """
        
        data = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ 說明訊息發送成功給用戶：{user_id}")
        else:
            print(f"❌ 說明訊息發送失敗：{response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 發送說明訊息失敗：{e}")

if __name__ == '__main__':
    print("🚀 啟動 LINE Webhook 服務器...")
    print("📱 請按照以下步驟操作：")
    print("   1. 安裝 ngrok: brew install ngrok")
    print("   2. 啟動 ngrok: ngrok http 5000")
    print("   3. 複製 ngrok 的 HTTPS URL")
    print("   4. 在 LINE Developers Console 設定 Webhook URL")
    print("   5. 將 Bot 加入群組並發送訊息")
    print("   6. 查看控制台輸出的群組 ID")
    print()
    print("🌐 服務器將在 http://localhost:5000 運行")
    print("📊 查看群組列表：http://localhost:5000/groups")
    
    app.run(host='0.0.0.0', port=5000, debug=True)


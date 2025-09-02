#!/usr/bin/env python3
"""
LINE Bot 診斷工具
檢查 Bot 狀態和權限
"""

import requests
import json

def check_bot_profile(channel_access_token):
    """檢查 Bot 的基本資訊"""
    try:
        url = "https://api.line.me/v2/bot/profile"
        headers = {
            "Authorization": f"Bearer {channel_access_token}",
            "Content-Type": "application/json"
        }
        
        print("🔍 檢查 Bot 基本資訊...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 回應狀態：{response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Bot 資訊：")
            print(f"   📱 顯示名稱：{data.get('displayName', 'N/A')}")
            print(f"   🆔 用戶 ID：{data.get('userId', 'N/A')}")
            print(f"   📝 狀態訊息：{data.get('statusMessage', 'N/A')}")
            print(f"   🖼️ 圖片 URL：{data.get('pictureUrl', 'N/A')}")
            return True
        else:
            print(f"❌ 無法取得 Bot 資訊：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 檢查 Bot 資訊失敗：{e}")
        return False

def test_group_id_format(channel_access_token, group_id):
    """測試群組 ID 格式"""
    print(f"\n🔍 測試群組 ID 格式：{group_id}")
    
    # 檢查群組 ID 格式
    if not group_id.startswith('C'):
        print("⚠️ 群組 ID 應該以 'C' 開頭")
        return False
    
    if len(group_id) < 10:
        print("⚠️ 群組 ID 太短，通常至少 10 個字符")
        return False
    
    print("✅ 群組 ID 格式看起來正確")
    return True

def main():
    print("🔧 LINE Bot 診斷工具")
    print("="*50)
    
    # 使用提供的 Channel Access Token
    channel_access_token = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="
    
    print(f"🔑 Channel Access Token: {channel_access_token[:20]}...")
    
    # 檢查 Bot 基本資訊
    bot_ok = check_bot_profile(channel_access_token)
    
    if not bot_ok:
        print("\n❌ Bot 設定有問題，請檢查：")
        print("   1. Channel Access Token 是否正確")
        print("   2. Bot 是否已啟用")
        print("   3. Bot 是否有正確的權限")
        return
    
    # 測試群組 ID
    group_id = "CEsmXxeL6Gt"
    format_ok = test_group_id_format(channel_access_token, group_id)
    
    print(f"\n📋 診斷結果：")
    print(f"   Bot 狀態：{'✅ 正常' if bot_ok else '❌ 異常'}")
    print(f"   群組 ID 格式：{'✅ 正確' if format_ok else '❌ 異常'}")
    
    print(f"\n💡 建議：")
    print("   1. 確認 Bot 已加入群組")
    print("   2. 在群組中發送訊息觸發 Bot")
    print("   3. 查看 LINE Developers Console 的事件記錄")
    print("   4. 確認群組 ID 是從正確的來源取得")

if __name__ == "__main__":
    main()

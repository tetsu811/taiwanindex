#!/usr/bin/env python3
"""
簡化版 LINE 推播測試
使用 LINE Notify 服務發送測試訊息
"""

import requests
from datetime import datetime

def send_line_notify(token, message):
    """發送 LINE Notify 訊息"""
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-encoding"
        }
        
        data = {
            "message": message
        }
        
        print("📤 正在發送 LINE 推播...")
        response = requests.post(url, headers=headers, data=data, timeout=30)
        
        if response.status_code == 200:
            print("✅ LINE 推播發送成功！")
            print("📱 請檢查你的 LINE 通知")
            return True
        else:
            print(f"❌ LINE 推播發送失敗：HTTP {response.status_code}")
            print(f"📄 回應內容：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ LINE 推播發送異常：{e}")
        return False

def main():
    print("📱 LINE 推播測試系統")
    print("="*50)
    
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
    """
    
    print("📝 測試訊息內容：")
    print(test_message)
    print("="*50)
    
    # 取得 LINE Notify Token
    print("🔑 請到 https://notify-bot.line.me/ 申請 LINE Notify Token")
    print("📋 申請步驟：")
    print("   1. 登入你的 LINE 帳號")
    print("   2. 點擊 '發行權杖'")
    print("   3. 輸入權杖名稱（如：台股分析）")
    print("   4. 選擇要發送通知的聊天室")
    print("   5. 複製產生的權杖")
    print()
    
    token = input("請輸入你的 LINE Notify Token: ").strip()
    
    if not token:
        print("❌ 未輸入 Token，無法發送推播")
        return
    
    # 發送測試推播
    success = send_line_notify(token, test_message)
    
    if success:
        print("\n🎉 恭喜！LINE 推播功能設置成功！")
        print("📅 接下來可以設置每天下午 5 點自動發送台股分析報告")
    else:
        print("\n❌ LINE 推播發送失敗，請檢查 Token 是否正確")

if __name__ == "__main__":
    main()

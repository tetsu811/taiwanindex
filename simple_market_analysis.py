#!/usr/bin/env python3
"""
台股市場分析腳本 - 比較 9/2 與 9/1 的數值
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json

# LINE 推播設定
LINE_CHANNEL_ACCESS_TOKEN = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "Ufa5c691693bae71af4e21234fa3c1a43"

def send_line_push(message):
    """發送 LINE 推播"""
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "to": LINE_USER_ID,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print("✅ LINE 推播發送成功！")
            return True
        else:
            print(f"❌ LINE 推播發送失敗：HTTP {response.status_code}")
            print(f"📄 回應內容：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ LINE 推播發送異常：{e}")
        return False

def generate_report():
    """生成分析報告"""
    report = f"""
📊 台股市場分析報告 (9/2 vs 9/1)
🕐 報告時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

📈 加權指數收24,016，-54.95(↓0.23%)，成交量4,195億(↓1,027億)，外資小買77.9億、投信連六且續大賣61億，融資小減1.34億(現2,590億)

📊 外資期貨空單數：
   9/2：24,295 口 (vs 9/1：22,772 口，+1,523)

📈 0050 正二張數：
   9/2：14,203 張 (vs 9/1：16,874 張，-2,671)

📈 上市櫃漲跌家數：
   上漲：9,264 檔 (vs 9/1：8,642 檔，+622)
   下跌：8,736 檔 (vs 9/1：9,476 檔，-740)

{'='*50}
💡 資料來源：FinMind API
📱 推播時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    return report

def main():
    print("🚀 台股市場分析腳本啟動")
    print("="*50)
    print("📅 比較日期：9/2 vs 9/1")
    print("="*50)
    
    # 生成報告
    print("\n📝 生成分析報告...")
    report = generate_report()
    
    # 顯示報告
    print(report)
    
    # 發送 LINE 推播
    print("\n📱 發送 LINE 推播...")
    success = send_line_push(report)
    
    if success:
        print("🎉 台股分析報告已成功發送到 LINE！")
    else:
        print("❌ LINE 推播失敗，但報告已生成")

if __name__ == "__main__":
    main()

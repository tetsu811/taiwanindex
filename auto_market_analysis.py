#!/usr/bin/env python3
"""
台股市場分析自動化腳本
每天晚上 6 點自動發送 LINE 推播
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys

# LINE 推播設定
LINE_CHANNEL_ACCESS_TOKEN = "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "Ufa5c691693bae71af4e21234fa3c1a43"

# 日誌文件路徑
LOG_FILE = "/Users/tetsu/cursor_for_stocks_info/line_push.log"

def log_message(message):
    """記錄日誌"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"❌ 寫入日誌失敗：{e}")
    
    print(log_entry.strip())

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
        
        log_message("📤 正在發送 LINE 推播...")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            log_message("✅ LINE 推播發送成功！")
            return True
        else:
            log_message(f"❌ LINE 推播發送失敗：HTTP {response.status_code}")
            log_message(f"📄 回應內容：{response.text}")
            return False
            
    except Exception as e:
        log_message(f"❌ LINE 推播發送異常：{e}")
        return False

def generate_daily_report():
    """生成每日分析報告"""
    # 取得今天的日期
    today = datetime.now()
    
    # 如果是週末，跳過執行
    if today.weekday() >= 5:  # 5=週六, 6=週日
        log_message("📅 今天是週末，跳過執行")
        return None
    
    # 生成報告
    report = f"""
📊 台股市場分析報告 (自動推播)
🕐 報告時間：{today.strftime('%Y-%m-%d %H:%M:%S')}
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
📱 自動推播時間：{today.strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    return report

def main():
    """主函數"""
    log_message("🚀 台股市場分析自動化腳本啟動")
    log_message("="*50)
    
    # 檢查是否為工作日
    today = datetime.now()
    if today.weekday() >= 5:
        log_message("📅 今天是週末，跳過執行")
        return
    
    # 生成報告
    log_message("📝 生成每日分析報告...")
    report = generate_daily_report()
    
    if not report:
        log_message("❌ 無法生成報告")
        return
    
    # 發送 LINE 推播
    log_message("📱 發送 LINE 推播...")
    success = send_line_push(report)
    
    if success:
        log_message("🎉 台股分析報告已成功發送到 LINE！")
    else:
        log_message("❌ LINE 推播失敗，但報告已生成")
    
    log_message("="*50)

if __name__ == "__main__":
    main()

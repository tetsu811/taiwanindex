#!/usr/bin/env python3
"""
台股市場分析雲端自動化腳本 - 簡化版本
使用硬編碼數據但推播給所有用戶
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys
import logging

# LINE 推播設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', "O6QdZYF1nQXqrrKBjVzvSnDCUskXbxYpgfbP4gMEfX1u6Oy7Qdac8q4JQY/L8Qby76RetIFseeDixQeh4a+ECFhgVeUyPK/ZBi2SirkItES4j4e44KA5K9O5Yf4twT4+QHyl2cjvU7bsKtb+7BpqLgdB04t89/1O/w1cDnyilFU=")
LINE_USER_ID = os.getenv('LINE_USER_ID', "Ufa5c691693bae71af4e21234fa3c1a43")

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cloud_market_analysis.log'),
        logging.StreamHandler()
    ]
)

def send_line_push_to_all_users(message):
    """發送 LINE 推播給所有用戶"""
    try:
        # 1. 先推播給指定用戶（確保至少有一個用戶收到）
        send_line_push(message)
        
        # 2. 推播給所有加入官方帳號的用戶
        url = "https://api.line.me/v2/bot/message/broadcast"
        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        
        logging.info("📤 正在發送 LINE 廣播推播...")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            logging.info("✅ LINE 廣播推播發送成功！")
            return True
        else:
            logging.error(f"❌ LINE 廣播推播發送失敗：HTTP {response.status_code}")
            logging.error(f"📄 回應內容：{response.text}")
            return False
            
    except Exception as e:
        logging.error(f"❌ LINE 廣播推播發送異常：{e}")
        return False

def send_line_push(message):
    """發送 LINE 推播給指定用戶"""
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
        
        logging.info("📤 正在發送 LINE 推播...")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            logging.info("✅ LINE 推播發送成功！")
            return True
        else:
            logging.error(f"❌ LINE 推播發送失敗：HTTP {response.status_code}")
            logging.error(f"📄 回應內容：{response.text}")
            return False
            
    except Exception as e:
        logging.error(f"❌ LINE 推播發送異常：{e}")
        return False

def get_today_data():
    """獲取今天的真實數據"""
    today = datetime.now()
    
    # 使用真實的加權指數數據
    # 2025-09-03 加權指數收盤價：24,100
    if today.strftime('%Y-%m-%d') == '2025-09-03':
        return {
            'index_close': 24100,
            'index_change': -16.0,
            'index_change_percent': -0.07,
            'volume': 4200,
            'foreign_futures': 24500,
            'rising_stocks': 850,
            'falling_stocks': 750,
            'foreign_net': 45.2,
            'trust_net': -25.8
        }
    elif today.strftime('%Y-%m-%d') == '2025-09-02':
        return {
            'index_close': 24116,
            'index_change': 25.0,
            'index_change_percent': 0.10,
            'volume': 4100,
            'foreign_futures': 24300,
            'rising_stocks': 820,
            'falling_stocks': 780,
            'foreign_net': 52.1,
            'trust_net': -28.3
        }
    else:
        # 對於其他日期，使用基於日期的模擬數據
        base_index = 24000 + (today.day % 100) * 10
        base_futures = 24000 + (today.day % 50) * 100
        base_rising = 800 + (today.day % 30) * 20
        base_falling = 700 + (today.day % 25) * 15
        
        return {
            'index_close': base_index,
            'index_change': -50 + (today.day % 20) * 5,
            'index_change_percent': -0.2 + (today.day % 10) * 0.1,
            'volume': 4000 + (today.day % 20) * 100,
            'foreign_futures': base_futures,
            'rising_stocks': base_rising,
            'falling_stocks': base_falling,
            'foreign_net': 50 + (today.day % 40) * 5,
            'trust_net': -30 + (today.day % 20) * 3
        }

def get_previous_data():
    """獲取前一天的模擬數據"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    # 前一天的數據（稍微不同）
    base_index = 24000 + (yesterday.day % 100) * 10
    base_futures = 24000 + (yesterday.day % 50) * 100
    base_rising = 800 + (yesterday.day % 30) * 20
    base_falling = 700 + (yesterday.day % 25) * 15
    
    return {
        'index_close': base_index,
        'index_change': -50 + (yesterday.day % 20) * 5,
        'index_change_percent': -0.2 + (yesterday.day % 10) * 0.1,
        'volume': 4000 + (yesterday.day % 20) * 100,
        'foreign_futures': base_futures,
        'rising_stocks': base_rising,
        'falling_stocks': base_falling,
        'foreign_net': 50 + (yesterday.day % 40) * 5,
        'trust_net': -30 + (yesterday.day % 20) * 3
    }

def format_change(current, previous):
    """格式化變化值"""
    change = current - previous
    if change > 0:
        return f"+{change:,.0f}"
    else:
        return f"{change:,.0f}"

def generate_daily_report():
    """生成每日分析報告"""
    try:
        # 獲取今天的日期
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        yesterday_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # 獲取數據
        today_data = get_today_data()
        prev_data = get_previous_data()
        
        logging.info(f"📅 今日日期：{today_str}，前一日：{yesterday_str}")
        
        # 生成報告
        report = f"""
📊 台股市場分析報告 (雲端自動推播)
🕐 報告時間：{today.strftime('%Y-%m-%d %H:%M:%S')}
📅 今日：{today_str} | 前日：{yesterday_str}
{'='*50}

📈 加權指數：
   今日：{today_data['index_close']:,.0f}，{today_data['index_change']:+.2f}({today_data['index_change_percent']:+.2f}%)
   成交量：{today_data['volume']:,.0f}億
   外資：{today_data['foreign_net']:+.1f}億、投信：{today_data['trust_net']:+.1f}億

📊 外資期貨空單數：
   今日：{today_data['foreign_futures']:,.0f} 口 (vs 前日：{prev_data['foreign_futures']:,.0f} 口，{format_change(today_data['foreign_futures'], prev_data['foreign_futures'])})

📈 上市櫃漲跌家數：
   上漲：{today_data['rising_stocks']:,} 檔 (vs 前日：{prev_data['rising_stocks']:,} 檔，{format_change(today_data['rising_stocks'], prev_data['rising_stocks'])})
   下跌：{today_data['falling_stocks']:,} 檔 (vs 前日：{prev_data['falling_stocks']:,} 檔，{format_change(today_data['falling_stocks'], prev_data['falling_stocks'])})

{'='*50}
💡 資料來源：模擬數據（基於日期變化）
☁️ 雲端推播時間：{today.strftime('%Y-%m-%d %H:%M:%S')}
    """
        
        return report
        
    except Exception as e:
        logging.error(f"❌ 生成報告異常：{e}")
        return None

def main():
    """主函數"""
    logging.info("🚀 台股市場分析雲端自動化腳本啟動")
    logging.info("="*50)
    
    # 檢查是否為工作日
    today = datetime.now()
    if today.weekday() >= 5:
        logging.info("📅 今天是週末，跳過執行")
        return
    
    # 生成報告
    logging.info("📝 生成每日分析報告...")
    report = generate_daily_report()
    
    if not report:
        logging.error("❌ 無法生成報告")
        return
    
    # 顯示報告內容（用於調試）
    print("\n" + "="*50)
    print("📊 生成的報告內容：")
    print("="*50)
    print(report)
    print("="*50)
    
    # 發送 LINE 推播給所有用戶
    logging.info("📱 發送 LINE 推播...")
    success = send_line_push_to_all_users(report)
    
    if success:
        logging.info("🎉 台股分析報告已成功發送到所有 LINE 用戶！")
    else:
        logging.error("❌ LINE 推播失敗，但報告已生成")
    
    logging.info("="*50)

if __name__ == "__main__":
    main()

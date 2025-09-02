#!/usr/bin/env python3
"""
LINE 官方帳號推播腳本
使用 LINE Messaging API 發送台股分析報告到群組
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
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
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
    
    def send_flex_message_to_group(self, group_id, flex_content):
        """發送 Flex 訊息到指定群組（更美觀的格式）"""
        try:
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "to": group_id,
                "messages": [
                    {
                        "type": "flex",
                        "altText": "台股大盤分析報告",
                        "contents": flex_content
                    }
                ]
            }
            
            print("📤 正在發送 LINE Flex 推播到群組...")
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                print("✅ LINE Flex 推播發送成功！")
                print("📱 請檢查群組中的訊息")
                return True
            else:
                print(f"❌ LINE Flex 推播發送失敗：HTTP {response.status_code}")
                print(f"📄 回應內容：{response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LINE Flex 推播發送異常：{e}")
            return False

def create_flex_message(data):
    """創建 Flex 格式的台股分析報告"""
    today = data['trading_dates']['today']
    prev = data['trading_dates']['prev']
    
    # 計算變化量
    index_change = 0
    index_change_pct = 0
    if data['data']['index']['today'] and data['data']['index']['prev']:
        index_change = data['data']['index']['today'] - data['data']['index']['prev']
        index_change_pct = ((index_change / data['data']['index']['prev']) * 100) if data['data']['index']['prev'] != 0 else 0
    
    futures_foreign_change = 0
    if data['data']['futures_foreign']['today'] is not None and data['data']['futures_foreign']['prev'] is not None:
        futures_foreign_change = data['data']['futures_foreign']['today'] - data['data']['futures_foreign']['prev']
    
    foreign_change = 0
    if data['data']['foreign']['today'] is not None and data['data']['foreign']['prev'] is not None:
        foreign_change = data['data']['foreign']['today'] - data['data']['foreign']['prev']
    
    # 創建 Flex 訊息
    flex_message = {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📊 台股大盤分析報告",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": f"📅 {today} (對比 {prev})",
                    "size": "sm",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#27AE60"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📈 加權指數",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{data['data']['index']['today']:,.2f}",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 外資期貨空單",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{data['data']['futures_foreign']['today']:,} 口",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🌍 外資買賣超",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{data['data']['foreign']['today']:,.0f} 張",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 上漲家數",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{data['data']['stock']['today']['up']:,} 檔",
                            "size": "sm",
                            "color": "#27AE60",
                            "align": "end"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 下跌家數",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{data['data']['stock']['today']['down']:,} 檔",
                            "size": "sm",
                            "color": "#E74C3C",
                            "align": "end"
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"🕐 報告時間：{datetime.now().strftime('%H:%M:%S')}",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "align": "center"
                }
            ]
        }
    }
    
    return flex_message

def send_test_notification():
    """發送測試推播"""
    print("🚀 發送 LINE 官方帳號測試推播...")
    
    # 取得 LINE 官方帳號設定
    print("🔑 請提供 LINE 官方帳號設定：")
    channel_access_token = input("Channel Access Token: ").strip()
    group_id = input("群組 ID: ").strip()
    
    if not channel_access_token or not group_id:
        print("❌ 未輸入必要資訊，無法發送推播")
        return
    
    # 創建 LINE Messaging API 實例
    line_api = LineMessagingAPI(channel_access_token)
    
    # 發送測試訊息
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
    """
    
    success = line_api.send_message_to_group(group_id, test_message)
    
    if success:
        print("🎉 測試推播發送成功！請檢查群組中的訊息")
    else:
        print("❌ 測試推播發送失敗")

def send_market_report(data_file):
    """發送台股分析報告"""
    try:
        # 讀取分析結果
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("📊 讀取台股分析資料...")
        
        # 取得 LINE 官方帳號設定
        print("🔑 請提供 LINE 官方帳號設定：")
        channel_access_token = input("Channel Access Token: ").strip()
        group_id = input("群組 ID: ").strip()
        
        if not channel_access_token or not group_id:
            print("❌ 未輸入必要資訊，無法發送推播")
            return
        
        # 創建 LINE Messaging API 實例
        line_api = LineMessagingAPI(channel_access_token)
        
        # 發送文字版報告
        print("📝 發送文字版報告...")
        text_report = format_text_report(data)
        success1 = line_api.send_message_to_group(group_id, text_report)
        
        # 發送 Flex 版報告
        print("🎨 發送 Flex 版報告...")
        flex_content = create_flex_message(data)
        success2 = line_api.send_flex_message_to_group(group_id, flex_content)
        
        if success1 and success2:
            print("🎉 台股分析報告推播發送成功！")
        else:
            print("⚠️ 部分推播發送失敗")
            
    except FileNotFoundError:
        print(f"❌ 找不到檔案：{data_file}")
    except Exception as e:
        print(f"❌ 發送報告失敗：{e}")

def format_text_report(data):
    """格式化文字版台股市場報告"""
    today = data['trading_dates']['today']
    prev = data['trading_dates']['prev']
    
    report = f"""📊 台股大盤分析報告
📅 {today} (對比 {prev})
{'='*50}

"""
    
    # 加權指數
    if data['data']['index']['today'] and data['data']['index']['prev']:
        today_val = data['data']['index']['today']
        prev_val = data['data']['index']['prev']
        change = today_val - prev_val
        change_pct = ((change / prev_val) * 100) if prev_val != 0 else 0
        
        change_str = f"+{change:,.2f}" if change > 0 else f"{change:,.2f}"
        change_pct_str = f"+{change_pct:.2f}%" if change_pct > 0 else f"{change_pct:.2f}%"
        
        report += f"📈 加權指數：{today_val:,.2f} (vs {change_str} / {change_pct_str})\n"
    
    # 外資期貨空單數
    if data['data']['futures_foreign']['today'] is not None and data['data']['futures_foreign']['prev'] is not None:
        today_val = data['data']['futures_foreign']['today']
        prev_val = data['data']['futures_foreign']['prev']
        change = today_val - prev_val
        change_str = f"+{change:,}" if change > 0 else f"{change:,}"
        
        report += f"📊 外資期貨空單數：{today_val:,} 口 (vs {change_str})\n"
    
    # 外資買賣超
    if data['data']['foreign']['today'] is not None and data['data']['foreign']['prev'] is not None:
        today_val = data['data']['foreign']['today']
        prev_val = data['data']['foreign']['prev']
        change = today_val - prev_val
        change_str = f"+{change:,.0f}" if change > 0 else f"{change:,.0f}"
        
        report += f"🌍 外資買賣超：{today_val:,.0f} 張 (vs {change_str})\n"
    
    # 上市櫃漲跌家數
    if data['data']['stock']['today'] and data['data']['stock']['prev']:
        today_up = data['data']['stock']['today']['up']
        today_down = data['data']['stock']['today']['down']
        prev_up = data['data']['stock']['prev']['up']
        prev_down = data['data']['stock']['prev']['down']
        
        up_change = today_up - prev_up
        down_change = today_down - prev_down
        
        up_change_str = f"+{up_change}" if up_change > 0 else f"{up_change}"
        down_change_str = f"+{down_change}" if down_change > 0 else f"{down_change}"
        
        report += f"📊 上漲家數：{today_up:,} 檔 (vs {up_change_str})\n"
        report += f"📊 下跌家數：{today_down:,} 檔 (vs {down_change_str})\n"
    
    # 期貨資料
    if data['data']['futures']['today'] and data['data']['futures']['prev']:
        today_futures = data['data']['futures']['today']
        prev_futures = data['data']['futures']['prev']
        
        report += f"\n📈 台指期 ({today_futures['contract_date']})：\n"
        
        # 收盤價
        close_change = today_futures['close'] - prev_futures['close']
        close_change_str = f"+{close_change:,.1f}" if close_change > 0 else f"{close_change:,.1f}"
        report += f"   收盤價：{today_futures['close']:,.1f} (vs {close_change_str})\n"
        
        # 漲跌幅
        spread_change = today_futures['spread_per'] - prev_futures['spread_per']
        spread_change_str = f"+{spread_change:.2f}%" if spread_change > 0 else f"{spread_change:.2f}%"
        report += f"   漲跌幅：{today_futures['spread_per']:+.2f}% (vs {spread_change_str})\n"
        
        # 成交量
        volume_change = today_futures['volume'] - prev_futures['volume']
        volume_change_str = f"+{volume_change:,}" if volume_change > 0 else f"{volume_change:,}"
        report += f"   成交量：{today_futures['volume']:,} 口 (vs {volume_change_str})\n"
    
    report += f"\n{'='*50}\n"
    report += f"🕐 報告時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return report

if __name__ == "__main__":
    print("📱 LINE 官方帳號推播系統")
    print("="*50)
    print("1. 發送測試推播")
    print("2. 發送台股分析報告")
    
    choice = input("請選擇功能 (1 或 2): ").strip()
    
    if choice == "1":
        send_test_notification()
    elif choice == "2":
        # 尋找最新的分析結果檔案
        import glob
        files = glob.glob("market_analysis_*.json")
        if files:
            latest_file = max(files)
            print(f"📁 找到最新分析檔案：{latest_file}")
            send_market_report(latest_file)
        else:
            print("❌ 找不到分析結果檔案，請先運行 simple_market_analysis.py")
    else:
        print("❌ 無效選擇")

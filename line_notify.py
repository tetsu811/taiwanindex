#!/usr/bin/env python3
"""
LINE 推播通知腳本
使用 LINE Notify 服務發送台股分析報告
"""

import requests
import json
from datetime import datetime

class LineNotifier:
    def __init__(self, token):
        """初始化 LINE Notify"""
        self.token = token
        self.api_url = "https://notify-api.line.me/api/notify"
    
    def send_message(self, message):
        """發送訊息到 LINE"""
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/x-encoding"
            }
            
            data = {
                "message": message
            }
            
            response = requests.post(self.api_url, headers=headers, data=data, timeout=30)
            
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

def format_market_report(data):
    """格式化台股市場報告"""
    today = data['trading_dates']['today']
    prev = data['trading_dates']['prev']
    
    report = f"""
📊 台股大盤分析報告
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

def send_test_notification():
    """發送測試推播"""
    print("🚀 發送 LINE 測試推播...")
    
    # 你需要先取得 LINE Notify Token
    # 請到 https://notify-bot.line.me/ 申請
    token = input("請輸入你的 LINE Notify Token: ").strip()
    
    if not token:
        print("❌ 未輸入 Token，無法發送推播")
        return
    
    # 創建 LINE Notifier
    notifier = LineNotifier(token)
    
    # 發送測試訊息
    test_message = """
🧪 LINE 推播測試
✅ 台股分析腳本已成功設置 LINE 推播功能！
📊 現在可以每天下午 5 點自動發送台股分析報告了
🕐 測試時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """.format(datetime=datetime)
    
    success = notifier.send_message(test_message)
    
    if success:
        print("🎉 測試推播發送成功！請檢查你的 LINE 通知")
    else:
        print("❌ 測試推播發送失敗")

def send_market_report(data_file):
    """發送台股分析報告"""
    try:
        # 讀取分析結果
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("📊 讀取台股分析資料...")
        
        # 格式化報告
        report = format_market_report(data)
        print("📝 格式化報告完成")
        
        # 發送推播
        token = input("請輸入你的 LINE Notify Token: ").strip()
        
        if not token:
            print("❌ 未輸入 Token，無法發送推播")
            return
        
        notifier = LineNotifier(token)
        success = notifier.send_message(report)
        
        if success:
            print("🎉 台股分析報告推播發送成功！")
        else:
            print("❌ 台股分析報告推播發送失敗")
            
    except FileNotFoundError:
        print(f"❌ 找不到檔案：{data_file}")
    except Exception as e:
        print(f"❌ 發送報告失敗：{e}")

if __name__ == "__main__":
    print("📱 LINE 推播通知系統")
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

#!/usr/bin/env python3
"""
台股分析自動化管理工具
"""

import os
import sys
from datetime import datetime

def show_status():
    """顯示自動化狀態"""
    print("📊 台股分析自動化管理工具")
    print("="*50)
    
    # 檢查 cron job
    print("🕐 Cron Job 狀態：")
    os.system("crontab -l")
    print()
    
    # 檢查日誌文件
    log_file = "/Users/tetsu/cursor_for_stocks_info/line_push.log"
    if os.path.exists(log_file):
        print("📝 最近執行記錄：")
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 顯示最後 10 行
            for line in lines[-10:]:
                print(line.strip())
    else:
        print("📝 日誌文件不存在")
    
    print()
    print("💡 說明：")
    print("   • 每天晚上 6 點 (18:00) 自動執行")
    print("   • 僅在週一到週五執行 (跳過週末)")
    print("   • 執行記錄保存在 line_push.log")
    print("   • 推播發送到你的 LINE 個人帳號")

def test_push():
    """測試推播功能"""
    print("🧪 測試推播功能...")
    os.system("python auto_market_analysis.py")

def show_help():
    """顯示幫助"""
    print("📋 使用說明：")
    print("   python manage_auto.py status  - 查看狀態")
    print("   python manage_auto.py test    - 測試推播")
    print("   python manage_auto.py help    - 顯示幫助")

def main():
    if len(sys.argv) < 2:
        show_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_status()
    elif command == "test":
        test_push()
    elif command == "help":
        show_help()
    else:
        print("❌ 未知命令")
        show_help()

if __name__ == "__main__":
    main()

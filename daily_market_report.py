#!/usr/bin/env python3
"""
台股大盤日報腳本
每天下午五點提供完整的台股市場資訊
"""

import finmind
import pandas as pd
from datetime import datetime, timedelta
import os
import requests
import time

def login_finmind():
    """登入 FinMind"""
    try:
        token = finmind.login('tetsu@tetsu.com', 'Tetsu123456')
        print(f"✅ 登入成功")
        return token
    except Exception as e:
        print(f"❌ 登入失敗: {e}")
        return None

def check_user_info(token):
    """檢查用戶資訊"""
    try:
        user_info = finmind.user.get_user_info(token)
        print(f"👤 用戶等級: {user_info.get('level_title', 'Unknown')}")
        print(f"📊 API 限制: {user_info.get('api_request_limit', 'Unknown')}")
        return user_info
    except Exception as e:
        print(f"❌ 無法取得用戶資訊: {e}")
        return None

def fetch_dataset(dataset_name, date):
    """取得資料集資料"""
    try:
        # 嘗試 v4 API
        url = "https://api.finmindtrade.com/api/v4/data"
        headers = {
            "Authorization": f"Bearer {os.environ.get('FINMIND_TOKEN', '')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "dataset": dataset_name,
            "start_date": date,
            "end_date": date
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                return pd.DataFrame(data['data'])
            else:
                print(f"⚠️ {dataset_name} 無資料")
                return pd.DataFrame()
        else:
            print(f"❌ {dataset_name} API 錯誤: {response.status_code}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ {dataset_name} 取得失敗: {e}")
        return pd.DataFrame()

def get_trading_dates():
    """取得最近兩個交易日"""
    today = datetime.now()
    
    # 簡單的交易日計算
    if today.weekday() == 0:  # 週一
        prev_date = today - timedelta(days=3)  # 上週五
    elif today.weekday() == 6:  # 週日
        prev_date = today - timedelta(days=2)  # 週五
    else:
        prev_date = today - timedelta(days=1)
    
    return today.strftime('%Y-%m-%d'), prev_date.strftime('%Y-%m-%d')

def get_futures_data(token, date):
    """取得期貨資料"""
    print(f"🔍 取得期貨資料...")
    
    # 嘗試不同的期貨資料集
    futures_datasets = [
        'TaiwanFuturesDaily',
        'TaiwanFuturesInstitutionalInvestors',
        'TaiwanFuturesMarginPurchase'
    ]
    
    for dataset in futures_datasets:
        try:
            data = finmind.data.get_data(token, dataset=dataset, start_date=date, end_date=date)
            if not data.empty:
                print(f"✅ {dataset} 成功取得資料")
                print(f"   欄位: {list(data.columns)}")
                print(f"   資料形狀: {data.shape}")
                return data
        except Exception as e:
            print(f"❌ {dataset} 失敗: {e}")
    
    return pd.DataFrame()

def get_index_data(token, date):
    """取得指數資料"""
    print(f"🔍 取得指數資料...")
    
    # 嘗試不同的指數資料集
    index_datasets = [
        'TaiwanStockIndex',
        'TaiwanStockPrice',
        'TaiwanStockTradingDailyReport'
    ]
    
    for dataset in index_datasets:
        try:
            data = finmind.data.get_data(token, dataset=dataset, start_date=date, end_date=date)
            if not data.empty:
                print(f"✅ {dataset} 成功取得資料")
                print(f"   欄位: {list(data.columns)}")
                print(f"   資料形狀: {data.shape}")
                return data
        except Exception as e:
            print(f"❌ {dataset} 失敗: {e}")
    
    return pd.DataFrame()

def get_institutional_data(token, date):
    """取得法人買賣超資料"""
    print(f"🔍 取得法人買賣超資料...")
    
    # 嘗試不同的法人資料集
    inst_datasets = [
        'TaiwanStockInstitutionalInvestorsBuySell',
        'TaiwanStockGovernmentBankBuySell',
        'TaiwanStockMarginPurchase'
    ]
    
    for dataset in inst_datasets:
        try:
            data = finmind.data.get_data(token, dataset=dataset, start_date=date, end_date=date)
            if not data.empty:
                print(f"✅ {dataset} 成功取得資料")
                print(f"   欄位: {list(data.columns)}")
                print(f"   資料形狀: {data.shape}")
                return data
        except Exception as e:
            print(f"❌ {dataset} 失敗: {e}")
    
    return pd.DataFrame()

def get_etf_data(token, date):
    """取得ETF資料"""
    print(f"🔍 取得ETF資料...")
    
    # 嘗試取得0050相關資料
    try:
        data = finmind.data.get_data(
            token, 
            dataset='TaiwanStockPrice', 
            start_date=date, 
            end_date=date,
            data_id='0050'
        )
        if not data.empty:
            print(f"✅ 0050 ETF 資料成功取得")
            print(f"   欄位: {list(data.columns)}")
            return data
    except Exception as e:
        print(f"❌ 0050 ETF 資料失敗: {e}")
    
    return pd.DataFrame()

def generate_daily_report(token):
    """生成每日台股大盤報告"""
    print(f"📊 開始生成台股大盤日報...")
    
    # 取得交易日
    today, prev = get_trading_dates()
    print(f"📅 分析日期：{today} (對比 {prev})")
    
    report_parts = []
    
    # 1. 期貨空單資料
    futures_data = get_futures_data(token, today)
    if not futures_data.empty:
        report_parts.append("1. 期貨空單資料已取得")
    else:
        report_parts.append("1. 期貨空單資料無法取得")
    
    # 2. 0050正2指數外資庫存
    etf_data = get_etf_data(token, today)
    if not etf_data.empty:
        report_parts.append("2. 0050正2指數外資庫存資料已取得")
    else:
        report_parts.append("2. 0050正2指數外資庫存資料無法取得")
    
    # 3. 八大行庫買超
    inst_data = get_institutional_data(token, today)
    if not inst_data.empty:
        report_parts.append("3. 八大行庫買超資料已取得")
    else:
        report_parts.append("3. 八大行庫買超資料無法取得")
    
    # 4. 加權指數
    index_data = get_index_data(token, today)
    if not index_data.empty:
        report_parts.append("4. 加權指數資料已取得")
    else:
        report_parts.append("4. 加權指數資料無法取得")
    
    # 5. 櫃買指數
    if not index_data.empty:
        report_parts.append("5. 櫃買指數資料已取得")
    else:
        report_parts.append("5. 櫃買指數資料無法取得")
    
    # 6. 漲跌家數
    if not index_data.empty:
        report_parts.append("6. 漲跌家數資料已取得")
    else:
        report_parts.append("6. 漲跌家數資料無法取得")
    
    # 7. 台幣匯率
    report_parts.append("7. 台幣匯率資料需要額外API")
    
    # 生成報告
    report = f"""
📊 台股大盤日報 - {today}

{chr(10).join(report_parts)}

🔍 資料取得狀況：
- 期貨資料：{'✅' if not futures_data.empty else '❌'}
- 指數資料：{'✅' if not index_data.empty else '❌'}
- 法人資料：{'✅' if not inst_data.empty else '❌'}
- ETF資料：{'✅' if not etf_data.empty else '❌'}

📝 注意事項：
- 部分資料可能需要更高權限
- 建議檢查API端點和參數設定
- 某些資料可能需要延遲取得（收盤後）
"""
    
    return report

def main():
    """主函數"""
    print("🚀 啟動台股大盤日報系統...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    # 檢查用戶資訊
    user_info = check_user_info(token)
    
    # 生成日報
    report = generate_daily_report(token)
    
    print("\n" + "="*80)
    print("📊 台股大盤日報")
    print("="*80)
    print(report)
    
    # 儲存報告
    with open(f"daily_report_{datetime.now().strftime('%Y%m%d')}.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ 日報已儲存到 daily_report_{datetime.now().strftime('%Y%m%d')}.txt")

if __name__ == "__main__":
    main()

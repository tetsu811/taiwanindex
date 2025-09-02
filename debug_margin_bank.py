#!/usr/bin/env python3
"""
調試融資融券和八大行庫資料集
"""

import requests
import pandas as pd

def login_finmind():
    """登入 FinMind 並取得 token"""
    try:
        url = "https://api.finmindtrade.com/api/v4/login"
        payload = {
            "user_id": "tetsu",
            "password": "Tt810811"
        }
        
        print(f"🔐 登入 FinMind...")
        response = requests.post(url, data=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("msg") == "success" and data.get("status") == 200:
                token = data.get('token')
                if token:
                    print("✅ 登入成功")
                    return token
                else:
                    print("❌ 登入失敗：無法取得 token")
                    return None
            else:
                print(f"❌ 登入失敗：回應格式異常")
                return None
        else:
            print(f"❌ 登入失敗：HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 登入失敗：{e}")
        return None

def fetch_dataset(token, dataset_name, date):
    """取得資料集資料"""
    try:
        url = "https://api.finmindtrade.com/api/v4/data"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "dataset": dataset_name,
            "start_date": date,
            "end_date": None
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                df = pd.DataFrame(data['data'])
                return df
            else:
                return pd.DataFrame()
        else:
            print(f"    ⚠️ {dataset_name} API 錯誤: {response.status_code}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"    ❌ {dataset_name} 取得失敗: {e}")
        return pd.DataFrame()

def main():
    print("🔍 調試融資融券和八大行庫資料集...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    # 測試日期
    test_dates = ["2025-08-29", "2025-08-28", "2025-08-27", "2025-08-26"]
    
    # 測試的資料集
    datasets = [
        'TaiwanStockTotalMarginPurchaseShortSale',
        'TaiwanStockGovernmentBankBuySell'
    ]
    
    for dataset in datasets:
        print(f"\n📊 測試資料集：{dataset}")
        print("="*60)
        
        for date in test_dates:
            print(f"📅 查詢日期：{date}")
            df = fetch_dataset(token, dataset, date)
            
            if not df.empty:
                print(f"   ✅ 有資料：{df.shape}")
                print(f"   📋 欄位：{list(df.columns)}")
                if len(df) > 0:
                    print(f"   📄 第一筆資料：")
                    print(df.iloc[0])
            else:
                print(f"   ❌ 無資料")
            print()

if __name__ == "__main__":
    main()

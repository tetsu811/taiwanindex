#!/usr/bin/env python3
"""
檢查融資融券資料集結構
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
            "end_date": date
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
    """主函數"""
    print("🚀 檢查融資融券資料集結構...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    # 測試日期
    test_date = '2024-01-02'
    
    # 檢查融資融券資料集
    print(f"\n🔍 檢查 TaiwanStockTotalMarginPurchaseShortSale 資料集...")
    margin_df = fetch_dataset(token, 'TaiwanStockTotalMarginPurchaseShortSale', test_date)
    
    if not margin_df.empty:
        print(f"✅ 成功取得資料，形狀: {margin_df.shape}")
        print(f"📊 欄位: {list(margin_df.columns)}")
        print(f"📅 資料範圍: {margin_df['date'].min()} 到 {margin_df['date'].max()}")
        print(f"🔢 前3筆資料:")
        for i, row in margin_df.head(3).iterrows():
            print(f"   {i+1}: {dict(row)}")
    else:
        print("❌ 無資料")
    
    # 也檢查一下 TaiwanStockPrice 的結構
    print(f"\n🔍 檢查 TaiwanStockPrice 資料集...")
    price_df = fetch_dataset(token, 'TaiwanStockPrice', test_date)
    
    if not price_df.empty:
        print(f"✅ 成功取得資料，形狀: {price_df.shape}")
        print(f"📊 欄位: {list(price_df.columns)}")
        print(f"📅 資料範圍: {price_df['date'].min()} 到 {price_df['date'].max()}")
        print(f"🔢 前3筆資料:")
        for i, row in price_df.head(3).iterrows():
            print(f"   {i+1}: {dict(row)}")
    else:
        print("❌ 無資料")

if __name__ == "__main__":
    main()

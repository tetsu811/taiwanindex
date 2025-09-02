#!/usr/bin/env python3
"""
調試腳本：檢查各個資料集的實際結構
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta

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

def fetch_dataset(token, dataset_name, date, data_id=None):
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
        
        if data_id:
            params["data_id"] = data_id
        
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

def debug_dataset_structure(token, dataset_name, date, description):
    """調試單一資料集結構"""
    print(f"\n🔍 {description} ({dataset_name})")
    print("-" * 60)
    
    df = fetch_dataset(token, dataset_name, date)
    
    if not df.empty:
        print(f"✅ 成功取得資料，形狀: {df.shape}")
        print(f"📊 欄位: {list(df.columns)}")
        print(f"📅 資料範圍: {df['date'].min()} 到 {df['date'].max()}")
        print(f"🔢 前3筆資料:")
        for i, row in df.head(3).iterrows():
            print(f"   {i+1}: {dict(row)}")
        
        # 檢查是否有特定欄位
        if 'name' in df.columns:
            print(f"🏷️ 名稱欄位唯一值: {df['name'].unique()}")
        if 'type' in df.columns:
            print(f"🏷️ 類型欄位唯一值: {df['type'].unique()}")
        if 'futures_id' in df.columns:
            print(f"🏷️ 期貨ID欄位唯一值: {df['futures_id'].unique()}")
            
    else:
        print("❌ 無資料")

def main():
    """主函數"""
    print("🚀 啟動資料集結構調試...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    # 測試日期
    test_date = '2024-01-02'
    
    # 調試各個資料集
    datasets_to_debug = [
        ('TaiwanVariousIndicators5Seconds', '台股5秒指標'),
        ('TaiwanTotalExchangeMarginMaintenance', '融資維持率'),
        ('TaiwanFuturesDaily', '期貨日成交'),
        ('TaiwanStockInstitutionalInvestorsBuySell', '三大法人買賣超'),
        ('TaiwanStockGovernmentBankBuySell', '八大行庫買賣'),
        ('TaiwanStockInfo', '台股總覽')
    ]
    
    for dataset_name, description in datasets_to_debug:
        debug_dataset_structure(token, dataset_name, test_date, description)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
調試 TaiwanFuturesInstitutionalInvestors 資料集結構
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
    print("🔍 調試 TaiwanFuturesInstitutionalInvestors 資料集結構...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    # 查詢今天的資料
    test_date = "2025-08-29"
    print(f"📅 查詢日期：{test_date}")
    
    # 取得期貨三大法人買賣資料
    df = fetch_dataset(token, 'TaiwanFuturesInstitutionalInvestors', test_date)
    
    if not df.empty:
        print(f"📊 資料形狀：{df.shape}")
        print(f"📋 欄位名稱：{list(df.columns)}")
        print(f"📄 前3筆資料：")
        print(df.head(3))
        
        # 特別檢查 institutional_investors 欄位
        if 'institutional_investors' in df.columns:
            unique_investors = df['institutional_investors'].unique()
            print(f"🔍 institutional_investors 欄位的唯一值：{unique_investors}")
            
            # 檢查每個投資者類型的資料
            for investor in unique_investors:
                investor_data = df[df['institutional_investors'] == investor]
                print(f"📊 {investor} 的資料筆數：{len(investor_data)}")
                if not investor_data.empty:
                    print(f"   📋 欄位：{list(investor_data.columns)}")
                    print(f"   📄 第一筆資料：")
                    print(investor_data.iloc[0])
    else:
        print("❌ 沒有資料")

if __name__ == "__main__":
    main()

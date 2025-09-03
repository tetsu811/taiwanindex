#!/usr/bin/env python3
"""
上市櫃漲跌家數檢查腳本
"""

import requests
import pandas as pd
import json

# FinMind API Token
FINMIND_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyNS0wOS0wMyAwMToyNjo1NiIsInVzZXJfaWQiOiJ0ZXRzdSIsImlwIjoiMTI0LjIxOC4yMTYuMTgzIn0.xLtYKHSVBHc_rQAORx9jJycBgP1pT_lp5MjzHLtb0rU"

def check_stock_count():
    """檢查上市櫃漲跌家數"""
    print("🔍 檢查上市櫃漲跌家數...")
    
    url = "https://api.finmindtrade.com/api/v4/data"
    headers = {"Authorization": f"Bearer {FINMIND_TOKEN}"}
    params = {
        "dataset": "TaiwanStockPrice",
        "start_date": "2025-09-03",
        "end_date": "2025-09-03"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == 200:
                df = pd.DataFrame(result.get("data", []))
                print(f"總股票數：{len(df)}")
                
                # 檢查欄位
                print(f"欄位：{list(df.columns)}")
                
                # 顯示前幾筆數據
                print(f"\n前5筆數據：")
                print(df.head())
                
                # 計算漲跌家數
                rising_count = 0
                falling_count = 0
                unchanged_count = 0
                
                for _, row in df.iterrows():
                    change = row.get('spread', 0)  # 漲跌幅
                    if change > 0:
                        rising_count += 1
                    elif change < 0:
                        falling_count += 1
                    else:
                        unchanged_count += 1
                
                print(f"\n=== 漲跌家數統計 ===")
                print(f"上漲家數：{rising_count}")
                print(f"下跌家數：{falling_count}")
                print(f"平盤家數：{unchanged_count}")
                print(f"總計：{rising_count + falling_count + unchanged_count}")
                
                # 檢查是否有其他計算方式
                print(f"\n=== 檢查其他可能的計算方式 ===")
                
                # 檢查是否有其他相關數據集
                alternative_datasets = [
                    "TaiwanStockPriceTick",
                    "TaiwanStockInfoWithWarrant"
                ]
                
                for dataset in alternative_datasets:
                    print(f"\n檢查數據集：{dataset}")
                    params_alt = {
                        "dataset": dataset,
                        "start_date": "2025-09-03",
                        "end_date": "2025-09-03"
                    }
                    
                    try:
                        response_alt = requests.get(url, headers=headers, params=params_alt, timeout=10)
                        if response_alt.status_code == 200:
                            result_alt = response_alt.json()
                            if result_alt.get("status") == 200:
                                df_alt = pd.DataFrame(result_alt.get("data", []))
                                print(f"數據條數：{len(df_alt)}")
                                if not df_alt.empty:
                                    print(f"欄位：{list(df_alt.columns)}")
                                    print("前3筆：")
                                    print(df_alt.head(3))
                            else:
                                print(f"狀態：{result_alt.get('status')} - {result_alt.get('msg')}")
                        else:
                            print(f"HTTP {response_alt.status_code}")
                    except Exception as e:
                        print(f"異常：{e}")
                        
    except Exception as e:
        print(f"異常：{e}")

if __name__ == "__main__":
    check_stock_count()




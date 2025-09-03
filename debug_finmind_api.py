#!/usr/bin/env python3
"""
FinMind API 連接測試腳本
"""

import requests
import json

def test_finmind_login():
    """測試 FinMind API 登入"""
    print("🔍 測試 FinMind API 登入...")
    
    # 方法1：使用 v4 API
    url_v4 = "https://api.finmindtrade.com/api/v4/login"
    data_v4 = {"user_id": "finmind", "password": "finmind"}
    
    try:
        response = requests.post(url_v4, json=data_v4, timeout=10)
        print(f"v4 API 回應：HTTP {response.status_code}")
        print(f"v4 API 內容：{response.text[:200]}...")
    except Exception as e:
        print(f"v4 API 異常：{e}")
    
    # 方法2：使用 v2 API
    url_v2 = "https://api.finmindtrade.com/api/v2/login"
    data_v2 = {"user_id": "finmind", "password": "finmind"}
    
    try:
        response = requests.post(url_v2, json=data_v2, timeout=10)
        print(f"v2 API 回應：HTTP {response.status_code}")
        print(f"v2 API 內容：{response.text[:200]}...")
    except Exception as e:
        print(f"v2 API 異常：{e}")
    
    # 方法3：直接使用 token
    print("\n🔍 測試直接使用 token...")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZmlubWluZCIsImlhdCI6MTczNTQ5NzI5N30.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8"
    
    url_data = "https://api.finmindtrade.com/api/v4/data"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "dataset": "TaiwanVariousIndicators5Seconds",
        "start_date": "2025-09-02",
        "end_date": "2025-09-02"
    }
    
    try:
        response = requests.get(url_data, headers=headers, params=params, timeout=10)
        print(f"直接 token 回應：HTTP {response.status_code}")
        print(f"直接 token 內容：{response.text[:200]}...")
    except Exception as e:
        print(f"直接 token 異常：{e}")

if __name__ == "__main__":
    test_finmind_login()

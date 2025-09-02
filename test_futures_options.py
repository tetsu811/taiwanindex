#!/usr/bin/env python3
"""
測試 FinMind v4 API 中期貨和選擇權相關的資料集
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta

def login_finmind():
    """登入 FinMind 並取得 token"""
    try:
        # 使用正確的帳戶資訊
        url = "https://api.finmindtrade.com/api/v4/login"
        payload = {
            "user_id": "tetsu",
            "password": "Tt810811"
        }
        
        print(f"🔐 嘗試登入帳戶: {payload['user_id']}")
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
                    print(f"回應內容：{data}")
                    return None
            else:
                print(f"❌ 登入失敗：回應格式異常")
                print(f"回應內容：{data}")
                return None
        else:
            print(f"❌ 登入失敗：HTTP {response.status_code}")
            print(f"回應內容：{response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 登入失敗：{e}")
        return None

def test_dataset(token, dataset_name, date):
    """測試單一資料集"""
    try:
        url = "https://api.finmindtrade.com/api/v4/data"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 使用 GET 方法，參數放在 URL 中
        params = {
            "dataset": dataset_name,
            "start_date": date,
            "end_date": date
        }
        
        print(f"  🔍 測試 {dataset_name}...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                df = pd.DataFrame(data['data'])
                print(f"    ✅ 成功！資料形狀: {df.shape}")
                print(f"      欄位: {list(df.columns)}")
                print(f"      前3筆資料:")
                for i, row in df.head(3).iterrows():
                    print(f"        {i+1}: {dict(row)}")
                return {
                    'success': True,
                    'data': df,
                    'shape': df.shape,
                    'columns': list(df.columns)
                }
            else:
                print(f"    ⚠️ 無資料")
                return {'success': False, 'error': '無資料'}
        else:
            print(f"    ❌ API 錯誤: {response.status_code}")
            print(f"      錯誤訊息: {response.text}")
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        print(f"    ❌ 請求失敗: {e}")
        return {'success': False, 'error': str(e)}

def test_futures_options_datasets(token):
    """測試期貨和選擇權相關的資料集"""
    print(f"\n" + "="*80)
    print("🔍 測試期貨和選擇權相關的資料集")
    print("="*80)
    
    # 期貨和選擇權相關的資料集
    futures_options_datasets = {
        "期貨選擇權總覽": [
            'TaiwanOptionFutureInfo'
        ],
        "期貨日成交資訊": [
            'TaiwanFuturesDaily'
        ],
        "選擇權日成交資訊": [
            'TaiwanOptionDaily'
        ],
        "期貨交易明細": [
            'TaiwanFuturesTick'
        ],
        "選擇權交易明細": [
            'TaiwanOptionTick'
        ],
        "期貨三大法人買賣": [
            'TaiwanFuturesInstitutionalInvestors'
        ],
        "選擇權三大法人買賣": [
            'TaiwanOptionInstitutionalInvestors'
        ],
        "期貨夜盤三大法人買賣": [
            'TaiwanFuturesInstitutionalInvestorsAfterHours'
        ],
        "選擇權夜盤三大法人買賣": [
            'TaiwanOptionInstitutionalInvestorsAfterHours'
        ],
        "期貨各卷商每日交易": [
            'TaiwanFuturesDealerTradingVolumeDaily'
        ],
        "選擇權各卷商每日交易": [
            'TaiwanOptionDealerTradingVolumeDaily'
        ],
        "期貨大額交易人未沖銷部位": [
            'TaiwanFuturesOpenInterestLargeTraders'
        ],
        "選擇權大額交易人未沖銷部位": [
            'TaiwanOptionOpenInterestLargeTraders'
        ]
    }
    
    # 測試日期 - 使用最近的日期
    test_date = '2024-01-02'  # 使用 2024-01-02
    
    successful_datasets = {}
    failed_datasets = {}
    
    for category, datasets in futures_options_datasets.items():
        print(f"\n📊 測試 {category} 相關資料集...")
        successful_datasets[category] = []
        failed_datasets[category] = []
        
        for dataset in datasets:
            result = test_dataset(token, dataset, test_date)
            
            if result['success']:
                successful_datasets[category].append({
                    'dataset': dataset,
                    'shape': result['shape'],
                    'columns': result['columns']
                })
            else:
                failed_datasets[category].append({
                    'dataset': dataset,
                    'error': result['error']
                })
    
    # 總結報告
    print(f"\n" + "="*80)
    print("📊 期貨選擇權資料集測試總結報告")
    print("="*80)
    
    total_success = 0
    total_failed = 0
    
    for category, datasets in futures_options_datasets.items():
        success_count = len(successful_datasets[category])
        failed_count = len(failed_datasets[category])
        total_count = len(datasets)
        
        total_success += success_count
        total_failed += failed_count
        
        print(f"\n{category}:")
        print(f"  ✅ 成功: {success_count}/{total_count}")
        
        if successful_datasets[category]:
            print(f"  可用資料集:")
            for ds in successful_datasets[category]:
                print(f"    - {ds['dataset']}: {ds['shape']} 筆資料")
                print(f"      欄位: {ds['columns']}")
        
        if failed_datasets[category]:
            print(f"  ❌ 失敗: {failed_count} 個")
            for ds in failed_datasets[category]:
                print(f"    - {ds['dataset']}: {ds['error']}")
    
    print(f"\n" + "="*80)
    print(f"📊 總體結果：成功 {total_success} 個，失敗 {total_failed} 個")
    print("="*80)
    
    return successful_datasets, failed_datasets

def main():
    """主函數"""
    print("🚀 啟動 FinMind 期貨選擇權資料集測試...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    print(f"🔑 Token: {token[:20]}...")
    
    # 測試期貨選擇權資料集
    successful_datasets, failed_datasets = test_futures_options_datasets(token)
    
    # 儲存結果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = f"futures_options_result_{timestamp}.json"
    
    result_data = {
        'timestamp': timestamp,
        'successful_datasets': successful_datasets,
        'failed_datasets': failed_datasets
    }
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 測試結果已儲存到 {result_file}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
測試 FinMind 所有您需要的資料集
"""

import finmind
import pandas as pd
from datetime import datetime, timedelta

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

def test_all_required_datasets(token):
    """測試您需要的所有資料集"""
    print(f"\n" + "="*80)
    print("🔍 測試您需要的所有資料集")
    print("="*80)
    
    # 您需要的資料集清單
    required_datasets = {
        "期貨空單": [
            'TaiwanFuturesDaily',
            'TaiwanFuturesInstitutionalInvestors', 
            'TaiwanFuturesMarginPurchase',
            'TaiwanFuturesShortSale'
        ],
        "0050正2指數外資庫存": [
            'TaiwanStockPrice',
            'TaiwanStockInstitutionalInvestorsBuySell',
            'TaiwanStockETF'
        ],
        "八大行庫買超": [
            'TaiwanStockGovernmentBankBuySell',
            'TaiwanStockInstitutionalInvestorsBuySell'
        ],
        "加權指數": [
            'TaiwanStockIndex',
            'TaiwanStockPrice',
            'TaiwanStockTradingDailyReport'
        ],
        "櫃買指數": [
            'TaiwanStockIndex',
            'TaiwanStockPrice'
        ],
        "漲跌家數": [
            'TaiwanStockPrice',
            'TaiwanStockTradingDailyReport'
        ],
        "融資融券": [
            'TaiwanStockMarginPurchase',
            'TaiwanStockShortSale'
        ],
        "台幣匯率": [
            'TaiwanExchangeRate',
            'ExchangeRate'
        ]
    }
    
    successful_datasets = {}
    failed_datasets = {}
    
    for category, datasets in required_datasets.items():
        print(f"\n📊 測試 {category} 相關資料集...")
        successful_datasets[category] = []
        failed_datasets[category] = []
        
        for dataset in datasets:
            try:
                print(f"  🔍 測試 {dataset}...")
                data = finmind.data.get_data(token, dataset=dataset, start_date='2024-01-01', end_date='2024-01-01')
                
                if not data.empty:
                    print(f"    ✅ 成功！資料形狀: {data.shape}")
                    print(f"      欄位: {list(data.columns)}")
                    successful_datasets[category].append({
                        'dataset': dataset,
                        'shape': data.shape,
                        'columns': list(data.columns),
                        'sample': data.head(2).to_dict('records')
                    })
                else:
                    print(f"    ⚠️ 無資料")
                    failed_datasets[category].append(dataset)
                    
            except Exception as e:
                print(f"    ❌ 失敗: {e}")
                failed_datasets[category].append(dataset)
    
    # 總結報告
    print(f"\n" + "="*80)
    print("📊 資料集測試總結報告")
    print("="*80)
    
    for category, datasets in required_datasets.items():
        success_count = len(successful_datasets[category])
        total_count = len(datasets)
        print(f"\n{category}:")
        print(f"  ✅ 成功: {success_count}/{total_count}")
        
        if successful_datasets[category]:
            print(f"  可用資料集:")
            for ds in successful_datasets[category]:
                print(f"    - {ds['dataset']}: {ds['shape']} 筆資料")
                print(f"      欄位: {ds['columns']}")
        
        if failed_datasets[category]:
            print(f"  ❌ 失敗: {failed_datasets[category]}")
    
    return successful_datasets, failed_datasets

def main():
    """主函數"""
    print("🚀 啟動 FinMind 資料集測試...")
    
    # 登入
    token = login_finmind()
    if not token:
        print("❌ 登入失敗，無法繼續")
        return
    
    # 檢查用戶資訊
    user_info = check_user_info(token)
    
    # 測試所有需要的資料集
    successful_datasets, failed_datasets = test_all_required_datasets(token)
    
    print(f"\n✅ 測試完成！")
    print(f"📊 成功: {sum(len(v) for v in successful_datasets.values())} 個資料集")
    print(f"❌ 失敗: {sum(len(v) for v in failed_datasets.values())} 個資料集")

if __name__ == "__main__":
    main()

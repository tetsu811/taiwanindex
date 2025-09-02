#!/usr/bin/env python3
"""
檢查 FinMind 免費版所有可用的資料集和欄位
"""

import finmind
import pandas as pd
from datetime import datetime, timedelta
import json

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

def get_available_datasets(token):
    """取得可用的資料集清單"""
    try:
        datasets = finmind.data.get_available_datasets(token)
        print(f"📋 可用資料集: {datasets}")
        return datasets
    except Exception as e:
        print(f"❌ 無法取得資料集清單: {e}")
        return []

def test_dataset(token, dataset_name, start_date, end_date):
    """測試特定資料集"""
    print(f"\n🔍 測試資料集: {dataset_name}")
    print(f"📅 日期範圍: {start_date} 到 {end_date}")
    
    try:
        # 嘗試取得資料
        data = finmind.data.get_data(
            token, 
            dataset=dataset_name, 
            start_date=start_date, 
            end_date=end_date
        )
        
        if not data.empty:
            print(f"✅ 成功取得資料!")
            print(f"📊 資料形狀: {data.shape}")
            print(f"🏷️ 欄位: {list(data.columns)}")
            print(f"📝 前3筆資料:")
            print(data.head(3))
            
            # 檢查是否有數值資料
            numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
            if numeric_columns:
                print(f"🔢 數值欄位: {numeric_columns}")
                
                # 顯示數值欄位的統計資訊
                for col in numeric_columns[:5]:  # 只顯示前5個
                    if col in data.columns:
                        print(f"   {col}: {data[col].describe()}")
            
            return data
        else:
            print(f"⚠️ 資料為空")
            return None
            
    except Exception as e:
        print(f"❌ 查詢失敗: {e}")
        return None

def test_taiwan_datasets(token):
    """測試所有台股相關的資料集"""
    print("\n" + "="*60)
    print("🇹🇼 測試所有台股相關資料集")
    print("="*60)
    
    # 設定測試日期（使用最近的日期）
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # 所有可能的台股資料集
    taiwan_datasets = [
        'TaiwanStockInfo',                    # 台股總覽
        'TaiwanStockPrice',                   # 台股價格
        'TaiwanStockIndex',                   # 台股指數
        'TaiwanStockInstitutionalInvestorsBuySell',  # 三大法人買賣超
        'TaiwanStockMarginPurchase',          # 融資融券
        'TaiwanStockShortSale',               # 借券
        'TaiwanStockGovernmentBankBuySell',  # 八大行庫買賣
        'TaiwanStockTradingDailyReport',     # 台股交易日報
        'TaiwanStockWarrantTradingDailyReport',  # 權證交易日報
        'TaiwanStockBalanceSheet',            # 資產負債表
        'TaiwanStockFinancialStatements',     # 財務報表
        'TaiwanStockCashDividend',            # 現金股利
        'TaiwanStockStockDividend',           # 股票股利
        'TaiwanStockShareholding',            # 股權分散
        'TaiwanStockShareholdingChange',      # 股權變動
        'TaiwanStockNews',                    # 台股新聞
        'TaiwanStockNewsCategory',            # 台股新聞分類
        'TaiwanStockNewsTag',                 # 台股新聞標籤
        'TaiwanStockNewsContent',             # 台股新聞內容
        'TaiwanStockNewsSummary',             # 台股新聞摘要
        'TaiwanStockNewsTitle',               # 台股新聞標題
        'TaiwanStockNewsUrl',                 # 台股新聞網址
        'TaiwanStockNewsDate',                # 台股新聞日期
        'TaiwanStockNewsSource',              # 台股新聞來源
        'TaiwanStockNewsAuthor',              # 台股新聞作者
        'TaiwanStockNewsContentLength',       # 台股新聞內容長度
        'TaiwanStockNewsTitleLength',         # 台股新聞標題長度
        'TaiwanStockNewsUrlLength',           # 台股新聞網址長度
        'TaiwanStockNewsDateLength',          # 台股新聞日期長度
        'TaiwanStockNewsSourceLength',        # 台股新聞來源長度
        'TaiwanStockNewsAuthorLength',        # 台股新聞作者長度
    ]
    
    successful_datasets = []
    failed_datasets = []
    
    for dataset in taiwan_datasets:
        try:
            data = test_dataset(token, dataset, start_date, end_date)
            if data is not None and not data.empty:
                successful_datasets.append(dataset)
            else:
                failed_datasets.append(dataset)
        except Exception as e:
            print(f"❌ {dataset} 測試異常: {e}")
            failed_datasets.append(dataset)
    
    # 總結結果
    print(f"\n" + "="*60)
    print("📊 測試結果總結")
    print("="*60)
    print(f"✅ 成功的資料集 ({len(successful_datasets)}):")
    for dataset in successful_datasets:
        print(f"   - {dataset}")
    
    print(f"\n❌ 失敗的資料集 ({len(failed_datasets)}):")
    for dataset in failed_datasets:
        print(f"   - {dataset}")
    
    return successful_datasets, failed_datasets

def test_global_datasets(token):
    """測試全球市場資料集"""
    print("\n" + "="*60)
    print("🌍 測試全球市場資料集")
    print("="*60)
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    global_datasets = [
        'USStockInfo',                        # 美股總覽
        'USStockPrice',                       # 美股價格
        'USStockIndex',                       # 美股指數
        'USStockInstitutionalInvestorsBuySell',  # 美股法人買賣超
        'USStockMarginPurchase',              # 美股融資融券
        'USStockShortSale',                   # 美股借券
        'USStockTradingDailyReport',         # 美股交易日報
        'USStockBalanceSheet',                # 美股資產負債表
        'USStockFinancialStatements',         # 美股財務報表
        'USStockCashDividend',                # 美股現金股利
        'USStockStockDividend',               # 美股股票股利
        'USStockShareholding',                # 美股股權分散
        'USStockShareholdingChange',          # 美股股權變動
        'USStockNews',                        # 美股新聞
        'USStockNewsCategory',                # 美股新聞分類
        'USStockNewsTag',                     # 美股新聞標籤
        'USStockNewsContent',                 # 美股新聞內容
        'USStockNewsSummary',                 # 美股新聞摘要
        'USStockNewsTitle',                   # 美股新聞標題
        'USStockNewsUrl',                     # 美股新聞網址
        'USStockNewsDate',                    # 美股新聞日期
        'USStockNewsSource',                  # 美股新聞來源
        'USStockNewsAuthor',                  # 美股新聞作者
        'USStockNewsContentLength',           # 美股新聞內容長度
        'USStockNewsTitleLength',             # 美股新聞標題長度
        'USStockNewsUrlLength',               # 美股新聞網址長度
        'USStockNewsDateLength',              # 美股新聞日期長度
        'USStockNewsSourceLength',            # 美股新聞來源長度
        'USStockNewsAuthorLength',            # 美股新聞作者長度
    ]
    
    successful_datasets = []
    failed_datasets = []
    
    for dataset in global_datasets:
        try:
            data = test_dataset(token, dataset, start_date, end_date)
            if data is not None and not data.empty:
                successful_datasets.append(dataset)
            else:
                failed_datasets.append(dataset)
        except Exception as e:
            print(f"❌ {dataset} 測試異常: {e}")
            failed_datasets.append(dataset)
    
    # 總結結果
    print(f"\n" + "="*60)
    print("📊 全球市場測試結果總結")
    print("="*60)
    print(f"✅ 成功的資料集 ({len(successful_datasets)}):")
    for dataset in successful_datasets:
        print(f"   - {dataset}")
    
    print(f"\n❌ 失敗的資料集 ({len(failed_datasets)}):")
    for dataset in failed_datasets:
        print(f"   - {dataset}")
    
    return successful_datasets, failed_datasets

def main():
    """主函數"""
    print("🚀 開始檢查 FinMind 免費版所有可用資料集")
    
    # 登入
    token = login_finmind()
    if not token:
        return
    
    # 檢查用戶資訊
    user_info = check_user_info(token)
    
    # 取得可用資料集清單
    available_datasets = get_available_datasets(token)
    
    # 測試台股資料集
    taiwan_success, taiwan_failed = test_taiwan_datasets(token)
    
    # 測試全球市場資料集
    global_success, global_failed = test_global_datasets(token)
    
    # 最終總結
    print(f"\n" + "="*60)
    print("🎯 最終總結")
    print("="*60)
    print(f"📊 總共測試的資料集: {len(taiwan_success) + len(taiwan_failed) + len(global_success) + len(global_failed)}")
    print(f"✅ 成功的資料集: {len(taiwan_success) + len(global_success)}")
    print(f"❌ 失敗的資料集: {len(taiwan_failed) + len(global_failed)}")
    print(f"🇹🇼 台股成功: {len(taiwan_success)}")
    print(f"🌍 全球成功: {len(global_success)}")
    
    # 保存結果到檔案
    results = {
        'user_info': user_info,
        'available_datasets': available_datasets,
        'taiwan_successful': taiwan_success,
        'taiwan_failed': taiwan_failed,
        'global_successful': global_success,
        'global_failed': global_failed,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('finmind_dataset_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細結果已保存到 finmind_dataset_results.json")

if __name__ == "__main__":
    main()



def test_required_datasets():
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
    
    print("📋 您需要的資料集清單：")
    for category, datasets in required_datasets.items():
        print(f"\n{category}:")
        for dataset in datasets:
            print(f"  - {dataset}")
    
    print(f"\n⚠️ 注意：由於環境問題，無法直接測試這些資料集")
    print(f"   建議您直接在 FinMind 網站上測試這些資料集的可用性")
    print(f"   或者檢查您的帳戶權限和 API 設定")
    
    return required_datasets

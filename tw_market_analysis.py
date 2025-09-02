"""
Taiwan stock market trend analysis script.

This script fetches Taiwan stock market data from FinMind API and sends daily reports via LINE.
First logs in to FinMind to get a fresh token.
"""

from __future__ import annotations

import sys
import os
from datetime import datetime, time, timedelta
from typing import Optional, Tuple

import pandas as pd
import requests


def is_after_5pm_taipei(now: datetime | None = None) -> bool:
    """Return True if current local time in Asia/Taipei is after 17:00."""
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("Asia/Taipei")
        now_tpe = (now or datetime.now(tz)).astimezone(tz)
    except Exception:
        now_tpe = now or datetime.now()

    five_pm = time(17, 0, 0)
    return now_tpe.time() >= five_pm


def get_two_latest_trading_dates_twse() -> Tuple[str, str]:
    """取得最近兩個交易日"""
    end = datetime.now().date()
    candidates = [end - timedelta(days=i) for i in range(0, 14)]
    valid: list[str] = []
    
    for d in candidates:
        try:
            # 使用 TWSE API 檢查是否為交易日
            d_str = d.strftime("%Y%m%d")
            resp = requests.get(
                "https://www.twse.com.tw/exchangeReport/MI_INDEX",
                params={"response": "json", "date": d_str, "type": "ALL"},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=20
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("stat") == "OK":
                    valid.append(d.isoformat())
                    if len(valid) >= 2:
                        break
        except Exception:
            continue
    
    if len(valid) >= 2:
        return valid[0], valid[1]
    
    # 後備方案
    return end.isoformat(), (end - timedelta(days=1)).isoformat()


def login_finmind() -> str:
    """登入 FinMind 取得新的 token"""
    login_url = "https://api.finmindtrade.com/api/v4/login"
    
    # 根據文檔，使用 user_id 和 password
    login_data = {
        "user_id": "tetsu",
        "password": "Tt810811"
    }
    
    try:
        print(f"[Info] 嘗試登入 FinMind，使用參數：{list(login_data.keys())}")
        print(f"[Debug] 登入資料：{login_data}")
        
        # 使用 data 而不是 json，因為文檔範例使用 data
        login_resp = requests.post(login_url, data=login_data, timeout=20)
        print(f"[Debug] 登入回應：{login_resp.status_code} {login_resp.text[:200]}")
        
        if login_resp.status_code == 200:
            resp_data = login_resp.json()
            if resp_data.get("msg") == "success" and resp_data.get("status") == 200:
                new_token = resp_data.get("token")
                if new_token:
                    print(f"[Info] 登入成功，取得新 token")
                    return new_token
                else:
                    print(f"[Warn] 登入成功但未取得 token")
            else:
                print(f"[Warn] 登入回應格式異常：{resp_data}")
        else:
            print(f"[Warn] 登入失敗：{login_resp.status_code} {login_resp.text}")
                    
    except Exception as exc:
        print(f"[Warn] 登入異常：{exc}")
    
    # 如果登入失敗，使用舊 token
    print("[Warn] 登入失敗，使用舊 token")
    OLD_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyNS0wOC0yOCAxNzowMDowMSIsInVzZXJfaWQiOiJ0ZXRzdSIsImlwIjoiMTI0LjIxOC4yMTYuMTgzIiwiZXhwIjoxNzU2OTc2NDAxfQ.AjeOEd4TUeRC_j8D_uoGiD2uiHtNuYoLEMzyA0M_zoQ"
    return OLD_TOKEN


def check_user_info(token: str) -> None:
    """檢查用戶資訊和權限"""
    try:
        user_info_url = "https://api.web.finmindtrade.com/v2/user_info"
        headers = {"Authorization": f"Bearer {token}"}
        user_resp = requests.get(user_info_url, headers=headers, timeout=20)
        print(f"[Debug] 用戶資訊檢查：{user_resp.status_code} {user_resp.text[:500]}")
        
        if user_resp.status_code == 200:
            user_data = user_resp.json()
            print(f"[Info] 用戶資訊：{user_data}")
        else:
            print(f"[Warn] 用戶資訊檢查失敗：{user_resp.status_code}")
            
    except Exception as exc:
        print(f"[Warn] 用戶資訊檢查異常：{exc}")


def get_available_datasets(token: str) -> None:
    """查詢可用的資料集清單"""
    try:
        # 使用 datalist API 查詢可用資料集
        datalist_url = "https://api.finmindtrade.com/api/v4/datalist"
        headers = {"Authorization": f"Bearer {token}"}
        
        print(f"[Info] 查詢可用資料集清單...")
        resp = requests.get(datalist_url, headers=headers, timeout=20)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"[Info] 資料集清單查詢成功")
            print(f"[Debug] 回應內容：{data}")
            
            if data.get("data"):
                datasets = data["data"]
                print(f"[Info] 找到 {len(datasets)} 個可用資料集：")
                for i, dataset in enumerate(datasets[:20]):  # 只顯示前20個
                    print(f"  {i+1}. {dataset}")
                if len(datasets) > 20:
                    print(f"  ... 還有 {len(datasets) - 20} 個資料集")
            else:
                print(f"[Warn] 未找到資料集清單")
        else:
            print(f"[Warn] 資料集清單查詢失敗：{resp.status_code} {resp.text[:200]}")
            
    except Exception as exc:
        print(f"[Warn] 資料集清單查詢異常：{exc}")


def get_dataset_fields(token: str, dataset: str) -> None:
    """查詢特定資料集的欄位名稱對照"""
    try:
        # 使用 translation API 查詢欄位名稱對照
        translation_url = "https://api.finmindtrade.com/api/v4/translation"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"dataset": dataset}
        
        print(f"[Info] 查詢 {dataset} 的欄位名稱對照...")
        resp = requests.get(translation_url, headers=headers, params=params, timeout=20)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"[Info] {dataset} 欄位名稱對照查詢成功")
            print(f"[Debug] 回應內容：{data}")
            
            if data.get("data"):
                fields = data["data"]
                print(f"[Info] {dataset} 有 {len(fields)} 個欄位：")
                for field in fields:
                    print(f"  - {field}")
            else:
                print(f"[Warn] {dataset} 未找到欄位資訊")
        else:
            print(f"[Warn] {dataset} 欄位名稱對照查詢失敗：{resp.status_code} {resp.text[:200]}")
            
    except Exception as exc:
        print(f"[Warn] {dataset} 欄位名稱對照查詢異常：{exc}")


def fetch_dataset(dataset: str, date: str, data_id: Optional[str] = None, prev_date: Optional[str] = None) -> pd.DataFrame:
    """從 FinMind API 取得資料"""
    # 先登入取得新 token
    api_token = login_finmind()
    
    # 嘗試 v2 API 端點
    base_urls = [
        "https://api.web.finmindtrade.com/v2/data",  # v2 API
        "https://api.finmindtrade.com/api/v4/data"   # v4 API (備用)
    ]
    
    headers = {"Authorization": f"Bearer {api_token}"}
    
    for base_url in base_urls:
        try:
            print(f"[Debug] 嘗試 {base_url} 取得 {dataset}")
            
            # 優先使用日期範圍查詢
            if prev_date:
                params = {
                    "dataset": dataset,
                    "start_date": prev_date,
                    "end_date": date,
                }
                if data_id is not None:
                    params["data_id"] = data_id
                
                resp = requests.get(base_url, params=params, headers=headers, timeout=20)
                if resp.ok:
                    data = resp.json().get("data", [])
                    df = pd.DataFrame(data)
                    print(f"[Info] 成功使用 {base_url} 取得 {dataset} (日期範圍)")
                    return df.reset_index(drop=True)
            
            # 單日查詢
            params = {"dataset": dataset, "date": date}
            if data_id is not None:
                params["data_id"] = data_id
            
            resp = requests.get(base_url, params=params, headers=headers, timeout=20)
            
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                df = pd.DataFrame(data)
                print(f"[Info] 成功使用 {base_url} 取得 {dataset} (單日)")
                return df.reset_index(drop=True)
            else:
                print(f"[Warn] {base_url} 取得 {dataset} 於 {date} 失敗：{resp.status_code} {resp.reason}")
                if resp.status_code == 422:
                    print(f"[Debug] 422 from {dataset}({date}): {resp.text[:200]}")
                elif resp.status_code == 400:
                    print(f"[Debug] 400 from {dataset}({date}): {resp.text[:200]}")
                    
        except Exception as exc:
            print(f"[Error] {base_url} 取得 {dataset} 時發生異常：{exc}")
    
    print(f"[Warn] 所有 API 端點都失敗，無法取得 {dataset}")
    return pd.DataFrame()


def extract_single_value(df: pd.DataFrame, field: str) -> Optional[float]:
    """從 DataFrame 中提取單一數值"""
    if df is None or df.empty:
        return None
    
    try:
        if field in df.columns:
            value = df[field].iloc[-1]
            if pd.notna(value):
                return float(value)
        
        # 嘗試其他可能的欄位名稱
        field_mapping = {
            'close': ['close', 'Close', 'price', 'Price', 'index', 'Index'],
            'net_buy_sell': ['net_buy_sell', 'buy_sell', 'net_value', 'value'],
            'margin_maintenance_ratio': ['margin_maintenance_ratio', 'maintain_rate', 'margin_ratio'],
            'short_sale_balance': ['short_sale_balance', 'balance', 'short_balance'],
            'foreign_investor_net_position': ['foreign_investor_net_position', 'foreign_net', 'foreign_position'],
            'advance_count': ['advance_count', 'up', 'rise', 'advancers'],
            'decline_count': ['decline_count', 'down', 'fall', 'decliners']
        }
        
        if field in field_mapping:
            for alt_field in field_mapping[field]:
                if alt_field in df.columns:
                    value = df[alt_field].iloc[-1]
                    if pd.notna(value):
                        return float(value)
        
        return None
        
    except Exception:
        return None


def fmt(v: Optional[float]) -> str:
    """格式化數值顯示"""
    if v is None:
        return "無資料"
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    return f"{v:,.2f}"


def send_line_push(message: str) -> None:
    """發送 LINE 通知"""
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    line_to_csv = os.getenv("LINE_TO")
    
    if not channel_access_token or not line_to_csv:
        print("[Warn] 未設定 LINE 環境變數")
        return
    
    recipients = [x.strip() for x in line_to_csv.split(",") if x.strip()]
    print(f"[Info] LINE 收件者：{recipients}")
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    
    try:
        for recipient in recipients:
            payload = {
                "to": recipient,
                "messages": [{"type": "text", "text": message}],
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                print(f"[Info] LINE 推送成功：{recipient}")
            else:
                print(f"[Warn] LINE 推送失敗：{resp.status_code} {resp.text}")
    except Exception as exc:
        print(f"[Warn] LINE 推送異常：{exc}")


def check_all_taiwan_datasets(token):
    """檢查所有台股相關的資料集"""
    print(f"\n" + "="*80)
    print("🔍 全面檢查所有台股相關資料集")
    print("="*80)
    
    # 所有可能的台股資料集
    all_taiwan_datasets = [
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
        'TaiwanStockETF',                     # 台股ETF
        'TaiwanStockETFInfo',                 # 台股ETF資訊
        'TaiwanStockETFPremiumDiscount',      # 台股ETF折溢價
        'TaiwanStockETFNetValue',             # 台股ETF淨值
        'TaiwanStockETFTradingVolume',        # 台股ETF成交量
        'TaiwanStockETFTradingValue',         # 台股ETF成交值
        'TaiwanStockETFTradingTurnover',      # 台股ETF成交筆數
        'TaiwanStockETFTradingMoney',         # 台股ETF成交金額
        'TaiwanStockETFTradingSpread',        # 台股ETF成交價差
        'TaiwanStockETFTradingOpen',          # 台股ETF開盤價
        'TaiwanStockETFTradingHigh',          # 台股ETF最高價
        'TaiwanStockETFTradingLow',           # 台股ETF最低價
        'TaiwanStockETFTradingClose',         # 台股ETF收盤價
        'TaiwanStockETFTradingMax',           # 台股ETF最高價
        'TaiwanStockETFTradingMin',           # 台股ETF最低價
        'TaiwanStockETFTradingSpread',        # 台股ETF價差
        'TaiwanStockETFTradingTurnover',      # 台股ETF成交筆數
        'TaiwanStockETFTradingMoney',         # 台股ETF成交金額
        'TaiwanStockETFTradingVolume',        # 台股ETF成交量
        'TaiwanStockETFTradingValue',         # 台股ETF成交值
        'TaiwanStockETFPremiumDiscount',      # 台股ETF折溢價
        'TaiwanStockETFNetValue',             # 台股ETF淨值
        'TaiwanStockETFInfo',                 # 台股ETF資訊
        'TaiwanStockETF',                     # 台股ETF
    ]
    
    successful_datasets = []
    failed_datasets = []
    
    # 使用最近的日期進行測試
    from datetime import datetime, timedelta
    test_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"📅 測試日期: {test_date}")
    print(f"🔢 總共要測試 {len(all_taiwan_datasets)} 個資料集")
    
    for i, dataset in enumerate(all_taiwan_datasets, 1):
        print(f"\n[{i:2d}/{len(all_taiwan_datasets)}] 🔍 測試: {dataset}")
        
        try:
            data = fetch_dataset(dataset, test_date)
            
            if data is not None and not data.empty:
                print(f"   ✅ 成功! 資料形狀: {data.shape}")
                print(f"   🏷️ 欄位: {list(data.columns)}")
                
                # 檢查是否有數值資料
                numeric_columns = [col for col in data.columns if data[col].dtype in ['int64', 'float64']]
                if numeric_columns:
                    print(f"   🔢 數值欄位: {numeric_columns[:5]}...")  # 只顯示前5個
                
                successful_datasets.append({
                    'dataset': dataset,
                    'shape': data.shape,
                    'columns': list(data.columns),
                    'numeric_columns': numeric_columns
                })
            else:
                print(f"   ⚠️ 資料為空")
                failed_datasets.append(dataset)
                
        except Exception as e:
            print(f"   ❌ 失敗: {str(e)[:100]}...")  # 只顯示前100個字元
            failed_datasets.append(dataset)
    
    # 總結結果
    print(f"\n" + "="*80)
    print("📊 全面檢查結果總結")
    print("="*80)
    print(f"✅ 成功的資料集 ({len(successful_datasets)}):")
    for item in successful_datasets:
        print(f"   - {item['dataset']} ({item['shape'][0]} 筆, {item['shape'][1]} 欄)")
    
    print(f"\n❌ 失敗的資料集 ({len(failed_datasets)}):")
    for dataset in failed_datasets:
        print(f"   - {dataset}")
    
    # 分析成功的資料集
    print(f"\n🔍 成功資料集分析:")
    for item in successful_datasets:
        dataset = item['dataset']
        columns = item['columns']
        
        print(f"\n📋 {dataset}:")
        print(f"   資料形狀: {item['shape']}")
        print(f"   所有欄位: {columns}")
        
        # 檢查是否有價格相關欄位
        price_related = [col for col in columns if any(word in col.lower() for word in ['price', 'close', 'open', 'high', 'low', 'volume', 'amount'])]
        if price_related:
            print(f"   💰 價格相關欄位: {price_related}")
        
        # 檢查是否有法人相關欄位
        institutional_related = [col for col in columns if any(word in col.lower() for word in ['foreign', 'investment', 'dealer', 'buy', 'sell'])]
        if institutional_related:
            print(f"   🏦 法人相關欄位: {institutional_related}")
        
        # 檢查是否有財務相關欄位
        financial_related = [col for col in columns if any(word in col.lower() for word in ['revenue', 'profit', 'asset', 'liability', 'equity', 'eps', 'pe'])]
        if financial_related:
            print(f"   📈 財務相關欄位: {financial_related}")
    
    return successful_datasets, failed_datasets

def run_analysis() -> None:
    """執行台股大盤分析"""
    print("開始執行台股大盤分析...")
    
    # 先登入並檢查用戶資訊
    token = login_finmind()
    print(f"[Info] 使用 token 檢查用戶資訊...")
    # 檢查用戶資訊
    user_info = check_user_info(token)
    
    # 檢查用戶等級
    level = "Unknown"
    level_num = 0
    if user_info:
        level = user_info.get('level_title', 'Unknown')
        level_num = user_info.get('level', 0)
        print(f"🔍 用戶等級檢查:")
        print(f"   - 等級名稱: {level}")
        print(f"   - 等級數字: {level_num}")
        print(f"   - 完整用戶資訊: {user_info}")
        
        if level_num < 3:
            print(f"⚠️ 警告：用戶等級 {level} (數字: {level_num}) 可能不是最高等級")
            print(f"   建議升級到 Sponsor 或更高等級")
        else:
            print(f"✅ 用戶等級 {level} 應該是最高等級")
    
    # 測試您需要的所有資料集
    print(f"\n[Info] 開始測試您需要的所有資料集...")
    successful_datasets, failed_datasets = check_all_taiwan_datasets(token)
    
    # 查詢可用的資料集清單
    print(f"[Info] 查詢可用的資料集清單...")
    get_available_datasets(token)
    
    # 查詢一些可能有用的資料集的欄位資訊
    print(f"[Info] 查詢可能有用的資料集欄位資訊...")
    potential_datasets = [
        'TaiwanStockBalanceSheet',           # 資產負債表
        'TaiwanStockFinancialStatements',    # 財務報表
        'TaiwanStockInstitutionalInvestorsBuySell',  # 三大法人買賣超
        'TaiwanStockInfo'                    # 台股總覽（已知可用）
    ]
    for dataset in potential_datasets:
        get_dataset_fields(token, dataset)
    
    # 取得最近兩個交易日
    today, prev = get_two_latest_trading_dates_twse()
    if not today or not prev:
        print("無法取得交易日資訊")
        return
    
    print(f"分析日期：{today} (對比 {prev})")
    
    # 測試基本資料集
    print(f"[Debug] 測試基本資料集...")
    test_data = fetch_dataset('TaiwanStockInfo', today)
    print(f"[Debug] TaiwanStockInfo 回應：{len(test_data)} 筆資料")
    if not test_data.empty:
        print(f"[Debug] 欄位：{list(test_data.columns)}")
        print(f"[Debug] 前幾筆資料：{test_data.head(2).to_dict()}")
        
        # 分析資料結構，尋找有用的資訊
        print(f"[Debug] 資料類型分析：")
        print(f"[Debug] 上市/櫃買分布：{test_data['type'].value_counts().to_dict()}")
        print(f"[Debug] 產業類別數量：{len(test_data['industry_category'].unique())}")
        print(f"[Debug] 前10個產業類別：{list(test_data['industry_category'].unique())[:10]}")
        
        # 嘗試尋找是否有價格相關的欄位
        if 'close' in test_data.columns:
            print(f"[Debug] 找到收盤價欄位，資料範圍：{test_data['close'].min()} - {test_data['close'].max()}")
        else:
            print(f"[Debug] 未找到收盤價欄位，嘗試其他可能的價格欄位...")
            price_columns = [col for col in test_data.columns if any(word in col.lower() for word in ['price', 'close', 'open', 'high', 'low'])]
            print(f"[Debug] 可能的價格相關欄位：{price_columns}")
    
    # 1. 加權指數 (嘗試從台股總覽中計算或尋找指數資料)
    taiex_today = fetch_dataset('TaiwanStockInfo', today)
    taiex_prev = fetch_dataset('TaiwanStockInfo', prev)
    
    # 嘗試不同的欄位名稱來取得指數資料
    taiex_v = None
    taiex_prev_v = None
    
    if not taiex_today.empty:
        # 嘗試尋找指數相關的資料
        index_stocks = taiex_today[taiex_today['stock_id'].isin(['0000', 'TAIEX', 'TWII'])]
        if not index_stocks.empty:
            print(f"[Debug] 找到指數相關股票：{index_stocks.to_dict()}")
            taiex_v = extract_single_value(index_stocks, 'close')
    
    if not taiex_prev.empty:
        index_stocks_prev = taiex_prev[taiex_prev['stock_id'].isin(['0000', 'TAIEX', 'TWII'])]
        if not index_stocks_prev.empty:
            taiex_prev_v = extract_single_value(index_stocks_prev, 'close')
    
    # 2. 櫃買指數 (嘗試從台股總覽中計算或尋找指數資料)
    otc_today = fetch_dataset('TaiwanStockInfo', today)
    otc_prev = fetch_dataset('TaiwanStockInfo', prev)
    
    otc_v = None
    otc_prev_v = None
    
    if not otc_today.empty:
        # 嘗試尋找櫃買指數相關的資料
        otc_stocks = otc_today[otc_today['stock_id'].isin(['0001', 'TPEX', 'GTSM'])]
        if not otc_stocks.empty:
            print(f"[Debug] 找到櫃買指數相關股票：{otc_stocks.to_dict()}")
            otc_v = extract_single_value(otc_stocks, 'close')
    
    if not otc_prev.empty:
        otc_stocks_prev = otc_prev[otc_prev['stock_id'].isin(['0001', 'TPEX', 'GTSM'])]
        if not otc_stocks_prev.empty:
            otc_prev_v = extract_single_value(otc_stocks_prev, 'close')
    
    # 3. 融資維持率 (使用台股交易日報)
    margin_today = fetch_dataset('TaiwanStockTradingDailyReport', today)
    margin_prev = fetch_dataset('TaiwanStockTradingDailyReport', prev)
    margin_v = extract_single_value(margin_today, 'margin_maintenance_ratio')
    margin_prev_v = extract_single_value(margin_prev, 'margin_maintenance_ratio')
    
    # 4. 借券餘額 (使用台股交易日報)
    short_today = fetch_dataset('TaiwanStockTradingDailyReport', today)
    short_prev = fetch_dataset('TaiwanStockTradingDailyReport', prev)
    short_v = extract_single_value(short_today, 'short_sale_balance')
    short_prev_v = extract_single_value(short_prev, 'short_sale_balance')
    
    # 5. 外資期貨口數 (使用台股交易日報)
    futures_today = fetch_dataset('TaiwanStockTradingDailyReport', today)
    futures_prev = fetch_dataset('TaiwanStockTradingDailyReport', prev)
    futures_v = extract_single_value(futures_today, 'foreign_investor_net_position')
    futures_prev_v = extract_single_value(futures_prev, 'foreign_investor_net_position')
    
    # 6. 八大行庫買賣超 (使用台股政府銀行買賣表)
    bank_today = fetch_dataset('TaiwanStockGovernmentBankBuySell', today)
    bank_prev = fetch_dataset('TaiwanStockGovernmentBankBuySell', prev)
    bank_v = extract_single_value(bank_today, 'net_buy_sell')
    bank_prev_v = extract_single_value(bank_prev, 'net_buy_sell')
    
    # 7. 三大法人買賣超 (使用可用的法人買賣超資料集)
    # 這個資料集需要日期範圍查詢，我們使用前30天作為範圍來確保有資料
    from datetime import datetime, timedelta
    
    # 計算前30天的日期作為 start_date
    today_dt = datetime.strptime(today, '%Y-%m-%d')
    prev_dt = datetime.strptime(prev, '%Y-%m-%d')
    
    start_date_today = (today_dt - timedelta(days=30)).strftime('%Y-%m-%d')
    start_date_prev = (prev_dt - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"[Debug] 三大法人買賣超查詢日期範圍：{start_date_today} 到 {today}")
    inst_today = fetch_dataset('TaiwanStockInstitutionalInvestorsBuySell', today, prev_date=start_date_today)
    inst_prev = fetch_dataset('TaiwanStockInstitutionalInvestorsBuySell', prev, prev_date=start_date_prev)
    
    inst_v = None
    inst_prev_v = None
    
    if not inst_today.empty:
        print(f"[Debug] 三大法人買賣超資料：{inst_today.to_dict()}")
        # 嘗試計算外資買賣超（Foreign_Investor 欄位）
        if 'Foreign_Investor' in inst_today.columns:
            inst_v = inst_today['Foreign_Investor'].iloc[0] if len(inst_today) > 0 else None
            print(f"[Debug] 外資買賣超：{inst_v}")
    
    if not inst_prev.empty:
        if 'Foreign_Investor' in inst_prev.columns:
            inst_prev_v = inst_prev['Foreign_Investor'].iloc[0] if len(inst_prev) > 0 else None
    
    # 8. 上市上漲家數 (嘗試從台股總覽中計算)
    adv_today = fetch_dataset('TaiwanStockInfo', today)
    adv_prev = fetch_dataset('TaiwanStockInfo', prev)
    
    adv_v = None
    adv_prev_v = None
    
    if not adv_today.empty:
        # 嘗試計算上漲家數（如果有價格資料）
        if 'close' in adv_today.columns and 'open' in adv_today.columns:
            # 計算上漲家數（收盤價 > 開盤價）
            adv_stocks = adv_today[adv_today['close'] > adv_today['open']]
            adv_v = len(adv_stocks)
            print(f"[Debug] 計算得出上漲家數：{adv_v}")
        else:
            print(f"[Debug] 無法計算上漲家數，缺少價格資料")
    
    if not adv_prev.empty:
        if 'close' in adv_prev.columns and 'open' in adv_prev.columns:
            adv_stocks_prev = adv_prev[adv_prev['close'] > adv_prev['open']]
            adv_prev_v = len(adv_stocks_prev)
    
    # 9. 上市下跌家數 (嘗試從台股總覽中計算)
    dec_today = fetch_dataset('TaiwanStockInfo', today)
    dec_prev = fetch_dataset('TaiwanStockInfo', prev)
    
    dec_v = None
    dec_prev_v = None
    
    if not dec_today.empty:
        # 嘗試計算下跌家數（如果有價格資料）
        if 'close' in dec_today.columns and 'open' in dec_today.columns:
            # 計算下跌家數（收盤價 < 開盤價）
            dec_stocks = dec_today[dec_today['close'] < dec_today['open']]
            dec_v = len(dec_stocks)
            print(f"[Debug] 計算得出下跌家數：{dec_v}")
        else:
            print(f"[Debug] 無法計算下跌家數，缺少價格資料")
    
    if not dec_prev.empty:
        if 'close' in dec_prev.columns and 'open' in dec_prev.columns:
            dec_stocks_prev = dec_prev[dec_prev['close'] < dec_prev['open']]
            dec_prev_v = len(dec_stocks_prev)
    
    # 生成報表
    report = f"""台股大盤日報：{today} (對比 {prev})
- 加權指數：{fmt(taiex_v)} (vs {fmt(taiex_prev_v)})
- 櫃買指數：{fmt(otc_v)} (vs {fmt(otc_prev_v)})
- 融資維持率(%)：{fmt(margin_v)} (vs {fmt(margin_prev_v)})
- 借券餘額：{fmt(short_v)} (vs {fmt(short_prev_v)})
- 外資期貨口數：{fmt(futures_v)} (vs {fmt(futures_prev_v)})
- 八大行庫買賣超：{fmt(bank_v)} (vs {fmt(bank_prev_v)})
- 三大法人買賣超：{fmt(inst_v)} (vs {fmt(inst_prev_v)})
- 上市上漲家數：{fmt(adv_v)} (vs {fmt(adv_prev_v)})
- 上市下跌家數：{fmt(dec_v)} (vs {fmt(dec_prev_v)})"""
    
    print(report)
    
    # 發送 LINE 通知
    send_line_push(report)


def main() -> None:
    # 暫時停用時間限制以便測試
    # if not is_after_5pm_taipei():
    #     print("現在時間未達 17:00，請於下午五點後再執行。")
    #     sys.exit(0)

    run_analysis()


if __name__ == "__main__":
    main()

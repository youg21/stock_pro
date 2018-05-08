# 导入django环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','stock_pro.settings')
django.setup()

import datetime

from django.db import connection
import pandas as pd
import numpy as np

from stock.crawls.stock import StockCrawl
from stock.models import StockBasicInfo,StockTradeMoneyHis
from stock.analysis.stock import StockAnalysis
from stock.analysis.bank import BankAnalysis
from stock.crawls.lhb import LHBInfo
from stock.crawls.crawlutils import get_sql_engine

def get_lhb_main_info(trade_date=datetime.datetime.now().strftime('%Y-%M-%d')):
    # 获取个股龙虎榜
    df = pd.read_sql('select * from stock_lhbmaininfo where trade_date="{0}"'.format(trade_date), get_sql_engine())
    if df.empty:
        return
    df['buy_rate'] = df['b_money'] / (df['b_money'] + df['s_money']) * 100
    
    # 获取个股对应的板块信息
    codes = list(df['code'])
    stocks = StockBasicInfo.objects.filter(code__in=codes)
    stock_in_bank = [[stock.code, [bank.name for bank in stock.bankbasicinfo_set.filter(bank_type='概念')]] for stock in
                     stocks]
    # stock_in_bank = [[stock.code,[bank.name for bank in stock.bankbasicinfo_set.all()]] for stock in stocks]
    bank_list = [[stock[0], ','.join(stock[1])] for stock in stock_in_bank]
    df_banks = pd.DataFrame(bank_list, columns=['code', 'banks'])
    df_banks[df_banks['banks'] == ''] = np.nan
    df_banks = df_banks.dropna()
    df = pd.merge(df, df_banks, how='left')
    
    df = df[['code', 'name', 'trade_date', 'change_rate', 'turnover', 'buy_rate', 'jm_rate', 'total_rate', 'banks',
             'reasons', 'jd']]
    df.to_excel('龙虎榜信息_{0}.xlsx'.format(trade_date))



if __name__ == '__main__':
    get_lhb_main_info('2018-05-04')





















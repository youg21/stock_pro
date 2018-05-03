# 导入django环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','stock_pro.settings')
django.setup()

from django.db import connection

from stock.crawls.stock import StockCrawl
from stock.models import StockBasicInfo,StockTradeMoneyHis
from stock.analysis.stock import StockAnalysis
from stock.analysis.bank import BankAnalysis

def crawl_stock_trade_info():
    cursor = connection.cursor()
    cursor.execute(
        'SELECT DISTINCT code from stock_stockbasicinfo where code not in (select DISTINCT `code` from stock_stocktrademoneyhis)')
    codes = cursor.fetchall()
    codes = [code[0] for code in codes]
    print(codes)
    stockinfo = StockCrawl()
    stockinfo.get_trade_his(codes=codes, days=10, adj='qfq')
    
def analysis_stock_trade_info():
    analysis = StockAnalysis()
    analysis.get_zhangting_stock(days=3)

def analysis_bank():
    bank_analysis = BankAnalysis()
    bank_analysis.trend_analysis('5G概念')


if __name__ == '__main__':
    # analysis_stock_trade_info()
    analysis_bank()














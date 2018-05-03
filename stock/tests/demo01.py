# 导入django环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','stock_pro.settings')
django.setup()

from django.db import connection

from stock.crawls.stock import StockInfo
from stock.models import StockBasicInfo,StockTradeMoneyHis

cursor = connection.cursor()
cursor.execute('SELECT DISTINCT code from stock_stockbasicinfo where code not in (select DISTINCT `code` from stock_stocktrademoneyhis)')
codes = cursor.fetchall()
codes = [code[0] for code in codes]
print(codes)
# stockinfo = StockInfo()
# stockinfo.get_trade_his(codes=codes, days=10, adj='qfq')



















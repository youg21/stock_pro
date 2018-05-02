# 导入django环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','stock_pro.settings')
django.setup()

from stock.crawls.stock import StockInfo

stockinfo = StockInfo()

stockinfo.get_trade_his()



















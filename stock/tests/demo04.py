# 导入django环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','stock_pro.settings')
django.setup()

from stock.crawls.crawlutils import get_trade_dates
from stock.models import BankBasicInfo


new_stock_bank = ['次新股','两年新股','次新开板']
# new_stock_bank = ['次新股','两年新股','次新开板','次新超跌','深次新股']
banks = BankBasicInfo.objects.filter(name__in=new_stock_bank)
# for bank in banks:
#     print(bank.name)

stocks = [[stock.code for stock in bank.stocks.all()] for bank in banks]
stock_list = []
for stock in stocks:
    stock_list.extend(stock)

print(len(stock_list))


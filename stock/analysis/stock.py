
from stock.models import StockBasicInfo,StockTradeMoneyHis
from stock.crawls.crawlutils import get_trade_dates


class StockAnalysis:
    '''
    股票分析类
    '''
    
    
    def get_zhangting_stock(self,days=1):
        # 获取指定日期的涨停股
        trade_dates = get_trade_dates(day_delta=days)
        trade_date = trade_dates[0]
        stock_trades = StockTradeMoneyHis.objects.filter(trade_date=trade_date).filter(change_rate__gte=7)
        # 获取涨停股对应的概念板块
        codes = [stock.code for stock in stock_trades]
        banks = [list(StockBasicInfo.objects.get(code=code).bankbasicinfo_set.filter(bank_type='概念')) for code in codes]
        bank_list = []
        for bank in banks:
            bank_list.extend(bank)
        bank_list = set(bank_list)

        for bank in bank_list:
            print(bank)
        
    


    # 获取异动股票
    # 异动股票：涨幅(>7、<7)、换手等
    
    
    # 获取连板股
    
    # 根据异动股，观察板块走势
    






































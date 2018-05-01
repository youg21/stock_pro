import tushare as ts
from stock.models import StockBasicInfo
from dateutil.parser import parse


class StockInfo:
    '''
    StockInfo类旨在获取一切与个股相关的数据，如个股基本资料数据、个股历史交易数据、个股当日数据等
    '''
    def get_basic_info(self):
        '''
        通过tushare获取个股基础数据
        :return:
        '''
        df = ts.get_stock_basics()
        df['code'] = df.index
        for _, row in enumerate(df.values):
            stock_info, _ = StockBasicInfo.objects.get_or_create(code=row[22])
            stock_info.code = row[22]
            stock_info.name = row[0]
            stock_info.industry = row[1]
            stock_info.area = row[2]
            stock_info.pe = row[3]
            stock_info.outstanding = row[4]
            stock_info.totals = row[5]
            stock_info.totalAssets = row[6]
            stock_info.liquidAssets = row[7]
            stock_info.fixedAssets = row[8]
            stock_info.reserved = row[9]
            stock_info.reservedPerShare = row[10]
            stock_info.esp = row[11]
            stock_info.bvps = row[12]
            stock_info.pb = row[13]
            timeToMarket = str(row[14])
            stock_info.timeToMarket = parse(timeToMarket) if timeToMarket != '0' else None
            stock_info.undp = row[15]
            stock_info.perundp = row[16]
            stock_info.rev = row[17]
            stock_info.profit = row[18]
            stock_info.gpr = row[19]
            stock_info.npr = row[20]
            stock_info.holders = row[21]
            stock_info.save()
    
    def get_trade_his(self):
        '''
        获取个股历史交替数据
        :return:
        '''
        # 通过pytdx获取行情数据，字段包括open、close、high、low、vol、amount
        # 其他字段通过基础字段计算出来
        
        
        # 通过东方财富网站，来获取个股的资金流动数据
        # 字段包括main_money、main_money_rate、super_money、super_money_rate、large_money、large_money_rate、midden_money、midden_money_rate、small_money、small_money_rate
        

    
    
    
    
    
    
    
    
    def get_trade_today_min(self):
        '''
        获取个股当日分钟数据
        :return:
        '''
        pass
    
    def get_trade_today_last(self):
        '''
        获取当日个股最新数据
        :return:
        '''
        pass
















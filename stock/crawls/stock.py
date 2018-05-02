import tushare as ts
from dateutil.parser import parse
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
import pandas as pd
from django.db import connection

from stock.models import StockBasicInfo

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
        hq_data = self.__get_trade_hq(code='000001')
        print(hq_data)
    
    
    
    
    
    
    
    
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


    def __get_trade_hq(self,code,days=10,adj='qfq'):
        mkcode = 1 if code.startswith('6') else 0
        api = TdxHq_API()
        with api.connect('218.108.98.244', 7709):
            data = api.get_security_bars(TDXParams.KLINE_TYPE_DAILY, mkcode, code, 0, days+1)
            data = api.to_df(data)
            data['datetime'] = data['datetime'].apply(lambda x: str(x[0:10]))
            data['datetime'] = pd.to_datetime(data['datetime'])
            data = data.assign(code=str(code))\
                .set_index('datetime',drop=True,inplace=False)\
                .drop(['year', 'month', 'day', 'hour','minute'],axis=1)
            data = data.sort_index(ascending=False)
            # 加入复权因子，计算复权数据
            if adj:
                df_adj = pd.read_csv('http://file.tushare.org/tsdata/f/factor/{0}.csv'.format(code))
                df_adj = df_adj.set_index('datetime')
                data = data.merge(df_adj, how='left',left_index=True, right_index=True)
                data['adj_factor'] = data['adj_factor'].fillna(method='bfill')
                for col in ['open', 'close', 'high', 'low']:
                    if adj == 'qfq':
                        data[col] = data[col] * data['adj_factor'] / float(df_adj['adj_factor'][0])
                    else:
                        data[col] = data[col] * data['adj_factor']
                    # data[col] = data[col].map(lambda x: '%.2f' % x)   # 会引起类型转换，从float转换成str
            # 计算换手率
            cursor = connection.cursor()
            cursor.execute('select outstanding from stock_stockbasicinfo where code="000001"')
            outstanding = cursor.fetchone()[0]*10**8
            data['outstanding'] = outstanding
            data['turnover'] = data['vol'] / data['outstanding'] * 100
            # 计算涨跌幅
            data['pre_close'] = data['close'].shift(-1)
            data['change_rate'] = (data['close'] - data['pre_close']) / data['pre_close'] * 100
            data = data.dropna()
            data = data[['code','pre_close','open','close','high','low','vol','amount','change_rate','turnover','outstanding']]
            return data
    
    def __get_trade_money(self):
        pass












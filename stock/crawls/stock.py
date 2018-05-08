import json
import re
from concurrent.futures import ThreadPoolExecutor
import time
import random
import logging
import datetime
from threading import Thread

import tushare as ts
from dateutil.parser import parse
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
import pandas as pd
from django.db import connection
import requests
import demjson

from stock.models import StockBasicInfo,StockTradeMoneyHis,StockTradeMoneyToday
from stock.crawls.crawlutils import get_user_agent_dict,compute_times

# 获取logging
log = logging.getLogger('mylogger')

class StockCrawl:
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
    
    @compute_times
    def get_trade_his(self,codes=None,days=1,adj='qfq'):
        '''
        获取个股历史交替数据
        通过pytdx获取行情数据，字段包括open、close、high、low、vol、amount
        其他字段通过基础字段计算出来
        通过东方财富网站，来获取个股的资金流动数据
        字段包括main_money、main_money_rate、super_money、super_money_rate、large_money、large_money_rate、midden_money、midden_money_rate、small_money、small_money_rate
        :return:
        '''
        # 获取全部股票代码
        if codes:
            stocks = StockBasicInfo.objects.filter(code__in=codes)
        else:
            stocks = StockBasicInfo.objects.all()
        # 创建线程池
        pool = ThreadPoolExecutor(100)
        # 获取数据，并通过多线程讲数据存入到数据库
        i = 1
        store_stocks = []
        for stock in stocks:
            code = stock.code
            name = stock.name
            for _ in range(3):
                try:
                    hq_data = self.__get_trade_hq(code=code, days=days, adj=adj)
                    money_data = self.__get_trade_money(code=code, days=days)
                    df_all = pd.concat([hq_data, money_data], axis=1)
                    df_all['name'] = name
                    df_all = df_all.dropna()
                    pool.submit(self.__trade_his_to_db, df_all)
                    time.sleep(random.randint(10, 20) / 10)
                    print('===============code:{0}---{1}次================='.format(code, i))
                    store_stocks.append(code)
                    i += 1
                    break
                except Exception as e:
                    info = 'code={0}获取数据出错'.format(code)
                    info = info + '\t' + str(e)
                    print(info)
                    log.error(info)
        # 返回已存储股票代码
        return store_stocks
    
    def get_trade_today_min(self):
        '''
        获取个股当日分钟数据
        :return:
        '''
        pass
    
    @compute_times
    def get_trade_today_last(self,trade_date=datetime.datetime.now()):
        '''
        获取当日个股最新数据
        :return:
        '''
        for _ in range(3):
            try:
                # ['code','name','close','change_money','change_rate','zhenfu','vol','amount','pre_close','open','high','low','zhangdie_5min','liangbi','turnover','pe','timeToMarket']
                df_trade = self.__get_trade_today_last()
                # ['code','name','main_money','main_money_rate','super_money','super_money_rate','large_money','large_money_rate','midden_money','midden_money_rate','small_money','small_money_rate']
                df_money = self.__get_money_today_last()
                df_money = df_money.drop('name',axis=1)
                df = pd.merge(df_trade,df_money,on='code')
                df['trade_date'] = trade_date
                
                # 将数据存入数据库中
                Thread(target=self.__trade_today_to_db, args=[df,]).start()
                
                break
            except Exception as e:
                log.error(e)
            
    def __get_trade_hq(self, code, days=10, adj='qfq'):
        mkcode = 1 if code.startswith('6') else 0
        api = TdxHq_API()
        with api.connect('218.108.98.244', 7709):
            # 获取股票行情数据，不复权的数据
            data = api.get_security_bars(TDXParams.KLINE_TYPE_DAILY, mkcode, code, 0, days + 1)
            data = api.to_df(data)
            data['datetime'] = data['datetime'].apply(lambda x: str(x[0:10]))
            data['datetime'] = pd.to_datetime(data['datetime'])
            data = data.assign(code=str(code)).set_index('datetime', drop=True, inplace=False).drop(
                ['year', 'month', 'day', 'hour', 'minute'], axis=1)
            data = data.sort_index(ascending=False)
            # 加入复权因子，计算复权数据
            if adj:
                df_adj = pd.read_csv('http://file.tushare.org/tsdata/f/factor/{0}.csv'.format(code))
                df_adj = df_adj.set_index('datetime')
                data = data.merge(df_adj, how='left', left_index=True, right_index=True)
                data['adj_factor'] = data['adj_factor'].fillna(method='bfill')
                for col in ['open', 'close', 'high', 'low']:
                    if adj == 'qfq':
                        data[col] = data[col] * data['adj_factor'] / float(df_adj['adj_factor'][0])
                    else:
                        data[col] = data[col] * data['adj_factor']  # data[col] = data[col].map(lambda x: '%.2f' % x)   # 会引起类型转换，从float转换成str
            # 计算换手率
            cursor = connection.cursor()
            cursor.execute('select outstanding from stock_stockbasicinfo where code="{0}"'.format(code))
            outstanding = cursor.fetchone()[0] * 10 ** 8
            data['outstanding'] = outstanding
            data['turnover'] = data['vol'] / data['outstanding'] * 100
            # 计算涨跌幅
            data['pre_close'] = data['close'].shift(-1)
            data['change_rate'] = (data['close'] - data['pre_close']) / data['pre_close'] * 100
            data = data.dropna()
            data = data[
                ['code', 'pre_close', 'open', 'close', 'high', 'low', 'vol', 'amount', 'change_rate', 'turnover',
                 'outstanding']]
            return data
    
    def __get_trade_money(self, code,days=10):
        # 个股资金流入URL
        stock_money_url = 'http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id={0}{1}'
        mkcode = 1 if code.startswith('6') else 2
    
        res = requests.get(stock_money_url.format(code,mkcode),headers=get_user_agent_dict())
        # 数据清洗
        money_datas = json.loads(res.text.strip().lstrip('(').rstrip(')'))
        money_datas = [data.split(',') for data in money_datas]
        money_datas = money_datas[-days:]
        # 利用正则表达式，将数据中的'-'替换成0
        regex = re.compile(r'^-$')
        money_datas = [['0' if regex.match(m) else m for m in money]for money in money_datas]
        money_datas = [data[:11] for data in money_datas]
        money_datas = [[[float(m.rstrip('%')) if m.endswith('%') else float(m) * 10 ** 4 for m in money[1:]], money[0]] for money in money_datas]
        m_datas = []
        for money in money_datas:
            m = []
            m.extend(money[0])
            m.append(money[1])
            m_datas.append(m)
        col_list = ['main_money','main_money_rate','super_money','super_money_rate','large_money','large_money_rate','midden_money','midden_money_rate','small_money','small_money_rate','datetime']
        df_money = pd.DataFrame(m_datas,columns=col_list)
        df_money['datetime'] = pd.to_datetime(df_money['datetime'])
        df_money = df_money.set_index('datetime')
        # df_money['code'] = code
        df_money = df_money.sort_index(ascending=False)
        return df_money
    
    def __trade_his_to_db(self,data):
        last_date = data.index[-1]
        # 删除已存在的数据
        StockTradeMoneyHis.objects.filter(code=data['code'][0],trade_date__gte=last_date).delete()
        stock_trade_list = []
        for index in data.index:
            '''
            code                  object
            pre_close            float64
            open                 float64
            close                float64
            high                 float64
            low                  float64
            vol                  float64
            amount               float64
            change_rate          float64
            turnover             float64
            outstanding          float64
            main_money           float64
            main_money_rate      float64
            super_money          float64
            super_money_rate     float64
            large_money          float64
            large_money_rate     float64
            midden_money         float64
            midden_money_rate    float64
            small_money          float64
            small_money_rate     float64
            '''
            row = data.ix[index]
            stock_trade = StockTradeMoneyHis()
            stock_trade.code = row['code']
            stock_trade.name = row['name']
            stock_trade.trade_date = index
            stock_trade.pre_close = row['pre_close']
            stock_trade.open = row['open']
            stock_trade.close = row['close']
            stock_trade.high = row['high']
            stock_trade.low = row['low']
            stock_trade.vol = row['vol']
            stock_trade.amount = row['amount']
            stock_trade.change_rate = row['change_rate']
            stock_trade.turnover = row['turnover']
            stock_trade.outstanding = row['outstanding']
            stock_trade.main_money = row['main_money']
            stock_trade.main_money_rate = row['main_money_rate']
            stock_trade.super_money = row['super_money']
            stock_trade.super_money_rate = row['super_money_rate']
            stock_trade.large_money = row['large_money']
            stock_trade.large_money_rate = row['large_money_rate']
            stock_trade.midden_money = row['midden_money']
            stock_trade.midden_money_rate = row['midden_money_rate']
            stock_trade.small_money = row['small_money']
            stock_trade.small_money_rate = row['small_money_rate']
            stock_trade_list.append(stock_trade)
        StockTradeMoneyHis.objects.bulk_create(stock_trade_list)
    
    def __get_trade_today_last(self):
        # 获取个股当日交易信息
        stock_trade_today_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=5000&js=var%20FVuEefaj={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'
        content = requests.get(stock_trade_today_url,headers=get_user_agent_dict()).text
        content = content.lstrip('var FVuEefaj=').strip()
        content_json = demjson.decode(content)
        stocks = [stock.split(',') for stock in content_json.get('rank')]
        
        # 处理空值的正则表达式
        regex_null = re.compile(r'^-$')
        # 存储最终结果
        
        result_list = []
        for stock in stocks:
            stock_name = stock[1:3]                     # 获取个股代码、名称
            stock_trade = stock[3:13]                   # 获取行情数据
            stock_trade_tmp = stock[21:25]              # 获取行情数据
            stock_timetomarket = stock[-1]              # 获取上市日期
            stock_trade.extend(stock_trade_tmp)         # 将2段行情数据连接
            
            # 处理空值
            stock_trade = list(map(lambda x: '0' if regex_null.match(x) else x, stock_trade))
            # 去掉%
            stock_trade = [item.strip().rstrip('%') for item in stock_trade]
            # 转换成数字
            stock_trade = [float(item) for item in stock_trade]
            # 转换交易量单位，将手转换成股数
            stock_trade[4] *= 100
            
            # 处理上市日期
            stock_timetomarket = parse(stock_timetomarket)
            
            # 将3个列表连成1个列表，形成最终结果
            stock_name.extend(stock_trade)
            stock_name.append(stock_timetomarket)
            result = stock_name
            
            result_list.append(result)
        
        # 将数据封装成DataFrame
        df_result = pd.DataFrame(result_list,columns=['code','name','close','change_money','change_rate','zhenfu','vol','amount','pre_close','open','high','low','zhangdie_5min','liangbi','turnover','pe','timeToMarket'])
            
        return df_result

    def __get_money_today_last(self):
        # 当日个股资金流向数据
        stock_money_today_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=5000&js=var%20DuFASpGM={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA'
        content = requests.get(stock_money_today_url, headers=get_user_agent_dict()).text
        content = content.lstrip('var DuFASpGM=').strip()
        content_json = demjson.decode(content)
        stocks = [stock.split(',') for stock in content_json.get('data')]
        
        # 处理空值的正则表达式
        regex_null = re.compile(r'^-$')
        # 存储最终结果
        result_list = []
        
        for stock in stocks:
            stock_name = stock[1:3]         # 获取股票代码、名称
            stock_money = stock[5:15]       # 获取股票资金数据
            
            # 处理空值
            stock_money = list(map(lambda x: '0' if regex_null.match(x) else x, stock_money))
            # 去掉%
            stock_money = [item.strip().rstrip('%') for item in stock_money]
            # 转换成数字
            stock_money = [float(item) for item in stock_money]
            # 转换数据单位，原金额值的单位是万
            stock_money = list(map(lambda money: money[1]*10000 if money[0]%2==0 else money[1], enumerate(stock_money)))

            # 将2个列表连成1个列表，形成最终结果
            stock_name.extend(stock_money)
            result = stock_name
            
            result_list.append(result)
            
        # 将数据封装成DataFrame
        df_result = pd.DataFrame(result_list,columns=['code','name','main_money','main_money_rate','super_money','super_money_rate','large_money','large_money_rate','midden_money','midden_money_rate','small_money','small_money_rate'])
            
        return df_result
        
    def __trade_today_to_db(self,data):
        stock_trade_list = []
        for index in data.index:
            '''
            code                                     300742
            name                                        N越博
            close                                     33.61
            change_money                              10.27
            change_rate                                  44
            zhenfu                                    23.99
            vol                                       12400
            amount                                   415556
            pre_close                                 23.34
            open                                      28.01
            high                                      33.61
            low                                       28.01
            zhangdie_5min                                 0
            liangbi                                       0
            turnover                                   0.06
            pe                                            0
            timeToMarket                2018-05-08 00:00:00
            main_money                               211700
            main_money_rate                            51.3
            super_money                              211700
            super_money_rate                           51.3
            large_money                                   0
            large_money_rate                              0
            midden_money                             181500
            midden_money_rate                         43.97
            small_money                             -393200
            small_money_rate                         -95.27
            trade_date           2018-05-08 14:25:51.474365
            '''
            row = data.ix[index]
            stock_trade = StockTradeMoneyToday()
            stock_trade.code = row['code']
            stock_trade.name = row['name']
            stock_trade.trade_date = row['trade_date']
            stock_trade.timeToMarket = row['timeToMarket']
            stock_trade.close = row['close']
            stock_trade.change_money = row['change_money']
            stock_trade.change_rate = row['change_rate']
            stock_trade.zhen_rate = row['zhenfu']
            stock_trade.vol = row['vol']
            stock_trade.amount = row['amount']
            stock_trade.pre_close = row['pre_close']
            stock_trade.open = row['open']
            stock_trade.high = row['high']
            stock_trade.low = row['low']
            stock_trade.zhangdie_5min = row['zhangdie_5min']
            stock_trade.liangbi= row['liangbi']
            stock_trade.turnover = row['turnover']
            stock_trade.pe = row['pe']
            stock_trade.main_money = row['main_money']
            stock_trade.main_money_rate = row['main_money_rate']
            stock_trade.super_money = row['super_money']
            stock_trade.super_money_rate = row['super_money_rate']
            stock_trade.large_money = row['large_money']
            stock_trade.large_money_rate = row['large_money_rate']
            stock_trade.midden_money = row['midden_money']
            stock_trade.midden_money_rate = row['midden_money_rate']
            stock_trade.small_money = row['small_money']
            stock_trade.small_money_rate = row['small_money_rate']
            stock_trade_list.append(stock_trade)
            
        StockTradeMoneyToday.objects.bulk_create(stock_trade_list)
    
    
    





















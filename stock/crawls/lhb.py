import requests
import json
import re
from dateutil.parser import parse

from stock.crawls.crawlutils import get_user_agent_dict
from stock.models import LHBMainInfo


class LHBInfo:
    '''
    获取龙虎榜相关信息
    '''
    
    def get_lhb_main(self, start_date, end_date):
        '''
        获取指定日期的龙虎榜主表
        :param start_date:
        :param end_date:
        :return:
        '''
        main_url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=500,page=1,sortRule=-1,sortType=,' \
                   'startDate={0},endDate={1},gpfw=0,js=var%20data_tab_1.html'.format(start_date, end_date)
        
        res = requests.get(main_url, headers=get_user_agent_dict())
        concent = res.text.lstrip('var data_tab_1=').strip()
        concent_json = json.loads(concent)
        
        # 删除指定日期的龙虎榜主表数据
        LHBMainInfo.objects.filter(trade_date__gte=start_date,trade_date__lte=end_date).delete()
        if concent_json.get('success'):
            data = concent_json.get('data')
            regex = re.compile(r'^\s*$')
            lhb_stock_dict = {}
            for stock in data:
                code = stock.get('SCode')
                if code in lhb_stock_dict:
                    lhb_info = lhb_stock_dict.get(code)
                    lhb_info.reasons = ';;;'.join([lhb_info.reasons,stock.get('Ctypedes')])
                    lhb_info.jd = ';;;'.join([lhb_info.reasons,stock.get('JD')])
                else:
                    lhb_info = LHBMainInfo()
                    lhb_info.code = code
                    lhb_info.name = stock.get('SName')
                    lhb_info.trade_date = None if regex.match(stock.get('Tdate')) else parse(stock.get('Tdate'))
                    lhb_info.close = 0 if regex.match(stock.get('ClosePrice')) else float(stock.get('ClosePrice'))
                    lhb_info.change_rate = 0 if regex.match(stock.get('Chgradio')) else float(stock.get('Chgradio'))
                    lhb_info.turnover = 0 if regex.match(stock.get('Dchratio')) else float(stock.get('Dchratio'))
                    lhb_info.vol = 0 if regex.match(stock.get('Ntransac')) else float(stock.get('Ntransac'))
                    lhb_info.jm_money = 0 if regex.match(stock.get('JmMoney')) else float(stock.get('JmMoney'))
                    lhb_info.amount = 0 if regex.match(stock.get('Turnover')) else float(stock.get('Turnover'))
                    lhb_info.s_money = 0 if regex.match(stock.get('Smoney')) else float(stock.get('Smoney'))
                    lhb_info.b_money = 0 if regex.match(stock.get('Bmoney')) else float(stock.get('Bmoney'))
                    lhb_info.total_money = 0 if regex.match(stock.get('ZeMoney')) else float(stock.get('ZeMoney'))
                    lhb_info.jm_rate = 0 if regex.match(stock.get('JmRate')) else float(stock.get('JmRate'))
                    lhb_info.total_rate = 0 if regex.match(stock.get('ZeRate')) else float(stock.get('ZeRate'))
                    lhb_info.Ltsz = 0 if regex.match(stock.get('Ltsz')) else float(stock.get('Ltsz'))
                    lhb_info.rchange1m = 0 if regex.match(stock.get('Rchange1m')) else float(stock.get('Rchange1m'))
                    lhb_info.rchange3m = 0 if regex.match(stock.get('Rchange3m')) else float(stock.get('Rchange3m'))
                    lhb_info.rchange6m = 0 if regex.match(stock.get('Rchange6m')) else float(stock.get('Rchange6m'))
                    lhb_info.rchange1y = 0 if regex.match(stock.get('Rchange1y')) else float(stock.get('Rchange1y'))
                    lhb_info.reasons = stock.get('Ctypedes')
                    lhb_info.jd = stock.get('JD')
                lhb_stock_dict[code] = lhb_info
            LHBMainInfo.objects.bulk_create(lhb_stock_dict.values())
            
        
        














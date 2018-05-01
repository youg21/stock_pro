from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams

from stock.models import BankBasicInfo, StockBasicInfo


class BankInfo:
    '''
    BankInfo类，旨在获取与板块相关的一切数据，如板块资本资料数据、板块交易数据等
    '''
    
    def get_basic_info(self):
        pass
    
    def _get_bankinfo_tdx(self):
        '''
        通过通达信获取板块信息
        :return:
        '''
        # 创建TDX对象
        api = TdxHq_API()
        with api.connect('218.108.98.244', 7709):
            # 概念
            bank_gn = api.get_and_parse_block_info(TDXParams.BLOCK_GN)
            # 风格
            bank_fg = api.get_and_parse_block_info(TDXParams.BLOCK_FG)
            # 指数
            bank_zs = api.get_and_parse_block_info(TDXParams.BLOCK_SZ)
            
            bank_gn_list = []
            for bank in bank_gn:
                bank_gn_list.append([bank['blockname'], '概念', bank['code']])
            bank_fg_list = []
            for bank in bank_fg:
                bank_fg_list.append([bank['blockname'], '风格', bank['code']])
            bank_zs_list = []
            for bank in bank_zs:
                bank_zs_list.append([bank['blockname'], '指数', bank['code']])
            
            bank_gn_list.extend(bank_fg_list)
            bank_gn_list.extend(bank_zs_list)
            df_bank_stocks = pd.DataFrame(bank_gn_list, columns=['bank_name', 'bank_type', 'stock_code'])
            df_bank = df_bank_stocks[['bank_name', 'bank_type']].drop_duplicates()
            
            # 先删除原表数据
            BankBasicInfo.objects.all().delete()
            # 新增板块数据。每次更新板块数据，都要先删除旧数据，再重建新数据。因为板块内的个股是会变动的
            for bank in df_bank.values:
                # name stocks bank_type bank_desc
                bankinfo = BankBasicInfo()
                bankinfo.name = bank[0]
                bankinfo.bank_type = bank[1]
                bankinfo.bank_desc = bank[1]
                bankinfo.save()
                stocks = df_bank_stocks[df_bank_stocks['bank_name'] == bank[0]]
                bankinfo.stocks.set(StockBasicInfo.objects.filter(code__in=list(stocks['stock_code'])))

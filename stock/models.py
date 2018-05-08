from django.db import models


class StockBasicInfo(models.Model):
    '''
    个股基础信息
    '''
    code = models.CharField(max_length=32, verbose_name='个股代码')
    name = models.CharField(max_length=64, verbose_name='个股名称')
    industry = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    pe = models.FloatField(verbose_name='PE', default=0)
    outstanding = models.FloatField(verbose_name='流通股本', default=0)
    totals = models.FloatField(verbose_name='总股本', default=0)
    totalAssets = models.FloatField(verbose_name='总资产', default=0)
    liquidAssets = models.FloatField(verbose_name='流动资产', default=0)
    fixedAssets = models.FloatField(verbose_name='固定资产', default=0)
    reserved = models.FloatField(verbose_name='公积金', default=0)
    reservedPerShare = models.FloatField(verbose_name='每股公积金', default=0)
    esp = models.FloatField(verbose_name='每股收益', default=0)
    bvps = models.FloatField(verbose_name='每股净资', default=0)
    pb = models.FloatField(verbose_name='市净率', default=0)
    timeToMarket = models.DateField(verbose_name='上市日期', null=True, blank=True)
    undp = models.FloatField(verbose_name='未分利润', default=0)
    perundp = models.FloatField(verbose_name='每股未分配', default=0)
    rev = models.FloatField(verbose_name='收入同比', default=0)
    profit = models.FloatField(verbose_name='利润同比', default=0)
    gpr = models.FloatField(verbose_name='毛利率', default=0)
    npr = models.FloatField(verbose_name='净利润率', default=0)
    holders = models.FloatField(verbose_name='股东人数', default=0)
    
    def __str__(self):
        return '<StockBasicInfo symbol=%s name=%s>' % (self.code, self.name)


class BankBasicInfo(models.Model):
    '''
    板块基础信息
    '''
    # code = models.CharField(max_length=32,unique=True)        # 板块code
    name = models.CharField(max_length=64)  # 板块名称
    bank_type = models.CharField(max_length=64)  # 板块类别，值为行业、地区、概念、风格、指数
    bank_desc = models.CharField(max_length=1000, blank=True)  # 板块描述
    stocks = models.ManyToManyField('StockBasicInfo')  # 该板块下的个股
    
    def __str__(self):
        return '<BankInfo name=%s bank_type=%s>' % (self.name, self.bank_type)


class StockTradeMoneyHis(models.Model):
    code = models.CharField(max_length=32, verbose_name='个股代码')
    name = models.CharField(max_length=64, verbose_name='个股名称', null=True, blank=True)
    trade_date = models.DateField(verbose_name='交易日期', null=True, blank=True)
    open = models.FloatField(verbose_name='开盘价', default=0)
    high = models.FloatField(verbose_name='最高价', default=0)
    low = models.FloatField(verbose_name='最低价', default=0)
    close = models.FloatField(verbose_name='收盘价', default=0)
    change_rate = models.FloatField(verbose_name='涨跌幅', default=0)
    change_money = models.FloatField(verbose_name='涨跌额', default=0)
    zhen_rate = models.FloatField(verbose_name='振幅', default=0)
    liangbi = models.FloatField(verbose_name='量比', default=0)
    zhangdie_5min = models.FloatField(verbose_name='5分钟涨跌', default=0)
    pre_close = models.FloatField(verbose_name='昨日收盘价', default=0)
    vol = models.FloatField(verbose_name='交易量', default=0)
    amount = models.FloatField(verbose_name='交易额', default=0)
    turnover = models.FloatField(verbose_name='换手率', default=0)
    outstanding = models.FloatField(verbose_name='流通值', default=0)
    mktcap = models.FloatField(verbose_name='总市值', default=0)
    pe = models.FloatField(verbose_name='市盈率', default=0)
    pb = models.FloatField(verbose_name='市净率', default=0)
    timeToMarket = models.DateField(verbose_name='上市日期', null=True, blank=True)
    main_money = models.FloatField(verbose_name='主力净流入', default=0)
    main_money_rate = models.FloatField(verbose_name='主力净流入占比', default=0)
    super_money = models.FloatField(verbose_name='超大单净流入', default=0)
    super_money_rate = models.FloatField(verbose_name='超大单净流入占比', default=0)
    large_money = models.FloatField(verbose_name='大单净流入', default=0)
    large_money_rate = models.FloatField(verbose_name='大单净流入占比', default=0)
    midden_money = models.FloatField(verbose_name='中单净流入', default=0)
    midden_money_rate = models.FloatField(verbose_name='中单净流入占比', default=0)
    small_money = models.FloatField(verbose_name='小单净流入', default=0)
    small_money_rate = models.FloatField(verbose_name='小单净流入占比', default=0)


class StockTradeMoneyToday(models.Model):
    code = models.CharField(max_length=32, verbose_name='个股代码')
    name = models.CharField(max_length=64, verbose_name='个股名称', null=True, blank=True)
    trade_date = models.DateTimeField(verbose_name='交易日期', null=True, blank=True)
    open = models.FloatField(verbose_name='开盘价', default=0)
    high = models.FloatField(verbose_name='最高价', default=0)
    low = models.FloatField(verbose_name='最低价', default=0)
    close = models.FloatField(verbose_name='收盘价', default=0)
    change_rate = models.FloatField(verbose_name='涨跌幅', default=0)
    change_money = models.FloatField(verbose_name='涨跌额', default=0)
    zhen_rate = models.FloatField(verbose_name='振幅', default=0)
    liangbi = models.FloatField(verbose_name='量比', default=0)
    zhangdie_5min = models.FloatField(verbose_name='5分钟涨跌', default=0)
    pre_close = models.FloatField(verbose_name='昨日收盘价', default=0)
    vol = models.FloatField(verbose_name='交易量', default=0)
    amount = models.FloatField(verbose_name='交易额', default=0)
    turnover = models.FloatField(verbose_name='换手率', default=0)
    outstanding = models.FloatField(verbose_name='流通值', default=0)
    mktcap = models.FloatField(verbose_name='总市值', default=0)
    pe = models.FloatField(verbose_name='市盈率', default=0)
    pb = models.FloatField(verbose_name='市净率', default=0)
    timeToMarket = models.DateField(verbose_name='上市日期', null=True, blank=True)
    main_money = models.FloatField(verbose_name='主力净流入', default=0)
    main_money_rate = models.FloatField(verbose_name='主力净流入占比', default=0)
    super_money = models.FloatField(verbose_name='超大单净流入', default=0)
    super_money_rate = models.FloatField(verbose_name='超大单净流入占比', default=0)
    large_money = models.FloatField(verbose_name='大单净流入', default=0)
    large_money_rate = models.FloatField(verbose_name='大单净流入占比', default=0)
    midden_money = models.FloatField(verbose_name='中单净流入', default=0)
    midden_money_rate = models.FloatField(verbose_name='中单净流入占比', default=0)
    small_money = models.FloatField(verbose_name='小单净流入', default=0)
    small_money_rate = models.FloatField(verbose_name='小单净流入占比', default=0)


class LHBMainInfo(models.Model):
    '''
    '''
    code = models.CharField(max_length=32, verbose_name='个股代码')
    name = models.CharField(max_length=64, verbose_name='个股名称')
    trade_date = models.DateField(verbose_name='交易日期', null=True, blank=True)
    close = models.FloatField(verbose_name='收盘价', default=0)
    change_rate = models.FloatField(verbose_name='涨跌幅', default=0)
    vol = models.FloatField(verbose_name='成交量', default=0)
    turnover = models.FloatField(verbose_name='换手率', default=0)
    jm_money = models.FloatField(verbose_name='龙虎榜净买额', default=0)
    amount = models.FloatField(verbose_name='市场总成交额', default=0)
    s_money = models.FloatField(verbose_name='龙虎榜卖出额', default=0)
    b_money = models.FloatField(verbose_name='龙虎榜买入额', default=0)
    total_money = models.FloatField(verbose_name='龙虎榜成交额', default=0)
    jm_rate = models.FloatField(verbose_name='龙虎榜净买额占总成交比', default=0)
    total_rate = models.FloatField(verbose_name='龙虎榜成交额占总成交比', default=0)
    Ltsz = models.FloatField(verbose_name='流通市值', default=0)
    rchange1m = models.FloatField(verbose_name='近一个月涨幅', default=0)
    rchange3m = models.FloatField(verbose_name='近三个月涨幅', default=0)
    rchange6m = models.FloatField(verbose_name='近六个月涨幅', default=0)
    rchange1y = models.FloatField(verbose_name='近一年涨幅', default=0)
    reasons = models.CharField(max_length=255, verbose_name='上榜原因')
    jd = models.CharField(max_length=255, verbose_name='解读')
    





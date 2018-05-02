import tushare as ts
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams

api = TdxHq_API()
with api.connect('218.108.98.244', 7709):
    data = api.get_security_bars(TDXParams.KLINE_TYPE_DAILY, 0, '000001', 0, 10)
    
    for line in data:
        print(line)
    
    
    
    
    
    
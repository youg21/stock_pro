import tushare as ts
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams

# api = TdxHq_API()
# with api.connect('218.108.98.244', 7709):
#     data = api.get_security_bars(TDXParams.KLINE_TYPE_DAILY, 0, '000001', 0, 10)
#
#     for line in data:
#         print(line)
#
aaa = [['2018-04-27', '-85229.1696', '-29.01%', '-69703.8448', '-23.73%', '-15525.3248', '-5.28%', '36414.4608', '12.39%', '48814.7077', '16.62%'], ['2018-05-02', '-953.12', '-0.76%', '1705.4752', '1.35%', '-2658.5952', '-2.11%', '-4096.1232', '-3.25%', '5049.2429', '4.01%']]

# dd = [[[a for a in aa[1:]],aa[0]] for aa in aaa]
dd = [[[float(a.rstrip('%')) if a.endswith('%') else float(a)*10**4 for a in aa[1:]],aa[0]] for aa in aaa]

for d in dd:
    print(d)
print('====================')
# dd = [d[0].append(d[1])for d in dd]
cc = []
for d in dd:
    print(d[0])
    print(d[1])
    cc.extend(d[0])
    cc.append(d[1])
    break
print('=======================')
print(cc)










    
    
    
    
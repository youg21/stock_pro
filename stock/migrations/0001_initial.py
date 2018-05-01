# Generated by Django 2.0.2 on 2018-05-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankBasicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('bank_type', models.CharField(max_length=64)),
                ('bank_desc', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='StockBasicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, verbose_name='个股代码')),
                ('name', models.CharField(max_length=64, verbose_name='个股名称')),
                ('industry', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('pe', models.FloatField(default=0, verbose_name='PE')),
                ('outstanding', models.FloatField(default=0, verbose_name='流通股本')),
                ('totals', models.FloatField(default=0, verbose_name='总股本')),
                ('totalAssets', models.FloatField(default=0, verbose_name='总资产')),
                ('liquidAssets', models.FloatField(default=0, verbose_name='流动资产')),
                ('fixedAssets', models.FloatField(default=0, verbose_name='固定资产')),
                ('reserved', models.FloatField(default=0, verbose_name='公积金')),
                ('reservedPerShare', models.FloatField(default=0, verbose_name='每股公积金')),
                ('esp', models.FloatField(default=0, verbose_name='每股收益')),
                ('bvps', models.FloatField(default=0, verbose_name='每股净资')),
                ('pb', models.FloatField(default=0, verbose_name='市净率')),
                ('timeToMarket', models.DateField(blank=True, null=True, verbose_name='上市日期')),
                ('undp', models.FloatField(default=0, verbose_name='未分利润')),
                ('perundp', models.FloatField(default=0, verbose_name='每股未分配')),
                ('rev', models.FloatField(default=0, verbose_name='收入同比')),
                ('profit', models.FloatField(default=0, verbose_name='利润同比')),
                ('gpr', models.FloatField(default=0, verbose_name='毛利率')),
                ('npr', models.FloatField(default=0, verbose_name='净利润率')),
                ('holders', models.FloatField(default=0, verbose_name='股东人数')),
            ],
        ),
        migrations.CreateModel(
            name='StockTradeMoneyHis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, verbose_name='个股代码')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='个股名称')),
                ('trade_date', models.DateField(blank=True, null=True, verbose_name='交易日期')),
                ('open', models.FloatField(default=0, verbose_name='开盘价')),
                ('high', models.FloatField(default=0, verbose_name='最高价')),
                ('low', models.FloatField(default=0, verbose_name='最低价')),
                ('close', models.FloatField(default=0, verbose_name='收盘价')),
                ('change_rate', models.FloatField(default=0, verbose_name='涨跌幅')),
                ('zhen_rate', models.FloatField(default=0, verbose_name='振幅')),
                ('liangbi', models.FloatField(default=0, verbose_name='量比')),
                ('pre_close', models.FloatField(default=0, verbose_name='昨日收盘价')),
                ('vol', models.FloatField(default=0, verbose_name='交易量')),
                ('amount', models.FloatField(default=0, verbose_name='交易额')),
                ('turnover', models.FloatField(default=0, verbose_name='换手率')),
                ('outstanding', models.FloatField(default=0, verbose_name='流通值')),
                ('mktcap', models.FloatField(default=0, verbose_name='总市值')),
                ('pe', models.FloatField(default=0, verbose_name='市盈率')),
                ('pb', models.FloatField(default=0, verbose_name='市净率')),
                ('main_money', models.FloatField(default=0, verbose_name='主力净流入')),
                ('main_money_rate', models.FloatField(default=0, verbose_name='主力净流入占比')),
                ('super_money', models.FloatField(default=0, verbose_name='超大单净流入')),
                ('super_money_rate', models.FloatField(default=0, verbose_name='超大单净流入占比')),
                ('large_money', models.FloatField(default=0, verbose_name='大单净流入')),
                ('large_money_rate', models.FloatField(default=0, verbose_name='大单净流入占比')),
                ('midden_money', models.FloatField(default=0, verbose_name='中单净流入')),
                ('midden_money_rate', models.FloatField(default=0, verbose_name='中单净流入占比')),
                ('small_money', models.FloatField(default=0, verbose_name='小单净流入')),
                ('small_money_rate', models.FloatField(default=0, verbose_name='小单净流入占比')),
            ],
        ),
        migrations.AddField(
            model_name='bankbasicinfo',
            name='stocks',
            field=models.ManyToManyField(to='stock.StockBasicInfo'),
        ),
    ]
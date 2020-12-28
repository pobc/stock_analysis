import akshare as ak
from utils.DBUtils import DBUtils

"""
统计3年上市的可转债对应的股票的价格
https://www.akshare.xyz/zh_CN/latest/data/stock/stock.html

https://www.aipo.org/aipo/ipohistory

绿鞋保护200%左右的，都在涨
"""


# 查询4年内的可转债，11月之前的
def query_bond_stock_codes_save():
    bond_infos = DBUtils.execute("select 正股代码, 申购日期, 交易场所 from kezhuanzhai "
                                 "where 申购日期>'2015-01-01' and 申购日期< '2020-11-01' order by 正股代码")
    for data in bond_infos:
        stock_code = str(data["交易场所"][-2:]).lower() + data['正股代码']
        print(data['正股代码'])
        stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol=stock_code,
                                                      adjust="qfq")
        for index, stock_price in stock_zh_a_daily_hfq_df.iterrows():
            if stock_price["open"] == 'nan' or stock_price["volume"] == 'nan':
                continue
            save_stock_price_info({"date": index, **dict(stock_price), "stock_code": data['正股代码']})

def query_stock_codes_save():
    stock_infos = DBUtils.execute("select * from stock_2020_1218")
    for data in stock_infos:
        print(data['symbol'])
        stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol=data['symbol'],
                                                      adjust="qfq")
        for index, stock_price in stock_zh_a_daily_hfq_df.iterrows():
            if stock_price["open"] == 'nan' or stock_price["volume"] == 'nan':
                continue
            save_stock_price_info({"date": index, **dict(stock_price), "stock_code": data['symbol']})


def query_stock_codes(stock_code: str = "sh603776"):
    print(stock_code)
    stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
    for index, stock_price in stock_zh_a_daily_hfq_df.iterrows():
        print(index, stock_price)


def save_stock_price_info(stock_price={}):
    result = DBUtils.execute(
        "insert into stock_day_qfq(date,close,high,low,open,volume,outstanding_share,turnover,stock_code) "
        " values ('{date}',{close},{high},{low},{open},{volume},{outstanding_share},{turnover},'{stock_code}')".format(
            **stock_price))
    if result is None or result <= 0:
        print(stock_price)

# 查询实时行情数据
def query_RT_stock():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    for index, stock_data_info in stock_zh_a_spot_df.iterrows():
        result = DBUtils.execute("INSERT INTO `stock_2020_1218`(`symbol`,`code`,`name`)"
                        "VALUES('{symbol}','{code}','{name}')".format(**dict(stock_data_info)))
        if result is None or result <= 0:
            print(stock_data_info)


if __name__ == "__main__":
    query_stock_codes_save()

import akshare as ak
from utils.DBUtils import DBUtils as DBUtils


    # https://www.akshare.xyz/zh_CN/latest/data/bond/bond.html#id17

def save_bond_data_info(kezhuanzhai_code='sh110003'):
    print(kezhuanzhai_code)
    # 查询每个转债的信息，存入数据库
    bond_zh_hs_cov_daily_df = ak.bond_zh_hs_cov_daily(symbol=kezhuanzhai_code)
    for index, row in bond_zh_hs_cov_daily_df.iterrows():
        print(index, row['open'], row['high'], row['low'], row['close'], row['volume'])
        DBUtils.execute("insert into kezhuanzhai_data(date,open,high,low,close,volume,bond_code) values "
                        "('{date}',{open},{high},{low},{close},{volume},{bond_code})".format(**{"date": index},
                                                                                             **dict(row), **{
                "bond_code": kezhuanzhai_code[2:]}))


def query_kezhuanzhai_info():
    # 查询所有转债的信息
    kezhuanzhai_infos = DBUtils.execute("select * from kezhuanzhai where 上市时间 <'2020-11-30T00:00:00' and "
                                        " 债券代码 not in (select bond_code from kezhuanzhai_data group by bond_code) and length(上市时间)>5 ")
    for data in kezhuanzhai_infos:
        save_bond_data_info(str(data["交易场所"][-2:]).lower() + data['债券代码'])


def save_bond_info():
    # 查询 保存所有转债的信息
    bond_zh_cov_df = ak.bond_zh_cov()
    for index, row in bond_zh_cov_df.iterrows():
        DBUtils.execute("insert into kezhuanzhai(`债券代码`,`交易场所`,`债券简称`,`申购日期`,`申购代码`,"
                        "`正股代码`,`正股简称`,`债券面值`,`发行价格`,`转股价`,`中签号发布日`,`中签率`,`上市时间`"
                        ",`备忘录`,`正股价`,`市场类型`,`股权登记日`,`申购上限`,`转股价值`,`债现价`,`转股溢价率`"
                        ",`每股配售额`,`发行规模`) "
                        "values('{债券代码}','{交易场所}','{债券简称}','{申购日期}','{申购代码}','{正股代码}',"
                        "'{正股简称}','{债券面值}','{发行价格}','{转股价}','{中签号发布日}','{中签率}','{上市时间}',"
                        "'{备忘录}','{正股价}','{市场类型}','{股权登记日}','{申购上限}','{转股价值}','{债现价}','"
                        "{转股溢价率}','{每股配售额}','{发行规模}')"
                        .format(**dict(row)))


if __name__ == "__main__":
    # print("CNSESH"[-2:])
    query_kezhuanzhai_info()

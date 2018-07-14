import tushare as ts
import openpyxl


# 下载近一年沪深指数if8888,只保存收盘价到excel(路径:c:/if.xlsx)
def download():
    cons = ts.get_apis()
    df = ts.bar('ifl9', conn=cons, asset='X', start_date='2017-6-24', end_date='')
    df1 = df[['close']]
    df1.to_excel('c:/if.xlsx')


import pandas as pd
import numpy as np


# 读取xls文件,修改datetim为date
def read_xls():
    # 使用pandas读取excel文件
    data = pd.ExcelFile('if.xls')
    # 显示出读入excel文件中的表名字
    name = data.sheet_names
    data = data.parse('Sheet1')
    date_line = list(data['date'])
    close_line = list(data['close'])
    # 计算日收益率(G3 - G2) / G2,
    data['return'] = (data['close'].shift(-1) - data['close']) / data['close']
    return_line = list(data['return'])
    return date_line, close_line, return_line


# 参考:
# https://blog.csdn.net/xingbuxing_py/article/details/78526117
# https://blog.csdn.net/bartonpd/article/details/51488343


# 计算年化收益率函数
def annual_return(date_line, close_line):
    """
    date_line: 日期序列
    close_line: 账户价值序列
    return: 输出在回测期间的年化收益率
    """
    # 将数据序列合并成dataframe并按日期排序
    df = pd.DataFrame({'date': date_line, 'close': close_line})
    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    rng = pd.period_range(df['date'].iloc[0], df['date'].iloc[-1], freq='D')
    # 计算年化收益率
    annual = pow(df.ix[len(df.index) - 1, 'close'] / df.ix[0, 'close'], 250 / len(rng)) - 1
    print('年化收益率为：{}'.format(annual))
    text1 = '年化收益率为：{}'.format(annual)
    return text1


# 计算最大回撤函数
def max_drawdown(date_line, close_line):
    """
    date_line: 日期序列
    capital_line: 账户价值序列
    输出最大回撤及开始日期和结束日期
    """
    # 将数据序列合并为一个dataframe并按日期排序
    df = pd.DataFrame({'date': date_line, 'close': close_line})
    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 计算当日之前的账户最大价值
    df['max2here'] = pd.expanding_max(df['close'])
    # 计算当日的回撤
    df['dd2here'] = df['close'] / df['max2here'] - 1

    # 计算最大回撤和结束时间
    temp = df.sort_values(by='dd2here').iloc[0][['date', 'dd2here']]
    max_dd = temp['dd2here']
    end_date = temp['date']

    # 计算开始时间
    df = df[df['date'] <= end_date]
    text2 = '最大回撤为：{}'.format(max_dd)
    print('最大回撤为：{}'.format(max_dd))
    return text2


# 最大连续下跌天数
def max_successive_up(date_line, return_line):
    """
    date_line: 日期序列
    return_line: 账户日收益率序列
    输出最大连续上涨天数和最大连续下跌天数
    """
    df = pd.DataFrame({'date': date_line, 'rtn': return_line})
    # 新建一个全为空值的series,并作为dataframe新的一列
    s = pd.Series(np.nan, index=df.index)
    s.name = 'up'
    df = pd.concat([df, s], axis=1)

    # 当收益率大于0时，up取1，小于0时，up取0，等于0时采用前向差值
    df.ix[df['rtn'] > 0, 'up'] = 1
    df.ix[df['rtn'] < 0, 'up'] = 0
    df['up'].fillna(method='ffill', inplace=True)

    # 根据up这一列计算到某天为止连续上涨下跌的天数
    rtn_list = list(df['up'])
    successive_up_list = []
    num = 1
    for i in range(len(rtn_list)):
        if i == 0:
            successive_up_list.append(num)
        else:
            if (rtn_list[i] == rtn_list[i - 1] == 1) or (rtn_list[i] == rtn_list[i - 1] == 0):
                num += 1
            else:
                num = 1
            successive_up_list.append(num)
    # 将计算结果赋给新的一列'successive_up'
    df['successive_up'] = successive_up_list
    # 分别在上涨和下跌的两个dataframe里按照'successive_up'的值排序并取最大值
    max_successive_down = df[df['up'] == 0].sort_values(by='successive_up', ascending=False)['successive_up'].iloc[0]
    print('最大连续下跌天数为：{}'.format(max_successive_down))
    text3 = '最大连续下跌天数为：{}'.format(max_successive_down)
    return text3


import random


# 涨跌停7%的限制,模拟指数
def index_simulation():
    close1 = 3638.600098
    close_list = [close1]
    n = 0
    while n < 243:  # 243
        # 由于极端行情出现频率低,采用随机正态浮点数
        x = random.uniform(0.93, 1.07)
        close_new = close_list[n] * x
        close_list.append(close_new)
        n += 1
    df = pd.DataFrame({'close': close_list})
    x, y, z = read_xls()
    # 计算日收益率(G3 - G2) / G2
    df['return'] = (df['close'].shift(-1) - df['close']) / df['close']
    return_line = list(df['return'])
    write_txt(annual_return(x, close_list))
    write_txt(max_drawdown(x, close_list))
    write_txt(max_successive_up(x, return_line))
    write_txt('#################################################')
    print('#################################################')


# 模拟10个if指数
def simulate():
    for i in range(10):
        index_simulation()


# 写入数列和结果到文本
def write_txt(text):
    with open('result11.txt', 'a') as file:
        file.write('\n' + text)


# 计算if8888
def if8888():
    x, y, z = read_xls()
    write_txt(annual_return(x, y))
    write_txt(max_drawdown(x, y))
    write_txt(max_successive_up(x, z))
    write_txt('#################################################')


if __name__ == '__main__':
    # if8888的计算
    if8888()
    # 其他10个的计算
    simulate()

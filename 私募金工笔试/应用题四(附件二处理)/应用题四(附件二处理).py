import xlrd
import json
from pymongo import MongoClient
import os
import re

# 连接数据库
client = MongoClient('localhost', 27017)
db = client.stock_list
coll = db.ROE


# 返回文件夹下所有formats路径
def file_name(file_dir, formats):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.{}'.format(formats):
                L.append(file_dir + '\\' + file)
    return L


# 数据处理及存如mongodb
def excle_mongo():
    file_dir = 'F:\\BaiduYunDownload\\下半部\\君道笔试\\应用题四(附件二处理)'
    formats = 'xlsx'
    xlsx_list = file_name(file_dir, formats)
    for fname in xlsx_list:
        data = xlrd.open_workbook(fname)
        table = data.sheets()[0]
        print('table', table)
        # 读取excel第一行作为存入mongodb的字段名
        rowstag = table.row_values(0)
        print('rowstag', rowstag)
        # 构造新表头
        new_rowstag = []
        for i in rowstag:
            if '证券' in i:
                t = i.replace('↑', '')
            else:
                t = re.sub('[净资产收益率ROE(扣除/加权)\r\n\[报告期\] 年报\r\n\[单位\] %]', '', i)
            new_rowstag.append(t)
        print('new', new_rowstag)
        nrows = table.nrows
        # ncols=table.nrows
        # print('rowstag',rowstag)
        # print('nrows',nrows)
        # print('ncols',ncols)
        returnData = {}
        for i in range(1, nrows):
            # zip打包为元组的列表,
            row_values = table.row_values(i)
            # row_values.append(v)
            print('row', row_values)
            # 处理代码后的.SZ和.SH
            row_values[0] = row_values[0][:-3]
            print(row_values)
            returnData[i] = json.dumps(dict(zip(new_rowstag, row_values)))
            # 转换为字典,转换为json格式,通过编解码还原数据
            returnData[i] = json.loads(returnData[i])
            print(returnData[i])
            coll.insert(returnData[i])


if __name__ == '__main__':
    excle_mongo()

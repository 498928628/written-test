'''
1.第一题
# Javascript（需要使用JQuery包）的例程如下： $(function () {
#     $.get( "test.php", function( data ) {
#         $( "body" ).append( "aaa" );
#     });
#     $("body").append("bbb");
# });
# 执行后显示为bbbaaa。要求改变这段代码的写法（功能不变），使显示结果变为aaabbb。但$("body").append("bbb");的执行位置不能调整，必须放在主函数的最末一句。


< html >
< head >
< script
type = "text/javascript"
src = "/jquery/jquery.js" > < / script >
< script
type = "text/javascript" >
$(document).ready(function()
{
$("button").click(function()
{
$("body").append(" aaa");
$("body").append(" bbb");
});
});
< / script >
< / head >
< body >
< button > 在body的结尾添加内容 < / button >
< / body >
< / html >

'''

# 2.第二题
# 写一个方法，把数字从一个字符串中提取出来。输入输出结果如下：输入：EUR 1.409,00；返回：1409。输入：$ 409,05；返回：409.05。输入：￥409.50；返回：409.5。输入：CNY 1,000；返回：1000。


# 识别币种（不区分大小写）
# 根据不同币种处理“ ，”
# 由于￥409.50没有空格不能用split
# python3

import re


def treat1(str):
    str = str.replace('.', '')
    str = str.replace(',', '.')
    return str


def treat2(str):
    str = str.replace(',', '.')
    return str


def treat3(str):
    str = str.replace(',', '.')
    return str


def treat4(str):
    str = re.sub(',', "", str)
    return str


cur = ['EUR', '\$', '￥', 'CNY']
cur_dict = {'EUR': treat1, '\$': treat2, '￥': treat3, 'CNY': treat4}

# 测试用例
test_list = ['EUR 1.409,00', '$ 409,05', '￥409.50', 'CNY 1,000', '* 10086']


def output(cur, str):
    for x in cur:
        if re.match(x, str):
            b = re.findall(r'\d+.\d+', str)
            f = re.findall(r"\d+\.?\d*", cur_dict[x](str))
            s = ['{:G}'.format(float(item)) for item in f]
            return s[0]


def test(test_list, cur):
    for i in test_list:
        print(output(cur, i))


if __name__ == '__main__':
    test(test_list, cur)


# 【加分题】一位程序猿想在[a, b]区间内找到 符合可以被一个整数c整除的整数个数； 例如，[0,20]中有3个整数能被7整除。现在你需要实现一段程序来统计区间内一共有多少个这样的数满足条件？
import math


def integer(a, b, c):
    if 1 <= c <= 500 and -50000 <= a <= b <= 50000:
        num_list = []
        for i in range(a, b + 1):
            if (i / c).is_integer():
                num_list.append(i)
        print(num_list)
        return len(num_list)

#测试
print(integer(0, 20, 7))

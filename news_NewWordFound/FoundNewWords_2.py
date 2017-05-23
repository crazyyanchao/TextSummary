# 	新词发现的信息熵方法与实现
import numpy as np
import pandas as pd
import re
from numpy import log, min
import pymysql

# 连接数据库
conn = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root',
                       passwd = '123456',db = 'news_5_23')
c = conn.cursor()

# 查询多条数据fetchAll(文件存在之后就不需要重复创建)
# c.execute("select content from event_news_ref into outfile '/var/lib/mysql-files/event_news_ref.txt'; ")
# r = c.fetchone()

f = open('/home/yanchao/PyCharmProject/TextSummary/event_news_ref.txt', 'r')  # 读取文章
s = f.read()  # 读取为一个字符串

# 定义要去掉的标点字或者字段
drop_dict = [u'，', u'\n', u'。', u'、', u'：', u'(', u')', u'[', u']', u'.', u',', u' ', u'\u3000', u'”', u'“', u'？', u'?',
             u'！', u'‘', u'’',u'(',u')',u'《',u'》', u'（',u'）',u'…',u'-',u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',
             u':',u'q',u'w',u'e',u'r',u't',u'y',u'u',u'i',u'o',u'u',u'p',u'a',u's',u'd',u'f',u'g',u'h',u'j',u'k',u'l',u'z',
             u'x',u'c',u'v',u'b',u'n',u'm',u'<',u'>',u'@',u'!',u'#',u'$',u'%',u'^',u'&',u'*',u'/',u'?',u'~',u'Q',u'W',u'E',
             u'R',u'T',u'Y',u'U',u'I',u'O',u'P',u'A',u'S',u'D',u'F',u'G','H',u'J',u'K',u'L',u'Z',u'X',u'C',u'V',u'B',u'N',u'M',
             u'【',u'】',u'|',u'à',u'╰',u'{',u'=',u';',u',',u'﹌﹌﹌']
for i in drop_dict:  # 去掉标点字或者字段
    s = s.replace(i, '')

# 为了方便调用，自定义了一个正则表达式的词典
myre = {2: '(..)', 3: '(...)', 4: '(....)', 5: '(.....)', 6: '(......)', 7: '(.......)'}

min_count = 10  # 录取词语最小出现次数
min_support = 30  # 录取词语最低支持度，1代表着随机组合
min_s = 3  # 录取词语最低信息熵，越大说明越有可能独立成词
max_sep = 4  # 候选词语的最大字数
t = []  # 保存结果用。

t.append(pd.Series(list(s)).value_counts())  # 逐字统计
tsum = t[0].sum()  # 统计总字数
rt = []  # 保存结果用

for m in range(2, max_sep + 1):
    print(u'正在生成%s字词...' % m)
    t.append([])
    for i in range(m):  # 生成所有可能的m字词
        t[m - 1] = t[m - 1] + re.findall(myre[m], s[i:])

    t[m - 1] = pd.Series(t[m - 1]).value_counts()  # 逐词统计
    t[m - 1] = t[m - 1][t[m - 1] > min_count]  # 最小次数筛选
    tt = t[m - 1][:]
    for k in range(m - 1):
        qq = np.array(list(map(lambda ms: tsum * t[m - 1][ms] / t[m - 2 - k][ms[:m - 1 - k]] / t[k][ms[m - 1 - k:]],
                               tt.index))) > min_support  # 最小支持度筛选。
        tt = tt[qq]
    rt.append(tt.index)


def cal_S(sl):  # 信息熵计算函数
    return -((sl / sl.sum()).apply(log) * sl / sl.sum()).sum()


for i in range(2, max_sep + 1):
    print(u'正在进行%s字词的最大熵筛选(%s)...' % (i, len(rt[i - 2])))
    pp = []  # 保存所有的左右邻结果
    for j in range(i):
        pp = pp + re.findall('(.)%s(.)' % myre[i], s[j:])
    pp = pd.DataFrame(pp).set_index(1).sort_index()  # 先排序，这个很重要，可以加快检索速度
    index = np.sort(np.intersect1d(rt[i - 2], pp.index))  # 作交集
    # 下面两句分别是左邻和右邻信息熵筛选
    index = index[np.array(list(map(lambda s: cal_S(pd.Series(pp[0][s]).value_counts()), index))) > min_s]
    rt[i - 2] = index[np.array(list(map(lambda s: cal_S(pd.Series(pp[2][s]).value_counts()), index))) > min_s]

# # 下面都是输出前处理
# for i in range(len(rt)):
#     t[i + 1] = t[i + 1][rt[i]]
#     t[i + 1].sort(ascending=False)

# 保存结果并输出
pd.DataFrame(pd.concat(t[1:])).to_csv('result.txt', header=False)

# 性能分析模块：
# python -m cProfile -o FoundNewWords_2.out FoundNewWords_2.
# 随机排序：
# python -m cProfile FoundNewWords.py
# 按耗时排序：
# python -c "import pstats; p=pstats.Stats('FoundNewWords_2.out'); p.sort_stats('time').print_stats()"



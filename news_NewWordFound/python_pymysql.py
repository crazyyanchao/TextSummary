#---------------------Python - PyMySQL---------------------------
# 支持Python3.6操作MySQL数据库的组件

import pymysql
import datetime,time

# 连接数据库
conn = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root',
                       passwd = '123456',db = 'news_5_23')
c = conn.cursor()

# # 创建表
# c.execute("create table test_datatypes (b bit,i int,l bigint,f real,s varchar(32),"
#           "u varchar(32),bb blob,d date,dt datetime,ts timestamp,td time,t time,st datetime)")

# # 插入数据
# v = (True, -3, 123456789012, 5.7, "hello'\" world", u"Espa\xc3\xb1ol",
#      "binary\x00data".encode(conn.charset), datetime.date(1988,2,2),
#      datetime.datetime.now(), datetime.timedelta(5,6),
#      datetime.time(16,32), time.localtime())
# c.execute("insert into test_datatypes (b,i,l,f,s,u,bb,d,dt,td,t,st) value "
#           "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",v)

# # 查询数据fetchOne
# c.execute("select b,i,l,f,s,u,bb,d,dt,td,t,st from test_datatypes")
# r = c.fetchone()  # 查询一条记录
# print(r)

# # 查询多条数据fetchAll
# c.execute("insert into test_datatypes (i, l) values (2,4), (6,8), 	(10,12)")
#
# c.execute("select l from test_datatypes where i in %s order by i",((2,6),))
# r = c.fetchall()

# # 删除数据
# c.execute("delete from test_datatypes")

# # 批量插入数据
# c.execute( """CREATE TABLE bulkinsert(
#               id int(11),
#               name char(20),
#               age int,
#               height int,
#               PRIMARY KEY (id)
#               )
#               """)
# data = [(0, "bob", 21, 123), (1, "jim", 56, 45), (2, "fred", 100, 180)]
# c.executemany("insert into bulkinsert (id, name, age, height) values (%s,%s,%s,%s)", data)
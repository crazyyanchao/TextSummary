# #-------------------python2.7连接MySQL数据库------------------------
#
# #!/usr/bin/env python
#
# import time
# import MySQLdb   # 不支持Python3
#
# #连接
# conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8")
# cursor = conn.cursor()
#
# #删除表
# sql = "drop table if exists user"
# cursor.execute(sql)
#
# #创建
# sql = "create table if not exists user(name varchar(128) primary key,created int(10))"
# cursor.execute(sql)
#
# #写入
# sql = "insert into user(name,created) values(%s,%s)"
# param = ("aaa",int(time.time()))
# n = cursor.execute(sql,param)
# print ('insert',n)
#
# #写入多行
# sql = "insert into user(name,created) values(%s,%s)"
# param = (("bbb",int(time.time())),("ccc",33),("ddd",44))
# print ('insertmany',n)
#
# #更新
# sql = "update user set name=%s where name='aaa'"
# param = ("zzz")
# n = cursor.execute(sql,param)
# print ('update',n)
#
# #查询
# n = cursor.execute("select * from user")
# for row in cursor.fetchall():
# 	print (row)
# 	for r in row:
# 		print (r)
#
# #删除 注意：MYSQL的占位符是s%
# sql = "delete from user where name=%s"
# param = ("bbb")
# n = cursor.execute(sql,param)
# print ('delete',n)
#
# #查询
# n = cursor.execute("select * from user")
# print (cursor.fetchall())
#
# cursor.close()
#
# #提交
# coon.commit()
# #关闭
# conn.close()
#
# # -------------------------------------------------------------
# # 以mysql或者sqlite为例，请用代码给出简洁且完整的数据库操作示例。注：请参考视频中的代码。
# # -------------------------------------------------------------
# # [参考代码：]
#
# # 导入MySQL驱动:
# import mysql
# from mysql import connector
#
# # import mysql.connector
# # 注意把password设为你的root口令:
# conn = mysql.connector.connect(user='root', password='password', database='test', use_unicode=True)
# cursor = conn.cursor()
# # 创建user表:
# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# # 插入一行记录，注意MySQL的占位符是%s:
# cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
#
# # 提交事务:
# conn.commit()
# cursor.close()
# # 运行查询:
# cursor = conn.cursor()
# cursor.execute('select * from user where id = %s', '1')
# values = cursor.fetchall()
# print (values)
#
# # 关闭Cursor和Connection:
# cursor.close()
# conn.close()

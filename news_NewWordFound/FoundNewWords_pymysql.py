import pymysql

# 连接数据库
conn = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root',
                       passwd = '123456',db = 'news_5_23')
c = conn.cursor()

# 查询多条数据fetchAll
c.execute("select content from event_news_ref into outfile '/var/lib/mysql-files/event_news_ref.txt'; ")
r = c.fetchone()
print(r)
# f = open('event_news_ref.txt', 'w')
print("write to .txt file!")
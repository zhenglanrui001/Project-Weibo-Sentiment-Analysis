import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='db_weibo',
    port=3306,
    charset='utf8mb4'
)

cursor = conn.cursor()

cursor.execute("SELECT VERSION()")
print(cursor.fetchone())

conn.close()
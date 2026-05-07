from pymysql import Connection


def getCon():
    """
    获取数据库连接
    :return:
    """
    con = Connection(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database="db_weibo",
        autocommit=True
    )

    return con


def closeCon(con):
    """
    关闭数据库连接
    :param con:
    :return:
    """
    con.close()

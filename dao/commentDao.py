"""
    微博评论信息，数据访问对象
"""
from utils import dbUtil


def getAllComment():
    """
        获取所有评论信息
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select * from t_comment where text_raw is not null"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)
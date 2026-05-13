"""
    微博数据访问对象
"""

from utils import dbUtil


def getTotalArticle():
    """
    获取微博总数
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select count(*) from t_article"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getTopAuthor():
    """
    获取点赞最高微博作者
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select authorName from t_article order by attitudes_count desc limit 0,1"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getTopRegion():
    """
    获取点赞最高城市
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select region_name, sum(attitudes_count) as ac from t_article where region_name is not null group by region_name order by ac desc limit 0,1"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getArticleTop6():
    """
    获取点赞top6
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select text_raw, attitudes_count from `t_article` where text_raw is not null order by attitudes_count desc limit 0,6"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def get7DayArticle():
    """
    获取最近7天点赞
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select date_format(created_at,'%Y-%m-%d') as articleDate, count(text_raw) as articleTotal from t_article group by articleDate order by articleDate desc limit 0,7"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


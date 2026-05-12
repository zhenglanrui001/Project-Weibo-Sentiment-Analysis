"""
    用户数据访问对象
"""
from datetime import datetime

from entity.User import User
from utils import dbUtil


def login(user: User):
    """
    登录判断
    :param user:
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"select * from t_user where username='{user.username}' and password='{user.password}'"
        cursor.execute(sql)
        return cursor.fetchone()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def add(user: User):
    """
    用户注册、添加
    :param user:
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"insert into t_user(username, password, createtime) values('{user.username}','{user.password}', '{datetime.now()}')"
        cursor.execute(sql)
        con.commit()
        return cursor.rowcount
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getByUserName(username):
    """
    根据用户名查询
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"select * from t_user where username='{username}' "
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        if con:
            con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)
"""
    爬数据，持久化到数据库
"""
import os
import traceback

import pandas as pd
from sqlalchemy import create_engine

from article import start as articleSpiderStart
from comment import start as commentSpiderStart

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/db_weibo?charset=utf8mb4')


def dataClean():
    """
    数据清洗
    :return:
    """
    pass


def saveTodb():
    """
    数据持久化
    先合并数据库和CSV文件，再去重，然后存数据库，最后删除CSV文件
    :return:
    """
    try:
        oldArticleDB = pd.read_sql('select * from t_article', con=engine)
        newArticleCSV = pd.read_csv('article_data.csv')
        concatArticle = pd.concat([oldArticleDB, newArticleCSV])
        resultArticle = concatArticle.drop_duplicates(subset='id', keep='last')
        resultArticle.to_sql('t_article', con=engine, if_exists='replace', index=False)

        oldCommentDB = pd.read_sql('select * from t_comment', con=engine)
        newCommentCSV = pd.read_csv('comment_data.csv')
        concatComment = pd.concat([oldCommentDB, newCommentCSV])
        resultComment = concatComment.drop_duplicates(subset='id', keep='last')
        resultComment.to_sql('t_comment', con=engine, if_exists='replace', index=False)

    except Exception as e:
        print('异常', e)
        traceback.print_exc()
        newArticleCSV = pd.read_csv('article_data.csv')
        newCommentCSV = pd.read_csv('comment_data.csv')

        newArticleCSV.to_sql('t_article', con=engine, if_exists='replace', index=False)
        newCommentCSV.to_sql('t_comment', con=engine, if_exists='replace', index=False)

    os.remove('article_data.csv')
    os.remove('comment_data.csv')


if __name__ == '__main__':
    print('微博内容爬取开始！')
    # articleSpiderStart()
    print('微博内容爬取结束！')

    print('微博评论爬取开始！')
    # commentSpiderStart()
    print('微博评论爬取结束！')

    print('数据清洗开始！')
    # dataClean()
    print('数据清洗结束！')

    print('数据持久化开始！')
    saveTodb()
    print('数据持久化结束！')
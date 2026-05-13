"""
    https://weibo.com/ajax/statuses/buildComments?id=5290832379773182&is_show_bulletin=2
    微博评论爬取 存CSV文件
"""
import csv
import os
import time
from datetime import datetime

import requests

from utils.stringUtil import clean_string


def init_csv():
    """
    初始化CSV文件
    :return:
    """
    if not os.path.exists("comment_data.csv"):
        with open("comment_data.csv", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                'id',  # 评论id
                'text_raw',  # 评论内容
                'created_at',  # 发布时间
                'source',  # 发布位置
                'like_counts',  # 点赞数
                'articleId',  # 微博id
                'userId',  # 用户id
                'userName',  # 用户名
                'gender',  # 性别
                'userHomeUrl',  # 评论用户主页
            ])


def getAllArticleList():
    """
    获取所有微博信息
    :return:
    """
    articleList = []
    with open('article_data.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for article in reader:
            articleList.append(article)
    return articleList


def getJsonHtml(url, params):
    """
    请求获取html内容，json格式
    :param url:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "referer": "https://weibo.com/102803",
        "cookie": "SCF=AvuehX7Rfiz9E7PwsRVGdkJkm6t0Km-Xqa4Fy0Dth-2dupmJhIMtVLg-_wR80xIW2c2PZAkVmjV3DDL3EQeSMLA.; _s_tentry=weibo.com; Apache=6596701156064.359.1777363611744; SINAGLOBAL=6596701156064.359.1777363611744; ULV=1777363611814:1:1:1:6596701156064.359.1777363611744:; XSRF-TOKEN=hf59qWqNyPB2JZouvzewAH2I; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5nW6q98Ou9vV-WM_CL7PUP5JpX5KMhUgL.FoqReKqRShzRShe2dJLoIEBLxK.L1KnLB.qLxKBLBonL1K.LxKBLBonL1K.LxKBLBonL1K.t; ALF=1781314858; SUB=_2A25HAVh6DeRhGeBG6lQZ9CzEzz-IHXVkf9WyrDV8PUJbkNANLXDBkW1NRjauA5UzINa-wrR5qix_EKMPakqw3EKS; WBPSESS=MIv-QR_yJFBFNxItr3xH5VHRuMhBgVBo2J5qMUR_Nev8M8yFrgZGTJLqyClKWqFYJo9VdXihjOMZ3CFtZDEfUCxRnkTLouS2LMvKZ69vUpc22yVZq7XyfbnbnjERxD1Uymqs1qrfVe29MqE3wI1SwA=="
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get json html")


def parseJson(json, articleId):
    """
    解析json
    :param jsonHtml:
    :param articleId:
    :return:
    """
    commentList = json['data']
    for comment in commentList:
        id = comment['id']
        text_raw = clean_string(comment['text_raw'])
        created_at = datetime.strptime(comment['created_at'], '%a %b %d %H:%M:%S %z %Y')
        source = comment.get('source', '').replace('来自', '').strip()
        like_counts = comment['like_counts']
        userId = comment['user']['id']
        userName = comment['user']['screen_name']
        gender = 'male'
        g = comment['user']['gender']
        if g == 'f':
            gender = 'female'
        userHomeUrl = 'https://weibo.com/u/%s' % userId

        writeToCsv([id, text_raw, created_at, source, like_counts, articleId, userId, userName, gender, userHomeUrl])


def writeToCsv(row):
    """
        追加写入CSV文件
        :param arcTypelist:
        :return:
    """
    with open('comment_data.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def start():
    url = "https://weibo.com/ajax/statuses/buildComments"
    init_csv()
    articleList = getAllArticleList()

    print("微博评论开始爬取")
    for article in articleList:
        print('正在爬取类型为:【%s】的数据' % article[0])
        time.sleep(1)

        # 最上方参数
        params = {
            "id": article[0],
            "is_show_bulletin": 2
        }

        jsonHtml = getJsonHtml(url, params)
        parseJson(jsonHtml, article[0])
    print("微博评论爬取结束")


if __name__ == '__main__':
    start()

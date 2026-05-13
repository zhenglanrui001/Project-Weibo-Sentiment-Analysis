"""
    https://weibo.com/ajax/feed/hottimeline?group_id=102803&containerid=102803&extparam=discover%7Cnew_feed
    微博内容爬取，存CSV文件
"""
import csv

import os
import time
from datetime import datetime

import requests

from utils.stringUtil import clean_string


def init_csv():
    """
    初始化操作，判断csv文件是否存在，不存在则创建
    :return:
    """
    if not os.path.exists('article_data.csv'):
        with open('article_data.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id',  # 文章id
                'text_raw',  # 内容
                'reposts_count',  # 转发数
                'comments_count',  # 评论数
                'attitudes_count',  # 点赞数
                'region_name',  # 发布位置
                'created_at',  # 发布时间
                'articleUrl',  # 文章链接
                'authorId',  # 作者id
                'authorName',  # 作者名
                'authorHomeUrl',  # 作者主页
                'articleType',  # 文章类型
            ])


def getAllTypeList():
    """
    获取所有文章类型
    :return:
    """
    allTypeList = []
    with open('arcType_data.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for articleType in reader:
            allTypeList.append(articleType)
    return allTypeList


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
        return "Failed to get json html"


def parseJson(json, articleType):
    """
    解析json
    :param json:
    :return:
    """
    articleList = json['statuses']
    for article in articleList:
        id = article['id']
        text_raw = clean_string(article['text_raw'])
        reposts_count = article['reposts_count']
        comments_count = article['comments_count']
        attitudes_count = article['attitudes_count']

        region_name = article.get('region_name', '').replace('发布于', '').strip()

        created_at = datetime.strptime(article['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        articleUrl = "https://weibo.com/%s%s" % (article['user']['id'], article['mblogid'])
        authorId = article['user']['id']
        authorName = article['user']['screen_name']
        authorHomeUrl = "https://weibo.com/u/%s" % authorId

        writeToCsv([id,
                    text_raw,
                    reposts_count,
                    comments_count,
                    attitudes_count,
                    region_name,
                    created_at,
                    articleUrl,
                    authorId,
                    authorName,
                    authorHomeUrl,
                    articleType])


def writeToCsv(row):
    """
        追加写入CSV文件
        :param arcTypelist:
        :return:
        """
    with open('article_data.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def start():
    init_csv()
    url = "https://weibo.com/ajax/feed/hottimeline"
    allTypeList = getAllTypeList()

    # print(allTypeList)

    print('微博内容开始爬取')
    for articleType in allTypeList:
        print('正在爬取类型为:【%s】的数据' % articleType[0])
        time.sleep(1)
        params = {
            "group_id": articleType[1],
            "containerid": articleType[2],
            "extparam": "discover|new_feed"
        }
        jsonHtml = getJsonHtml(url, params)
        parseJson(jsonHtml, articleType[0])
    print('微博内容爬取结束')


if __name__ == '__main__':
    """
        https://weibo.com/ajax/feed/hottimeline?group_id=102803&containerid=102803&extparam=discover%7Cnew_feed
    """
    start()

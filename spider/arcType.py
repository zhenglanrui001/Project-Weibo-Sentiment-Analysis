"""
    https://weibo.com/ajax/feed/allGroups
    微博类别信息爬取  存csv文件
"""
import csv
import os

import numpy as np
import requests


def init_csv():
    """
    初始化操作，判断csv文件是否存在，不存在则创建
    :return:
    """
    if not os.path.exists('arcType_data.csv'):
        with open('arcType_data.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                '类别标题(title)',
                '分组(gid)',
                '分类id(containerid)'
            ])


def getJsonHtml(url, params):
    """
    请求获取html内容，json格式
    :param url:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "referer": "https://weibo.com/102803",
        "cookie": "XSRF-TOKEN=Se8PkzAHX7II2j8_10x7sjL0; SCF=AvuehX7Rfiz9E7PwsRVGdkJkm6t0Km-Xqa4Fy0Dth-2dupmJhIMtVLg-_wR80xIW2c2PZAkVmjV3DDL3EQeSMLA.; SUB=_2A25E9Bo6DeRhGeBG6lQZ9CzEzz-IHXVniBPyrDV8PUNbmtB-LU3kkW9NRjauAyzSn33r_-d877dpC2HIbkpMNeAy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5nW6q98Ou9vV-WM_CL7PUP5NHD95Qc1h2c1hBE1hB0Ws4Dqcj.i--4iK.Ri-isi--Xi-zRiK.4i--Xi-zRiK.4i--Xi-zRiK.4; ALF=02_1779955563; _s_tentry=weibo.com; Apache=6596701156064.359.1777363611744; SINAGLOBAL=6596701156064.359.1777363611744; ULV=1777363611814:1:1:1:6596701156064.359.1777363611744:; PC_TOKEN=4bf70821ec; WBPSESS=MIv-QR_yJFBFNxItr3xH5VHRuMhBgVBo2J5qMUR_Nev8M8yFrgZGTJLqyClKWqFYJo9VdXihjOMZ3CFtZDEfUAjSIb7xNh7uEuSEKg8J3l5SkTI4AKKpulsjLuJki1fw8z_sV0Kebj80TKpYBOW2lQ==",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to get json html"


def writeToCsv(row):
        """
        追加写入CSV文件
        :param arcTypelist:
        :return:
        """
        with open('arcType_data.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)



def parseJson(json):
    """
    解析JSON数据
    :param jsonHtml:
    :return:
    """
    arcTypelist = np.append(json['groups'][3]['group'], json['groups'][4]['group'])

    # print(arcTypelist)

    for arcType in arcTypelist:
        arcType_title = arcType['title']
        gid = arcType['gid']
        container = arcType['containerid']
        writeToCsv([arcType_title, gid, container])


def start():
    init_csv()
    url = 'https://weibo.com/ajax/feed/allGroups'
    jsonHtml = getJsonHtml(url, {})
    print(jsonHtml)
    parseJson(jsonHtml)


if __name__ == '__main__':
    start()

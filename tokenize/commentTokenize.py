"""
    微博评论分词 词频统计 写入CSV
"""
import re

import jieba
import pandas as pd

from dao import commentDao


def getStopWordList():
    """
    获取停用词表， 此处选用百度
    :return:
    """
    return [line.strip() for line in open('baidu_stopwords.txt', encoding='utf-8').readlines()]


def cut_comment():
    """
    分词
    :return:
    """
    allCommentStr = " ".join([comment[1].strip() for comment in commentDao.getAllComment()])
    seg_list = jieba.cut(allCommentStr)  # 精准模式
    return seg_list


def wordCount():
    """
    词频统计，过滤数据：数字、单个词、停顿词
    :return:
    """
    seg_list = cut_comment()
    stop_list = getStopWordList()

    # 正则表达式去掉数字、单个字、停顿词
    new_seg_list = []
    for s in seg_list:
        number = re.search('\d+', s)
        if not number and s not in stop_list and len(s) > 1:
            new_seg_list.append(s)

    # 词频统计
    word_count = {}
    for word in set(new_seg_list):
        word_count[word] = new_seg_list.count(word)

    # 按词频排序
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_count


def commentFreToCsv(sorted_word_count):
    """
    将词频统计结果写入csv文件
    :return:
    """
    df = pd.DataFrame(sorted_word_count, columns=['word', 'count'])
    df.to_csv('commentFre.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    commentFreToCsv(wordCount())

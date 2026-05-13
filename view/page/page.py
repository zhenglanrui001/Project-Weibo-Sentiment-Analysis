from flask import Blueprint, render_template, jsonify

from dao import articleDao

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/home')
def home():

    """
    进入主页面，获取相应数据带到页面
    :return:
    """
    articleData = articleDao.get7DayArticle()
    xAxis7ArticleData = []
    yAxis7ArticleData = []
    for article in articleData:
        xAxis7ArticleData.append(article[0])
        yAxis7ArticleData.append(article[1])
    return render_template('index.html',
                           xAxis7ArticleData=xAxis7ArticleData,
                           yAxis7ArticleData=yAxis7ArticleData)


@pb.route('/homePageData')
def getHomePageData():
    """
    获取主页数据 ajax异步交互 前端每隔5Min获取一次
    :return:
    """
    totalArticle = articleDao.getTotalArticle()
    topAuthor = articleDao.getTopAuthor()
    topRegion = articleDao.getTopRegion()
    articleTop6 = articleDao.getArticleTop6()

    return jsonify(totalArticle=totalArticle, topAuthor=topAuthor, topRegion=topRegion, articleTop6=articleTop6)


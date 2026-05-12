from flask import Blueprint, request, render_template, jsonify, session, redirect

from dao import userDao
from entity.User import User
from utils.md5Util import MD5Utility

ub = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


@ub.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.values.get('username')
        password = request.values.get('password')
        if username is None or username.strip() == "":
            return jsonify(error=True, info="用户名不能为空")
        if password is None or password.strip() == "":
            return jsonify(error=True, info="密码不能为空")
        user = User(username, MD5Utility.encrypt(password))  # 密码加密
        print("用户名:", username)
        print("原密码:", password)
        print("加密后:", user.password)

        resultUser = userDao.login(user)

        print("数据库结果:", resultUser)
        if resultUser:
            session['user'] = resultUser
            return jsonify(error=False, info="登录成功")
        else:
            return jsonify(error=True, info="用户名或密码错误")


@ub.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册
    :return:
    """
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.values.get('username')
        password = request.values.get('password')
        password2 = request.values.get('password2')
        if username is None or username.strip() == "":
            return jsonify(error=True, info="用户名不能为空")
        if password is None or password.strip() == "":
            return jsonify(error=True, info="密码不能为空")
        if password2 is None or password2.strip() == "":
            return jsonify(error=True, info="确认密码不能为空")
        if password != password2:
            return jsonify(error=True, info="两次密码不一致")
        userList = userDao.getByUserName(username)
        if userList:
            return jsonify(error=True, info="用户名已存在!")
        else:
            user = User(username, MD5Utility.encrypt(password))
            if userDao.add(user):
                return jsonify(error=False, info="注册成功")
            else:
                return jsonify(error=True, info="注册失败")


@ub.route('/logout')
def logout():
    """
    用户安全退出
    :return:
    """
    session.clear()
    return redirect('/user/login')

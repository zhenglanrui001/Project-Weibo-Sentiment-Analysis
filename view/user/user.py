from flask import Blueprint, request, render_template

ub = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


@ub.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

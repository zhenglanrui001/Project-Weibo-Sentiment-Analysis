from flask import Flask

from view.page import page
from view.user import user

app = Flask(__name__)


# 注册蓝图
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)


if __name__ == '__main__':
    app.run()
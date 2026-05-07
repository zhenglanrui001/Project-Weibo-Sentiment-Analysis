from flask import Blueprint

ub = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


@ub.route('/test')
def test():
    return 'user'

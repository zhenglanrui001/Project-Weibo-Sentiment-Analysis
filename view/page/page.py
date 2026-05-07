from flask import Blueprint

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/test')
def test():
    return 'page'

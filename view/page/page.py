from flask import Blueprint, render_template

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/home')
def home():
    return render_template('index.html')

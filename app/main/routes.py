from flask import render_template, Blueprint, url_for
from app.API.categories import GetAllCategories

main_blueprint = Blueprint('main', __name__,template_folder='templates')

@main_blueprint.route('/')
@main_blueprint.route('/index')
def index():
    return render_template("main/index.html",title="Home")

@main_blueprint.route('/logs')
def logs():
    return render_template("main/logs.html",title="Audit Logs")

@main_blueprint.route('/favorites')
def favorites():
    objResponse = GetAllCategories()
    return render_template("main/favorites.html",title="Favorite List", lstCategories = objResponse.json["data"])
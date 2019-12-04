from app import app, db
from flask import render_template, jsonify
from Util import failure
from app.API.categories import GetAllCategories

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",title="Home")

@app.route('/logs')
def logs():
    return render_template("logs.html",title="Audit Logs")

@app.route('/favorites')
def favorites():
    objResponse = GetAllCategories()
    return render_template("favorites.html",title="Favorite List", lstCategories = objResponse.json["data"])
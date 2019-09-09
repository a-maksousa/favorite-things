from app import app, db
from flask import request, jsonify
from Util import Response
from app.models import Categories_Lookup, Favorite
from datetime import datetime

# Web API

# Categories

@app.route('/GetAllCategories', methods=['GET'])
def GetAllCategories():
    try:
        lstCategories = Categories_Lookup.query.all()
        response = []
        for objCategory in lstCategories:
            response.append(objCategory.as_dict())
        return jsonify(Response.success(response))

    except Exception as e:
        db.session.rollback()
        return jsonify(Response.failure())

@app.route('/AddCategory',methods=['POST'])
def AddCategory():
    try:
        strCategoryTitle = request.form["strCategoryTitle"]
        objCategory = Categories_Lookup.query.filter_by(title = strCategoryTitle).first()

        if objCategory is None:
            category = Categories_Lookup(title=strCategoryTitle,cteated_date = datetime.now(),modified_date=datetime.now())
            db.session.add(category)
            db.session.commit()
            response = Response.success(category.as_dict())
        else:
            response = Response.failure("This Category is already exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(Response.failure())

@app.route('/DeleteCategory',methods=['POST'])
def DeleteCategory():
    try:
        intCatID = request.form['intCategoryID']
        objCategory = Categories_Lookup.query.filter_by(id = intCatID).first()
        
        if not objCategory is None:
            lstFavorites = Favorite.query.filter_by(category_id=objCategory.id).all()
            if len(lstFavorites) > 0:
                Favorite.query.filter_by(category_id=objCategory.id).delete()
            db.session.delete(objCategory)
            db.session.commit()
            response = Response.success()
        else:
            response = Response.failure("This Category is not exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(Response.failure())
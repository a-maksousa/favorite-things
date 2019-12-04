from app import db
from flask import Blueprint, request, jsonify
from Util import success, failure
from app.models import Categories_Lookup, Favorite, Meta_Data, Audit_Log
from datetime import datetime

categories_blueprint = Blueprint('categories', __name__,)

@categories_blueprint.route('/GetAllCategories', methods=['GET'])
def GetAllCategories():

    objLogs = Audit_Log(description = "Getting all Categories",log_date = datetime.now())
    db.session.add(objLogs)
    db.session.commit()

    lstCategories = Categories_Lookup.query.all()
    response = [objCategory.as_dict() for objCategory in lstCategories]
    # response = []
    # for objCategory in lstCategories:
    #     response.append(objCategory.as_dict())
    return jsonify(success(response))

@categories_blueprint.route('/AddCategory',methods=['POST'])
def AddCategory():
    strCategoryTitle = request.form["strCategoryTitle"]
    objCategory = Categories_Lookup.query.filter_by(title = strCategoryTitle).first()

    if objCategory is None:
        category = Categories_Lookup(title=strCategoryTitle,cteated_date = datetime.now(),modified_date=datetime.now())
        db.session.add(category)
        db.session.commit()
        response = success(category.as_dict())

        objLogs = Audit_Log(description = "Add New Category (%s)" % strCategoryTitle ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Category is already exists")

    return jsonify(response)

@categories_blueprint.route('/DeleteCategory',methods=['POST'])
def DeleteCategory():    
    intCatID = request.form['id']
    objCategory = Categories_Lookup.query.filter_by(id = intCatID).first()
    
    if not objCategory is None:
        lstFavorites = Favorite.query.filter_by(category_id=objCategory.id).all()
        if len(lstFavorites) > 0:
            for objFavorite in lstFavorites:
                lstMetadata = Meta_Data.query.filter_by(favorite_id=objFavorite.id).all()
                if len(lstMetadata) > 0:
                    Meta_Data.query.filter_by(favorite_id=objFavorite.id).delete()
            Favorite.query.filter_by(category_id=objCategory.id).delete()
            
        db.session.delete(objCategory)
        db.session.commit()
        response = success()

        objLogs = Audit_Log(description = "Delete Category (%s)" % objCategory.title ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Category is not exists")

    return jsonify(response)
from app import db
from flask import Blueprint, request, jsonify
from Util import success, failure
from app.models import Categories_Lookup, Favorite, Meta_Data, Audit_Log
from datetime import datetime

favorites_blueprint = Blueprint('favorites', __name__,)

@favorites_blueprint.route('/GetFavByCatID', methods=['GET'])
def GetFavByCatID():
    intCategoryID = request.args['intCategoryID']
    objCategory = Categories_Lookup.query.filter_by(id = intCategoryID).first()

    if not objCategory is None:
        lstFavorites = Favorite.query.filter_by(category_id=objCategory.id)
        response = []
        for objFavorite in lstFavorites:
            response.append(objFavorite.as_dict())
        response =  success(response)

        objLogs = Audit_Log(description = "Getting all Favorites for (%s) Category" % objCategory.title ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Category is not exists")

    return jsonify(response)

@favorites_blueprint.route('/AddFavByCatID', methods=['POST'])
def AddFavByCatID():
    intCatID = request.form['intCatID']
    strFavoriteTitle = request.form['strFavoriteTitle']
    strDescription = request.form['strDescription']
    intRanking = request.form['intRanking']
    objCategory = Categories_Lookup.query.filter_by(id = intCatID).first()

    if not objCategory is None:
        objFavorite = Favorite.query.filter(Favorite.category_id == intCatID , Favorite.title == strFavoriteTitle).first()

        if objFavorite is None:
            objSameRankItem = Favorite.query.filter_by(category_id = intCatID, ranking = intRanking).first()
            if objSameRankItem:
                rankReorder(intCatID,intRanking)
            fav = Favorite(title = strFavoriteTitle,description = strDescription,ranking = intRanking,cteated_date = datetime.now(),modified_date=datetime.now(),Category=objCategory)
            db.session.add(fav)
            db.session.commit()
            response = success(fav.as_dict())

            objLogs = Audit_Log(description = "Add New Favorite (%s) for (%s) Category" % (strFavoriteTitle,objCategory.title) ,log_date = datetime.now())
            db.session.add(objLogs)
            db.session.commit()

        else:
            response = failure("Favorite Name Must be Unique")
    else:
        response = failure("This Category is not exists")

    return jsonify(response)

@favorites_blueprint.route('/DeleteFavorite', methods=['POST'])
def DeleteFavorite():
   
    intFavID = request.form['intFavID']
    objFavorite = Favorite.query.filter_by(id = intFavID).first()

    if not objFavorite is None:

        lstMetaData = Meta_Data.query.filter_by(favorite_id = intFavID).all()
        if len(lstMetaData) > 0:
            Meta_Data.query.filter_by(favorite_id = intFavID).delete()
        db.session.delete(objFavorite)
        db.session.commit()
        response = success()

        objLogs = Audit_Log(description = "Delete Favorite (%s)" % objFavorite.title ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Favorite is not Exists")

    return jsonify(response)

@favorites_blueprint.route('/UpdateFavorite', methods=['POST'])
def UpdateFavorite():
    
    intFavID = request.form['intFavID']
    strTitle = request.form['strTitle']
    strDescription = request.form['strDescription']
    intRank = request.form['intRank']
    
    objFavorite = Favorite.query.filter_by(id = intFavID).first()
    if not objFavorite is None:
        if strTitle != objFavorite.title and Favorite.query.filter_by(title = strTitle).first():
            response = failure("Favorite Name Must be Unique")

        objFavorite.title = strTitle
        objFavorite.description = strDescription
        objFavorite.ranking = intRank
        objFavorite.modified_date = datetime.now()
        db.session.commit()
        response = success(objFavorite.as_dict())

        objLogs = Audit_Log(description = "Update Favorite (%s)" % strTitle ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Favorite is not Exists")

    return jsonify(response)
    
def rankReorder(intCatID, intRank):
    lstSameRankItems = Favorite.query.filter(Favorite.ranking >= intRank, Favorite.category_id == intCatID).all()
    for objSameRankItem in lstSameRankItems:
        intNewRank = objSameRankItem.ranking + 1
        objSameRankItem.ranking = intNewRank
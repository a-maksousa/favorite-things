from app import app, db
from flask import request, jsonify
from Util import success, failure
from app.models import Categories_Lookup, Favorite, Meta_Data, Audit_Log
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
        return jsonify(success(response))

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

@app.route('/AddCategory',methods=['POST'])
def AddCategory():
    try:
        strCategoryTitle = request.form["strCategoryTitle"]
        objCategory = Categories_Lookup.query.filter_by(title = strCategoryTitle).first()

        if objCategory is None:
            category = Categories_Lookup(title=strCategoryTitle,cteated_date = datetime.now(),modified_date=datetime.now())
            db.session.add(category)
            db.session.commit()
            response = success(category.as_dict())
        else:
            response = failure("This Category is already exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

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
            response = success()
        else:
            response = failure("This Category is not exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

# Favorites

@app.route('/GetFavByCatID', methods=['GET'])
def GetFavByCatID():
    try:
        intCategoryID = request.form['intCategoryID']
        objCategory = Categories_Lookup.query.filter_by(id = intCategoryID).first()

        if not objCategory is None:
            lstFavorites = Favorite.query.filter_by(category_id=objCategory.id)
            response = []
            for objFavorite in lstFavorites:
                response.append(objFavorite.as_dict())
            response =  success(response)
        else:
            response = failure("This Category is not exists")

        return jsonify(response)
        
    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

@app.route('/AddFavByCatID', methods=['POST'])
def AddFavByCatID():
   try:
        intCatID = request.form['intCatID']
        strFavoriteTitle = request.form['strFavoriteTitle']
        strDescription = request.form['strDescription']
        intRanking = request.form['intRanking']
        objCategory = Categories_Lookup.query.filter_by(id = intCatID).first()

        if not objCategory is None:
            objFavorite = Favorite.query.filter_by(title = strFavoriteTitle).first()

            if objFavorite is None:
                objSameRankItem = Favorite.query.filter_by(category_id = intCatID, ranking = intRanking).first()
                if objSameRankItem:
                    rankReorder(intCatID,intRanking)
                fav = Favorite(title = strFavoriteTitle,description = strDescription,ranking = intRanking,cteated_date = datetime.now(),modified_date=datetime.now(),Category=objCategory)
                db.session.add(fav)
                db.session.commit()
                response = success(fav.as_dict())
            else:
                response = failure("Favorite Name Must be Unique")
        else:
            response = failure("This Category is not exists")

        return jsonify(response)

   except Exception as e:
       db.session.rollback()
       return jsonify(failure())

@app.route('/DeleteFavorite', methods=['POST'])
def DeleteFavorite():
   try:
        intFavID = request.form['intFavID']
        objFavorite = Favorite.query.filter_by(id = intFavID).first()

        if not objFavorite is None:

            lstMetaData = Meta_Data.query.filter_by(favorite_id = intFavID).all()
            if len(lstMetaData) > 0:
                Meta_Data.query.filter_by(favorite_id = intFavID).delete()
            db.session.delete(objFavorite)
            db.session.commit()
            response = success()
        else:
            response = failure("This Favorite is not Exists")

        return jsonify(response)
           
   except Exception as e:
       db.session.rollback()
       return jsonify(failure())

@app.route('/UpdateFavorite', methods=['POST'])
def UpdateFavorite():
    try:
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
        else:
            response = failure("This Favorite is not Exists")

        return jsonify(response)

    except Exception as e:
       db.session.rollback()
       return jsonify(failure())

# Favorites Meta Data

@app.route('/GetMetaDataByFavID', methods=['GET'])
def GetMetaDataByFavID():
    try:
        intFavID = request.form['intFavID']
        if Favorite.query.filter_by(id = intFavID).first():
            lstMetaData = Meta_Data.query.filter_by(favorite_id = intFavID)
            response = []
            for objMetaData in lstMetaData:
                response.append(objMetaData.as_dict())
            response = success(response)
        else:
            response = failure("This Favorite is not exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

@app.route('/AddMetaData', methods=['POST'])
def AddMetaData():
    try:
        intFavID = request.form['intFavID']
        key = request.form['key']
        value = request.form['value']
        objFavorite = Favorite.query.filter_by(id = intFavID).first()
        if objFavorite:
            objMetaData = Meta_Data(key = key,value = value,FavoriteItem = objFavorite)
            db.session.add(objMetaData)
            objFavorite.modified_date = datetime.now()
            db.session.commit()
            response = success(objMetaData.as_dict())

        else:
            response = failure("This Favorite is not exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

@app.route('/UpdateMetaData', methods=['POST'])
def UpdateMetaData():
    try:
        intFavID = request.form['intFavID']
        intMetaDataID = request.form['intMetaDataID']
        key = request.form['key']
        value = request.form['value'] 

        objFavorite = Favorite.query.filter_by(id = intFavID).first()
        if objFavorite:
            objMetaData = Meta_Data.query.filter_by(id = intMetaDataID).first()
            if objMetaData:
                objMetaData.key = key
                objMetaData.value = value
                objFavorite.modified_date = datetime.now()
                db.session.commit()
                response = success(objMetaData.as_dict())

            else:
                response = failure("This Meta Data is not exists")

        else:
            response = failure("This Favorite is not exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

@app.route('/DeleteMetaData', methods=['POST'])
def DeleteMetaData():
    try:
        intFavID = request.form['intFavID']
        intMetaDataID = request.form['intMetaDataID']

        objFavorite = Favorite.query.filter_by(id = intFavID).first()
        if objFavorite:
            objMetaData = Meta_Data.query.filter_by(id = intMetaDataID).first()
            if objMetaData:
                db.session.delete(objMetaData)
                objFavorite.modified_date = datetime.now()
                db.session.commit()
                response = success()
            else:
                response = failure("This Meta Data is not exists")
        else:
            response = failure("This Favorite is not exists")

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

# Logs

@app.route('/GetLogs', methods=['GET'])
def GetLogs():
    try:
        lstLogs = Audit_Log.query.all()
        response = []
        for objLog in lstLogs:
            response.append(objLog.as_dict())

        return jsonify(success(response))

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

@app.route('/ClearLogs', methods=['POST'])
def ClearLogs():
    try:
        Audit_Log.query.delete()
        db.session.commit()
        return jsonify(success())

    except Exception as e:
        db.session.rollback()
        return jsonify(failure())

# Helper Methods
def rankReorder(intCatID, intRank):
    lstSameRankItems = Favorite.query.filter(Favorite.ranking >= intRank, Favorite.category_id == intCatID).all()
    for objSameRankItem in lstSameRankItems:
        intNewRank = objSameRankItem.ranking + 1
        objSameRankItem.ranking = intNewRank
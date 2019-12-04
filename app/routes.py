from app import app, db
from flask import request, jsonify, render_template, url_for
from Util import success, failure
from app.models import Categories_Lookup, Favorite, Meta_Data, Audit_Log
from datetime import datetime

# Views

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

# Web API

@app.errorhandler(500)
def page_not_found(error):
    db.session.rollback()
    return jsonify(failure())

# Categories

@app.route('/GetAllCategories', methods=['GET'])
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

@app.route('/AddCategory',methods=['POST'])
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

@app.route('/DeleteCategory',methods=['POST'])
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

# Favorites

@app.route('/GetFavByCatID', methods=['GET'])
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

@app.route('/AddFavByCatID', methods=['POST'])
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

@app.route('/DeleteFavorite', methods=['POST'])
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

@app.route('/UpdateFavorite', methods=['POST'])
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
    
# Favorites Meta Data

@app.route('/GetMetaDataByFavID', methods=['GET'])
def GetMetaDataByFavID():
    
    intFavoriteID = request.args['intFavoriteID']
    objFavorite = Favorite.query.filter_by(id = intFavoriteID).first()
    if objFavorite:
        lstMetaData = Meta_Data.query.filter_by(favorite_id = intFavoriteID)
        response = []
        for objMetaData in lstMetaData:
            response.append(objMetaData.as_dict())
        response = success(response)

        objLogs = Audit_Log(description = "Getting all Meta Data from (%s) Favorite" % objFavorite.title ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Favorite is not exists")

    return jsonify(response)

@app.route('/AddMetaData', methods=['POST'])
def AddMetaData():
    
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

        objLogs = Audit_Log(description = "Add New MetaData (%s) for (%s) Favorite" % (key,objFavorite.title) ,log_date = datetime.now())
        db.session.add(objLogs)
        db.session.commit()

    else:
        response = failure("This Favorite is not exists")

    return jsonify(response)

@app.route('/UpdateMetaData', methods=['POST'])
def UpdateMetaData():
    
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

            objLogs = Audit_Log(description = "Update MetaData (%s) from (%s) Favorite" % (key,objFavorite.title) ,log_date = datetime.now())
            db.session.add(objLogs)
            db.session.commit()

        else:
            response = failure("This Meta Data is not exists")

    else:
        response = failure("This Favorite is not exists")

    return jsonify(response)

@app.route('/DeleteMetaData', methods=['POST'])
def DeleteMetaData():
    
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

            objLogs = Audit_Log(description = "Delete MetaData (%s) from (%s) Favorite" % (objMetaData.key,objFavorite.title) ,log_date = datetime.now())
            db.session.add(objLogs)
            db.session.commit()

        else:
            response = failure("This Meta Data is not exists")
    else:
        response = failure("This Favorite is not exists")

    return jsonify(response)

# Logs

@app.route('/GetLogs', methods=['GET'])
def GetLogs():
    
    lstLogs = Audit_Log.query.all()
    response = []
    for objLog in lstLogs:
        response.append(objLog.as_dict())

    return jsonify(success(response))

@app.route('/ClearLogs', methods=['POST'])
def ClearLogs():
    
    Audit_Log.query.delete()
    db.session.commit()
    return jsonify(success())

# Helper Methods
def rankReorder(intCatID, intRank):
    lstSameRankItems = Favorite.query.filter(Favorite.ranking >= intRank, Favorite.category_id == intCatID).all()
    for objSameRankItem in lstSameRankItems:
        intNewRank = objSameRankItem.ranking + 1
        objSameRankItem.ranking = intNewRank
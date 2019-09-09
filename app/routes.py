from app import app, db
from flask import request, jsonify
from Util import Response
from app.models import Categories_Lookup, Favorite, Meta_Data
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
            response =  Response.success(response)
        else:
            response = Response.failure("This Category is not exists")

        return jsonify(response)
        
    except Exception as e:
        db.session.rollback()
        return jsonify(Response.failure())

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
                response = Response.success(fav.as_dict())
            else:
                response = Response.failure("Favorite Name Must be Unique")
        else:
            response = Response.failure("This Category is not exists")

        return jsonify(response)

   except Exception as e:
       db.session.rollback()
       return jsonify(Response.failure())

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
            response = Response.success()
        else:
            response = Response.failure("This Favorite is not Exists")

        return jsonify(response)
           
   except Exception as e:
       db.session.rollback()
       return jsonify(Response.failure())

# Helper Methods
def rankReorder(intCatID, intRank):
    lstSameRankItems = Favorite.query.filter(Favorite.ranking >= intRank, Favorite.category_id == intCatID).all()
    for objSameRankItem in lstSameRankItems:
        intNewRank = objSameRankItem.ranking + 1
        objSameRankItem.ranking = intNewRank
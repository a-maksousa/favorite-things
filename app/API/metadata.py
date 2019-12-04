from app import db
from flask import Blueprint, request, jsonify
from Util import success, failure
from app.models import Favorite, Meta_Data, Audit_Log
from datetime import datetime

metadata_blueprint = Blueprint('metadata', __name__,)

@metadata_blueprint.route('/GetMetaDataByFavID', methods=['GET'])
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

@metadata_blueprint.route('/AddMetaData', methods=['POST'])
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

@metadata_blueprint.route('/UpdateMetaData', methods=['POST'])
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

@metadata_blueprint.route('/DeleteMetaData', methods=['POST'])
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

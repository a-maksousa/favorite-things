from app import db
from flask import Blueprint, jsonify
from Util import success
from app.models import Audit_Log

logs_blueprint = Blueprint('logs', __name__,)

@logs_blueprint.route('/GetLogs', methods=['GET'])
def GetLogs():
    
    lstLogs = Audit_Log.query.all()
    response = []
    for objLog in lstLogs:
        response.append(objLog.as_dict())

    return jsonify(success(response))

@logs_blueprint.route('/ClearLogs', methods=['POST'])
def ClearLogs():
    
    Audit_Log.query.delete()
    db.session.commit()
    return jsonify(success())

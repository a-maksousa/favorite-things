from app import app, db
from flask import jsonify
from Util import failure

@app.errorhandler(500)
def page_not_found(error):
    db.session.rollback()
    return jsonify(failure())
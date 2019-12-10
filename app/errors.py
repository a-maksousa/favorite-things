from app import app, db
from flask import jsonify
from Util import failure

@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return jsonify(failure())

@app.errorhandler(400)
def bad_request(error):
    db.session.rollback()
    if error.args[0]:
        return jsonify(failure("%s is Required" % error.args[0]))
    return jsonify(failure())

@app.errorhandler(404)
def not_found(error):
    db.session.rollback()
    return jsonify(failure("Incorrect Route Path"))
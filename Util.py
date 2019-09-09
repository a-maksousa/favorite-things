from flask import jsonify

class Response():
    def success(data):
        data = {'data':data,'code':1}
        return jsonify(data)

    def failure(msg):
        data = {'code':0,'msg':msg}
        return jsonify(data)
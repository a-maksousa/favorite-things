class Response():
    def success(data={}):
        data = {'code':1,'data':data}
        return data

    def failure(msg="Unknown Error"):
        data = {'code':0,'msg':msg}
        return data
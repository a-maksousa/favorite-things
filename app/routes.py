from app import app, db
from flask import request
from Util import Response
from app.models import Categories_Lookup
from datetime import datetime

# Web API

# Categories
@app.route('/addCategory',methods=['POST'])
def addCategory():
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

    except Exception as e:
        db.session.rollback()
        response = Response.failure("Unknown Error")

    return response

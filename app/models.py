from app import db

class Categories_Lookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='Category', lazy='dynamic')
    cteated_date = db.Column(db.DateTime,nullable=False)
    modified_date = db.Column(db.DateTime,nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    description = db.Column(db.Text)
    ranking = db.Column(db.Integer,nullable=False)
    cteated_date = db.Column(db.DateTime,nullable=False)
    modified_date = db.Column(db.DateTime,nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories__lookup.id'),nullable=False)
    meta_data = db.relationship('Meta_Data', backref='FavoriteItem', lazy='dynamic')

class Meta_Data(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    key=db.Column(db.String(30), index=True, nullable=False)
    value=db.Column(db.String(30), index=True, nullable=False)
    favorite_id=db.Column(db.Integer, db.ForeignKey('favorite.id'),nullable=False)

class Item_Type_Lookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(30), index=True, unique=True, nullable=False)
    audit_log = db.relationship('Audit_Log', backref='ItemType', lazy='dynamic')

class Operation_Type_Lookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(30), index=True, unique=True, nullable=False)
    audit_log = db.relationship('Audit_Log', backref='OperationType', lazy='dynamic')

class Audit_Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_date = db.Column(db.DateTime,nullable=False)
    item_name = db.Column(db.Text,nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey('item__type__lookup.id'),nullable=False)
    operation_type_id = db.Column(db.Integer, db.ForeignKey('operation__type__lookup.id'),nullable=False)
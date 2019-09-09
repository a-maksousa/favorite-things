from app import db

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Categories_Lookup(db.Model,JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='Category', lazy='dynamic')
    cteated_date = db.Column(db.DateTime,nullable=False)
    modified_date = db.Column(db.DateTime,nullable=False)

class Favorite(db.Model,JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    description = db.Column(db.Text)
    ranking = db.Column(db.Integer,nullable=False)
    cteated_date = db.Column(db.DateTime,nullable=False)
    modified_date = db.Column(db.DateTime,nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories__lookup.id'),nullable=False)
    meta_data = db.relationship('Meta_Data', backref='FavoriteItem', lazy='dynamic')

class Meta_Data(db.Model,JsonModel):
    id= db.Column(db.Integer, primary_key=True)
    key=db.Column(db.String(30), index=True, nullable=False)
    value=db.Column(db.String(30), index=True, nullable=False)
    favorite_id=db.Column(db.Integer, db.ForeignKey('favorite.id'),nullable=False)

class Audit_Log(db.Model,JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    log_date = db.Column(db.DateTime,nullable=False)
    description = db.Column(db.Text,nullable=False)
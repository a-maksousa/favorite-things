from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, routes
from app.API.categories import categories_blueprint
from app.API.favorites import favorites_blueprint
from app.API.metadata import metadata_blueprint
from app.API.logs import logs_blueprint

# register blueprints
for blueprint in (categories_blueprint, favorites_blueprint,metadata_blueprint,logs_blueprint):
    app.register_blueprint(blueprint)
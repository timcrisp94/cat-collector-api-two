from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.models.db import db
# import config to pass to create_app fn
from config import Config

# ============ Import Models ============
from api.models.user import User
from api.models.profile import Profile
from api.models.cat import Cat

# ============ Import Views ============
from api.views.auth import auth
from api.views.cats import cats

# Cross Origin Resource Sharing - allows Flask and React apps to communicate with one another while running on different ports (origins)

# creates a new instance of CORS 
cors = CORS()
migrate = Migrate() 
# allowable http methods
list = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'LINK']

# application factory - app object is created by a function
# config object has all settings necessary for a given environment
def create_app(config):
  # flask app created in create_app function
  app = Flask(__name__)
  app.config.from_object(config)
  # create app is passed config object and returns a new instance of our app with desired settings

  db.init_app(app)
  migrate.init_app(app, db)
  # configure cors instance with app and settings
  cors.init_app(app, supports_credentials=True, methods=list)

  # ============ Register Blueprints ============
  app.register_blueprint(auth, url_prefix='/api/auth')
  app.register_blueprint(cats, url_prefix='/api/cats') 

  return app

app = create_app(Config)
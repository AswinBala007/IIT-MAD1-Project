from flask import Flask,jsonify, render_template
import os
from db import db
from flask_smorest import Api
from flask_migrate import Migrate
from Controllers.admin import blp as adminBlueprint
from Controllers.auth import blp as authBlueprint
from Controllers.sponsors import blp as sponsorsBlueprint
from Controllers.influencer import blp as influencerBlueprint
from Controllers.search import blp as searchBlueprint
# from Controllers.profile import blp as profileBlueprint
from Models.models import *
from flask_login import UserMixin,login_user,current_user,LoginManager,login_required,logout_user

def create_app():
    app=Flask(__name__)
    app.debug =True
    app.config["PROPAGATE_EXCEPTIONS"] = True  
    app.config["API_TITLE"] = "Influencer Engagement and Sponsorship Coordination Platform"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" 
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secrett')
    app.config['SECRET_KEY'] ="secret"    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    login_manager=LoginManager()
    login_manager.init_app(app)
    login_manager.login_view="Auth.login"
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    
    api = Api(app)
    # migrate = Migrate(app, db)  
    with app.app_context():
        db.create_all()
          
    api.register_blueprint(adminBlueprint)
    api.register_blueprint(authBlueprint)
    api.register_blueprint(sponsorsBlueprint)
    api.register_blueprint(influencerBlueprint)
    api.register_blueprint(searchBlueprint)
    # api.register_blueprint(profileBlueprint)
    
    @app.route('/', methods=['GET'])
    def test():
        # return render_template("login.html")
        return "Welcome"

    return app

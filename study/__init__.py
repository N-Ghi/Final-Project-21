from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object('study.config.Config')  

    db.init_app(app)
    migrate.init_app(app, db) 
  
  

    with app.app_context():
        
        import study.db_models  
        from .routes import register_routes  

        register_routes(app) 

        db.create_all()

    return app
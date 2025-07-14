from flask import Flask
from backend.models import db,Admin,ServiceCategory, ServiceProfessional, User
from flask_login import LoginManager
from backend.api import api

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household_app_db.sqlite3"
    app.config["SECRET_KEY"] = "thisismysecret"
    db.init_app(app)
    api.init_app(app)
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_user(email):
        return db.session.query(User).filter_by(email= email ).first() or \
                db.session.query(Admin).filter_by(email= email).first() or \
                db.session.query(ServiceProfessional).filter_by(email=email).first()

    
    
    app.app_context().push()
    db.create_all()
    return app

app  = create_app()


from backend.routes import *
from backend.create_data import *
from backend.api import *





if __name__ == "__main__":
    app.run(debug=True)
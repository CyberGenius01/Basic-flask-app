from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'a6e745149e5d3b809ea3dcb5'
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(app, model_class=Base)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login_page' #  redirect to login
login_manager.login_message_category = 'info'
from static.market import routes

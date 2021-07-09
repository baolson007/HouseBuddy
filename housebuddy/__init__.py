from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///housebuddy.db'
app.config['SECRET_KEY'] = 'd488cab1ea81773f2583d911' #CHANGE THIS PRIOR TO DEPLOYING
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from housebuddy import routes
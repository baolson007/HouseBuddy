from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///housebuddy.db'
app.config['SECRET_KEY'] = 'd488cab1ea81773f2583d911' #CHANGE THIS PRIOR TO DEPLOYING
db = SQLAlchemy(app)


from housebuddy import routes
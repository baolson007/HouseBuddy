from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///housebuddy.db'
db = SQLAlchemy(app)


from housebuddy import routes
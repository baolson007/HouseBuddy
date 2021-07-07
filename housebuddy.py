from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///housebuddy.db'
db = SQLAlchemy(app)

class MaintenanceItem(db.Model):
    maintenanceID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=500), nullable=False)
    #user = 
    dueDate = db.Column(db.DateTime, default=datetime.utcnow)
    #completionStatus = db.Column(db.Integer(), default=0, unique=False)
    #completionDate = db.Column(db.DateTime, nullable =True, default=datetime.fromisoformat('1900-01-01'))

    def __repr__(self):
        return f'Maintenance: {self.name}'

#class User(db.Model):
    #id = db.Column(db.Integer(), primary_key=True)
    #username = db.Column(db.String(length=40, unique=True, nullable=False))
    #email = db.Column(db.String(length=120, unique=True, nullable=False))

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/myFiles')
def my_files():
    files = [
        {'dueDate':'1/3/21' , 'maintenanceItem' : 'clean gutters' , 'fileName' : 'cleanGutters.docx', 'uploadDate' : '1/3/21'},
        {'dueDate':'12/8/21' , 'maintenanceItem' : 'pest control' , 'fileName' : 'exterminatePests.docx', 'uploadDate' : '12/25/21'},
        {'dueDate':'4/19/21' , 'maintenanceItem' : 'asbestos removal' , 'fileName' : 'asbestosRemoval.pdf', 'uploadDate' : '5/25/21'}

    ]
    return render_template('myFiles.html', files = files, username = 'TestUser')

###
#@app.route('/overview')
#def overview():
#    return render_template('overview.html', username = 'TestUser')
###

@app.route('/maintenance')
def maintenance():
    items = MaintenanceItem.query.all()
    return render_template('maintenance.html', items=items, username = 'TestUser');

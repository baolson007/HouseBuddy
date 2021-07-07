from housebuddy import db
from datetime import datetime

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

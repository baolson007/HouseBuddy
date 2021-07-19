from housebuddy import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #__tablename__='User'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=40), unique=True, nullable=False)
    email = db.Column(db.String(length=80), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=80), nullable=False)
    first_name = db.Column(db.String(length=20), nullable=True)
    last_name = db.Column(db.String(length=20), nullable=True)
    #home-address?
    total_cost = db.Column(db.Numeric(), nullable=True)
    MaintenanceItems=db.relationship('MaintenanceItem', backref='item_owner', lazy=True) #sqlAlchemy lazy

    #@property 
    #def total_cost_formatted(self):
    #    if len(str(self.total_cost)) >= 4:
    #        return f'${str(self.total_cost)[:-3]},{str(self.total_cost)[-3:]}'
     #   else:
    #        return f'${str(self.total_cost)}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'Username: {self.username}'

#class HomeAddress(db.Model):

class MaintenanceItem(db.Model):
    __tablename__= 'MaintenanceItem'
    maintenanceID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    description = db.Column(db.String(length=500), unique=False, nullable=False)
    dueDate = db.Column(db.DateTime, default=None)#datetime.utcnow)
    #completionStatus = db.Column(db.Integer(), default=0, unique=False)
    #completionDate = db.Column(db.DateTime, nullable =True, default=datetime.fromisoformat('1900-01-01'))
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    cost = db.Column(db.Numeric(), nullable=True)
    deleted = db.Column(db.Integer(), nullable=True, default=0)

    def __repr__(self):
        return f'Maintenance: {self.name}'

class UserFile(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = (db.Column(db.String(length=60), nullable=False))
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    uploadDate = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Integer(), default=0)
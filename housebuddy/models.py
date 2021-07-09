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
    MaintenanceItems=db.relationship('MaintenanceItem', backref='item_owner', lazy=True) #sqlAlchemy lazy

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
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=500), nullable=False)
    dueDate = db.Column(db.DateTime, default=datetime.utcnow)
    #completionStatus = db.Column(db.Integer(), default=0, unique=False)
    #completionDate = db.Column(db.DateTime, nullable =True, default=datetime.fromisoformat('1900-01-01'))
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Maintenance: {self.name}'


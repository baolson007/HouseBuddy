from housebuddy import app
from flask import render_template, redirect, url_for, flash
from housebuddy.models import MaintenanceItem, User
from housebuddy.forms import RegisterForm
from housebuddy import db

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                                email=form.email.data,
                                password_hash=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home_page'))
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'Error in registration: {msg}', category='danger')
    return render_template('register.html', form=form)
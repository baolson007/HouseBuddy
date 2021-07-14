from housebuddy import app
from flask import render_template, redirect, url_for, flash, request
from housebuddy.models import MaintenanceItem, User
from housebuddy.forms import RegisterForm, LoginForm, AddItemForm, EditItemForm
from housebuddy import db
from flask_login import login_user, logout_user, current_user
from datetime import datetime

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/maintenance')
def maintenance():
    if current_user.is_authenticated:
        #items = MaintenanceItem.query.all()
        items = MaintenanceItem.query.filter_by(owner=current_user.id, deleted=0)
        return render_template('maintenance.html', items=items);
    else:
        flash(f'No items retrieved. Add items, or contact admin', category='info')
        return render_template('maintenance.html', items=none)

@app.route('/addItem',  methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        new_maintenance_item = MaintenanceItem(name=form.name.data,
                                description=form.description.data, 
                                dueDate=form.dueDate.data,
                                owner=current_user.id)
        db.session.add(new_maintenance_item)
        db.session.commit()
        flash(f'Item successfully added', category='success')
        return render_template('maintenance.html', items=MaintenanceItem.query.filter_by(owner=current_user.id, deleted=0))
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'Error in registration: {msg}', category='danger')
        return render_template('addItem.html', form=form)

    return render_template('addItem.html', form=form)



@app.route('/editItem/<item_id>', methods=['GET','POST'])
def edit_item(item_id):
    ##--NOTE--#############################################
    ##  url_for() sends param as str().                   
    ##  item_id is the MaintenanceItem id, NOT the User id
    #######################################################
    form = EditItemForm()
    item_to_edit = MaintenanceItem.query.filter_by(maintenanceID=int(item_id)).first()

    if form.delete.data == 1:
        item_to_edit.deleted = 1
        db.session.commit()
        flash('item deleted', category='danger')
        return redirect(url_for('maintenance'))

    if form.validate_on_submit():
        item_to_edit.name = form.name.data
        item_to_edit.description = form.description.data
        #item_to_edit.dueDate =form.dueDate
        db.session.commit()
        
        return redirect(url_for('maintenance'))
        #render_template('maintenance.html', items=MaintenanceItem.query.filter_by(owner=current_user.id))

    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'Error on Submit:could not edit item: {msg}', category='danger')
    return render_template('editItem.html', form=form, item=item_to_edit)
    
#@app.route('/delete/<item_id>', methods=['GET','POST'])
#def delete_item(item_id):



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                                email=form.email.data,
                                password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home_page'))
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'Error in registration: {msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        login_attempt_usr = User.query.filter_by(username=form.username.data).first()
        if login_attempt_usr and login_attempt_usr.check_password(
            attempted_password=form.password.data
            ):
                login_user(login_attempt_usr)
                flash(f'Succesfully logged in as {login_attempt_usr.username}', category='success')
                return redirect(url_for('maintenance'))
        else:
            flash('Username and\\or password do not match. Please try again', category='danger')
    return render_template('login.html', form=form)




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("Succesfully Logged Out", category='info')
    return redirect(url_for('home_page'))


# STUB
@app.route('/tour')
def tour():
    return render_template('tour.html')



# DUMMY FILES FOR NOW
@app.route('/myFiles')
def my_files():
    files = [
        {'dueDate':'1/3/21' , 'maintenanceItem' : 'clean gutters' , 'fileName' : 'cleanGutters.docx', 'uploadDate' : '1/3/21'},
        {'dueDate':'12/8/21' , 'maintenanceItem' : 'pest control' , 'fileName' : 'exterminatePests.docx', 'uploadDate' : '12/25/21'},
        {'dueDate':'4/19/21' , 'maintenanceItem' : 'asbestos removal' , 'fileName' : 'asbestosRemoval.pdf', 'uploadDate' : '5/25/21'}

    ]
    return render_template('myFiles.html', files = files)

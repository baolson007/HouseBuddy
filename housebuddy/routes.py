from housebuddy import app
from flask import render_template, redirect, url_for, flash, request, send_file
from housebuddy.models import MaintenanceItem, User, UserFile
from housebuddy.forms import RegisterForm, LoginForm, AddItemForm, EditItemForm, UploadForm
from housebuddy import db
from flask_login import login_user, logout_user, current_user
from datetime import datetime
import os, decimal
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/maintenance')
def maintenance():
    if current_user.is_authenticated:
        #items = MaintenanceItem.query.all()
        items = MaintenanceItem.query.filter_by(owner=current_user.id, deleted=0)
        item_cost_sum = decimal.Decimal(0.00)
        for item in items:
            if item.cost != None:
                item_cost_sum += decimal.Decimal(round(item.cost,2))
        return render_template('maintenance.html', items=items, item_cost_sum=round(item_cost_sum, 2))#float(item_cost_sum));
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



@app.route('/editItem/<int:item_id>', methods=['GET','POST'])
def edit_item(item_id):
    ##--NOTE--#############################################
    ##  url_for() sends param as str().                   
    ##  item_id is the MaintenanceItem id, NOT the User id
    #######################################################
    form = EditItemForm()
    item_to_edit = MaintenanceItem.query.filter_by(maintenanceID=item_id).first()

    if form.delete.data == 1:
        item_to_edit.deleted = 1
        db.session.commit()
        flash('item deleted', category='danger')
        return redirect(url_for('maintenance'))

    if form.validate_on_submit():
        item_to_edit.name = form.name.data
        item_to_edit.description = form.description.data
        #item_to_edit.dueDate =form.dueDate
        item_to_edit.cost = form.cost.data
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



@app.route('/myFiles', methods=['GET', 'POST'])
def my_files():
    #files = [
    #    {'dueDate':'1/3/21' , 'maintenanceItem' : 'clean gutters' , 'fileName' : 'cleanGutters.docx', 'uploadDate' : '1/3/21'},
    #    {'dueDate':'12/8/21' , 'maintenanceItem' : 'pest control' , 'fileName' : 'exterminatePests.docx', 'uploadDate' : '12/25/21'},
    #    {'dueDate':'4/19/21' , 'maintenanceItem' : 'asbestos removal' , 'fileName' : 'asbestosRemoval.pdf', 'uploadDate' : '5/25/21'}

    #]

    files = UserFile.query.filter_by(owner=current_user.id, deleted=0)

    return render_template('myFiles.html', files = files)


@app.route('/deleteFile/<int:file_id>', methods=['GET','POST'])
def delete_file(file_id):
    file_to_delete = UserFile.query.filter_by(id=int(file_id)).first()
    db.session.delete(file_to_delete)
    db.session.commit()
    flash('file deleted', category='success')

    files = UserFile.query.filter_by(owner=current_user.id)
    return render_template('myFiles.html', files=files)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadFile/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part in request')
            return redirect(request.url)
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('file ' + filename + ' successfully uploaded', category='success')
            file_to_add = UserFile(owner=current_user.id, filename=filename)
            db.session.add(file_to_add)
            db.session.commit()
            return redirect(url_for('my_files'))
        else:
            flash('File does not exist or is an invalid type of file, try again')
    return render_template('uploadFile.html')#, form=form)

@app.route('/downloadFile/<filename>', methods=['GET'])
def download_file(filename):
    file_path = app.config['UPLOAD_FOLDER'] + "//" + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')
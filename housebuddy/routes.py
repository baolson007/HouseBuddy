from housebuddy import app, db, mail, bcrypt
from flask import render_template, redirect, url_for, flash, request, send_file
from housebuddy.models import MaintenanceItem, User, UserFile
from housebuddy.forms import (RegisterForm, LoginForm, AddItemForm, EditItemForm,
                             NewPasswordForm, ResetPasswordForm)  #,UploadForm
#from housebuddy import db, mail
from flask_login import login_user, logout_user, current_user
from datetime import datetime, date
#import datetime, date
import os, decimal
from werkzeug.utils import secure_filename
from flask_mail import Message

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

@app.route('/')
@app.route('/home')
def home_page():
    if current_user.is_authenticated:
        return render_template('overview.html')
    else:
        return render_template('home.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html')



@app.route('/maintenance', methods=['GET','POST'])
def maintenance():
    if current_user.is_authenticated:
        items = MaintenanceItem.query.filter_by(owner=current_user.id, deleted=0, completionStatus=0)
        item_cost_sum = decimal.Decimal(0.00)
        for item in items:
            if item.cost != None:
                item_cost_sum += decimal.Decimal(round(item.cost,2))
        return render_template('maintenance.html', items=items, item_cost_sum=round(item_cost_sum, 2))#float(item_cost_sum));
    else:
        flash(f'No items retrieved. Add items, or contact admin', category='info')
        return render_template('maintenance.html', items=none)

@app.route('/completedMaintenance', methods=['GET', 'POST'])
def completed_maintenance():
    items = MaintenanceItem.query.filter_by(owner=current_user.id, deleted=0, completionStatus=1)
    item_cost_sum = decimal.Decimal(0.0)
    for item in items:
            if item.cost != None:
                item_cost_sum += decimal.Decimal(round(item.cost,2))
    return render_template('completedMaintenance.html', items=items, item_cost_sum=round(item_cost_sum, 2))



@app.route('/markComplete/<int:item_id>', methods=['GET', 'POST'])
def mark_complete(item_id):
    completed_item = MaintenanceItem.query.filter_by(maintenanceID=item_id).first()
    completed_item.completionStatus=1
    completed_item.completionDate=datetime.now()
    db.session.commit()
    flash('Task marked as complete, added to Completed Tasks', category="success")
    return redirect(url_for('completed_maintenance'))

@app.route('/markIncomplete', methods=['GET','POST'])
def mark_incomplete():
    id = request.form['maintenanceID']
    
    reverted_item = MaintenanceItem.query.filter_by(maintenanceID=id).first()
    reverted_item.completionStatus=0
    db.session.commit()

    flash("\"" + reverted_item.name + "\"" + 
        " removed from COMPLETED to \'My Maintenance Tasks\'", category="danger")
    return redirect(url_for('maintenance'))


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
        item_to_edit.dueDate =form.dueDate.data
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
        flash('Account Created! Login!!', category='success')
        return redirect(url_for('login'))
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

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part in request')
            return redirect(request.url)
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('file ' + filename + ' successfully uploaded', category='success')
            #date = datetime.UtcNow
            file_to_add = UserFile(owner=current_user.id, filename=filename)
            db.session.add(file_to_add)
            db.session.commit()
            return redirect(url_for('my_files'))
        else:
            flash('File does not exist or is an invalid type of file, try again')
    return render_template('uploadFile.html')



@app.route('/downloadFile/<filename>', methods=['GET'])
def download_file(filename):
    file_path = app.config['UPLOAD_FOLDER'] + "//" + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
            sender='HouseBuddyApp@gmail.com', 
            recipients=[user.email])
    msg.body = f''' To reset your password for username- {user.username} , visit :
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please disregard this message
'''
    mail.send(msg)

@app.route('/resetPassword', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash('logged in, must be logged out to request password reset', category="danger")
        return redirect(url_for("home_page"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('email with password reset instructions was sent', category="info")
        return redirect(url_for('login'))
    return render_template('resetRequest.html', form=form)

@app.route('/resetPassword/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash('logged in, must be logged out to request password reset', category="danger")
        return redirect("home_page")
    user = User.verify_reset_token(token)

    if user is None:
        flash('Invalid or expired token', category="warning")
        return redirect(url_for('reset_password_request'))

    form = NewPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_password
        db.session.commit()
        flash('Password updated! ', category="success")
        return redirect(url_for('login'))
    return render_template('resetToken.html', form=form)

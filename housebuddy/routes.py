from housebuddy import app
from flask import render_template
from housebuddy.models import MaintenanceItem

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

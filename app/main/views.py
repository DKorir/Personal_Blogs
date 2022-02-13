from flask import render_template,redirect,url_for
from . import main
from flask_login import login_required

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')
@main.route('/login')
def login():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('login.html')
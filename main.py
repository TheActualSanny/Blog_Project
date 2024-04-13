from flask import Flask, render_template, url_for, redirect, request
from database import database_manager

main = Flask(__name__)
manager = database_manager()

@main.route('/', methods = ['GET', 'POST'])
def login_page():
    return render_template('login.html')


@main.route('/sign_up', methods = ['GET', 'POST'])
def submit_page():
    return render_template('signup.html')

@main.route('/result', methods = ['GET', 'POST'])
def show_result():
    username = request.form['username_register']
    password = request.form['password_register']
    credentials = {
        'user' : username,
        'pass' : password
    }
    if not manager.get_username(username):
        manager.insert_data(username, password)
        return render_template('register_success.html', **credentials)
    
@main.route('/blog', methods = ['GET', 'POST'])    
def main_website():
    username = request.form['username_login']
    password = request.form['password_login']
    
    if manager.account_checker(username, password):
        return '<p> I will kill myeslf with coding. I will become a god at programming. </p>'
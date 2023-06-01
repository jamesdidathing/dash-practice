from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app_package import app
from app_package.forms import LoginForm
from app_package.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    # Here we are creating mock posts for our page from different users
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'My favourite recipe is Lasagne :)'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The soup recipe needs more salt..'
        }
    ]
    # render_template will render the html to the page
    return render_template('index.html', title='Home', posts=posts)


# 'POST' method is sending data/whatever from the browser to the server, 'GET' is the 
# other way around.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
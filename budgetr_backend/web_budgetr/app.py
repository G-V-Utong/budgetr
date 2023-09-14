#!/usr/bin/python3
""" The auth part of the app """
from models import storage
from models.user import User
from uuid import uuid4
from flask import Flask, send_from_directory, render_template, url_for, redirect, flash, request, current_app, abort
# from flask import Flask, send_static_file
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
# from flask_appjs import AppJS
# from flask_bcrypt import Bcrypt
import secrets
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisissecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)

"""
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
"""

@app.route('/sign-up', strict_slashes=False, methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = storage.getUserEmail(User, email)
        """
        """
        if user:
            flash("Email already exists!!", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            last_name=last_name, password=generate_password_hash(
                            password1, method='scrypt'))
            storage.new(new_user)
            storage.save()
            login_user(new_user, remember=True)
            flash('Registration successful. Account created!!.',
                  category='success')
            return redirect(url_for('index'))
    return render_template("sign-up.html", user=current_user)


@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = storage.getUserEmail(User, email)
        userpw = storage.getUserpw(User, email)
        if user:
            if check_password_hash(userpw, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)

@app.route('/', methods=['GET'])
@login_required
def index():

    return render_template('app.html', user=current_user)
    # return send_from_directory('static', 'src/App.js')
    # return url_for('static', filename='App.js')

# ...
@app.route('/about/')
def about():
    return render_template('about.html', user=current_user)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.teardown_appcontext
def close(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

"""
if __name__ == "__main__":

    h = getenv("budgetr_API_HOST")
    host = "0.0.0.0" if not h else h
    port = 5000 if not getenv("budgetr_API_PORT") else getenv("budgetr_API_PORT")

    app.run(host=host, port=port, threaded=True)
"""

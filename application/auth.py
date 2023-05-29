"""Routes for authentication."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user

from application import login_manager
from application.forms import LoginForm, SignupForm
from application.models import db, User

# Blueprint Configuration
auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up form to create a new user accounts.
    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to dashboard.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(name=form.name.data, email=form.email.data, website=form.website.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit() # Create new user
            login_user(user) # Log in as newly created user
            print(user)
            return redirect(url_for('main.dashboard'))
        flash('A user already exists with that email address.')
    return render_template('signup.jinja2',
                           title='Create an Account.',
                           form = form,
                           template="signup-page",
                           body='Sign up for a user account.')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Validate Login Attempt
        if user and user.check_password(password = form.password.data):
            login_user(user)
            next_page = request.args.get('next') # If login is successful, store the page  that the user was trying to access
            return redirect(next_page or url_for('main.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth.login'))
    return render_template('login.jinja2',
                           form=form,
                           title='Log in.',
                           template = 'login-page',
                           body='Login with your User account.')

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for('auth.login'))
import functools
from flask import Blueprint, g, redirect,\
                    render_template, request, session, url_for
from pymongo import MongoClient
from services.util import get_form_to_dict

auth_bp = Blueprint('auth', __name__, url_prefix='/', template_folder='../templates', static_folder='../static')
client = MongoClient("localhost", 27017)
db = client["pfe"]


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user."""
    if request.method == 'POST':
        dic = get_form_to_dict(request.form)
        error = None
        found = db.users.find_one({'email': dic["email"]})
        if not dic["username"]:
            error = 'Username is required.'
        elif not dic["password"]:
            error = 'Password is required'
        elif  found != None:
            error = 'Email already in use'

        if error is None:
                db.users.insert_one(dic)
                return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.register'))

    return render_template('register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = db.users.find_one({'email': email})

        if user is None:
            error = 'Incorrect email.'
        elif not user['password'] == password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['_id']
            return redirect(url_for('general.dashboard'))

    return render_template('login.html', title='Login')

@auth_bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.users.find_one({'_id': user_id})


@auth_bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def first_responder_required(view):
    """View decorator that redirects non-first_responders users to the home page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['accountType'] != 'first_responder':
            return redirect(url_for('general.dashboard'))

        return view(**kwargs)

    return wrapped_view

def investigator_required(view):
    """View decorator that redirects non-first_responders users to the home page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['accountType'] != 'investigator':
            return redirect(url_for('general.dashboard'))

        return view(**kwargs)

    return wrapped_view

def lawyer_required(view):
    """View decorator that redirects non-first_responders users to the home page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['accountType'] != 'lawyer':
            return redirect(url_for('general.dashboard'))

        return view(**kwargs)

    return wrapped_view
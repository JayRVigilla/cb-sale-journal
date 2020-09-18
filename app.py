"""Blogly application."""

from flask import Flask, redirect, render_template, request, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserForm, LoginForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///CB_sales_journal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
db.create_all()

#################
# Users Routes  #
#################

@app.before_request
def add_user_to_g():
    """If logged in: add curr_user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """ Render Login Screen and Auth from form data """
    return render_template(
        'userform.html',
        form=form,
        mode='Log In'
        )

@app.route('/')
def get_index():
    """ Redirects to list of all Users """
    return redirect("/users/")

@app.route('/users')
def get_users():
    """ Lists all users """
    users = User.query.all()
    return render_template(
        'userslist.html',
        users=users
    )

# @app.route('/users/new', methods=["GET", "POST"])
# def create_new_user_html():
#     """ Route to create new user form """
#     return render_template('userform.html')

@app.route('/users/new', methods=["GET", "POST"])
def add_new_user():
    """Create New User through form
    Creates then redirects to homepage.
    If form not valid, show form.
    If username is taken => flash message @ form
    """
    form = UserForm()
    """ Validate form """
    if form.validate_on_submit():
        try:
            new_user = User.register(
                        username=form.username.data,
                        password=form.password.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        img_url=form.img_url.data or User.img_url.default.arg,
                        status=form.status.data or User.status.default.arg,
                        )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template(
                'userform.html',
                form=form,
                mode='Add')
        do_login(new_user)
        return redirect("/users")
    else:
        return render_template('userform.html', form=form, mode='Add')


@app.route('/users/<username>')
def get_user(username):
    """ GET user data """
    current_user = User.query.filter_by(username=username).one()
    user_full_name = f"{current_user.first_name} {current_user.last_name}"
    img_url = current_user.img_url
    status = current_user.status

    return render_template(
        'userdetail.html',
        user=user_full_name,
        status=status,
        image_url=img_url,
        username=username
    )

@app.route('/users/<username>/edit')
def edit_user_html():
    """ Removes User from database """


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """ Removes User from database """

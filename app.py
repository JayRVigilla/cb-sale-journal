"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserForm, LoginForm
from models import db, connect_db, User

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

@app.route('/users/new', methods=["GET", "POST"])
def create_new_user_html():
    """ Route to create new user form """
    return render_template('userform.html')

@app.route('/users/new', methods="POST")
def add_new_user():
    """Create New User through form
    Creates then redirects to homepage.
    If form not valid, show form.
    If username is taken => flash message @ form
    """
    form = UserForm()
""" Validate form and Authenticates witness """
if form.validate_on_submit():
    try:
        if User.auth(form.w_username.data, form.w_pwd.data):
            try:
                User.register(
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
                return render_template('userform.html', form=form, mode='Add')

            # TODO log in user
            return redirect("/users")
        else:
            flash("Witnessing Member failed to authenticate", 'danger')
            return render_template('userform.html', form=form, mode='Add')

    except IntegrityError:
        flash("Username already taken", 'danger')
        return render_template('userform.html', form=form, mode='Add')
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

@app.route('users/<username>/edit')
def edit_user_html():
    """ Removes User from database """


@app.route('users/delete', methods="POST")
def delete_user():
    """ Removes User from database """

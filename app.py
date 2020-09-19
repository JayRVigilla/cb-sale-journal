"""Blogly application."""

from flask import Flask, redirect, render_template, request, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserForm, LoginForm, PrePopulatedForm
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
    """If logged in: add user to Flask global."""

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
        del g

# FIX doesn't redirect as a function
# def logged_in():
#     """ Redirects to /login if not logged in """
#     if  not g.user:
#         flash('You must be logged in.', 'danger')
#         return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """ Render Login Screen and Auth from form data """
    form = LoginForm()

    if form.validate_on_submit:
        user = User.auth(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", 'success')
            return redirect('/users')

        # flash('Invalid credentials', 'danger')

    return render_template(
        'userform.html',
        form=form,
        mode='Log In'
        )

@app.route('/logout', methods=["GET"])
def logout_user():
        do_logout()
        return redirect('/login')

@app.route('/')
def get_index():
    """ Redirects to login if no g.user
        else redirects to /users
    """
    if g.user:
        return redirect('users')
    return redirect('/login')


@app.route('/users')
def get_users():
    """ Lists all users """
    # logged_in()  # FIX won't redirect as function

    if  not g.user:
        flash('You must be logged in.', 'danger')
        return redirect('/login')

    users = User.query.all()
    return render_template(
        'userslist.html',
        users=users
    )


@app.route('/users/new', methods=["GET", "POST"])
def add_new_user():
    """Create New User through form
    Creates then redirects to homepage.
    If form not valid, show form.
    If username is taken => flash message @ form
    """
    if  not g.user:
        flash('You must be logged in.', 'danger')
        return redirect('/login')

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
            return render_template('userform.html', form=form, mode='Add')

        do_login(new_user)
        return redirect("/users")
    else:
        return render_template(
            'userform.html',
            form=form,
            mode='Add')


@app.route('/users/<int:id>')
def get_user(id):
    """ GET user data """

    if  not g.user:
        flash('You must be logged in.', 'danger')
        return redirect('/login')

    current_user = User.query.filter_by(id=id).first()
    user_full_name = f"{current_user.first_name} {current_user.last_name}"
    img_url = current_user.img_url
    status = current_user.status
    username = current_user.username

    return render_template(
        'userdetail.html',
        user=user_full_name,
        status=status,
        image_url=img_url,
        username=username,
        id=id
    )


@app.route('/users/<int:id>/edit', methods=["GET", "POST"])
def edit_user_html(id):
    """ Allows User to edit from form
    Successful edit redirects to detail page
    If form not valid, show form.
    """

    if  not g.user:
        flash('You must be logged in.', 'danger')
        return redirect('/login')

    form = UserForm()

    if form.validate_on_submit():
        user = User.auth(username=form.username.data,
            password=form.password.data)

        if user:
            user.username = form.username.data
            user.password = form.password.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.img_url = form.img_url.data
            user.status = form.status.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

        else:
            flash('Invalid credentials.', 'danger')
            return redirect('/')

    return render_template(
        'userform.html',
        form=form,
        mode='Edit')

# There will not be a route to delete users
# Change status instead to 'former_member' or 'former_candidate'


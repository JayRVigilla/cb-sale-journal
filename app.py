"""CB Sales Journal application.
    may rename this app.
    Contemplating adding more functions than just Sales Journal
"""

from flask import Flask, redirect, render_template, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import datetime
# from flask_login import LoginManager

from forms import UserForm, LoginForm, PrePopulatedForm, NewJournalEntry
from models import db, connect_db, User, SalesReport
from secrets import APP_SECRET
from aqi import get_aqi
from weather_api import get_weather
import pdb

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///CB_sales_journal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = APP_SECRET
toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

#################
# Users Routes  #
#################


@app.before_request
def add_user_to_g():
    """If logged in: add curr_user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# FIX doesn't redirect as a function
# def logged_in():
#     """ Redirects to /login if not logged in """
#     if  not g.user:
#         flash('You must be logged in.', 'danger')
#         return redirect('/login')


@app.route('/TBD', methods=["GET"])
def unknown_path():
    """ Under Construction Routes """
    return render_template('tbd.html')


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """ Render Login Screen and Auth from form data """
    form = LoginForm()

    if form.validate_on_submit:
        user = User.auth(form.l_username.data,
                         form.l_password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", 'success')
            return redirect('/')
        else:
            flash('Invalid credentials', 'danger')

    return render_template(
        'userform.html',
        form=form,
        mode='Log In'
        )


@app.route('/logout', methods=["GET"])
def logout_user():
    do_logout()
    flash("You're logged out.", 'success')
    return redirect('/login')


@app.route('/')
def get_index():
    """ Redirects to login if no g.user
        else redirects to /users
    """
    if g.user:
        return render_template('hub.html', user=g.user)
    return redirect('/login')


@app.route('/users')
def get_users():
    """ Lists all users """
    # logged_in()  # FIX won't redirect as function

    if not g.user:
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
    if not g.user:
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
        return redirect("/users")
    else:
        return render_template(
            'userform.html',
            form=form,
            mode='Add')


@app.route('/users/<int:id>')
def get_user(id):
    """ GET user data """

    if not g.user:
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

    if not g.user:
        flash('You must be logged in.', 'danger')
        return redirect('/login')

    form = PrePopulatedForm(obj=g.user)
    verify_form = LoginForm()

    if form.validate_on_submit() and verify_form.validate_on_submit():
        user = User.auth(verify_form.l_username.data,
                         verify_form.l_password.data)

        if user:
            user.username = form.username.data
            user.password = User.hash_pwd(form.password.data)
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.img_url = form.img_url.data or form.img_url.default
            user.status = form.status.data

            db.session.commit()

            return redirect(f"/users/{user.id}")

        else:
            flash('Invalid credentials.', 'danger')
            return redirect('/')

    return render_template(
        'useredit.html',
        form=form,
        verify_form=verify_form,
        mode='Edit')

# There will not be a route to delete users
# Change status instead to 'former_member' or 'former_candidate'
# Move to an archive db? save id, id of user who deleted, data as object

#######################
# Sales Report Routes #
#######################


sr_URL = '/reports/sales'


# get_report(s) - GET
@app.route(f"{sr_URL}/<int:id>", methods=["GET"])
def get_report():
    """ GETs report of specific date
    OR of a range of dates """


# create_report - POST
@app.route(f"{sr_URL}/new", methods=["GET", "POST"])
def new_report():
    """ POSTs report to DB
    if not logged in redirect to login
    if form valid then commit to db
    else render form
    """
    if not g.user:
        flash('You must be logged in.', 'danger')
        return redirect('/login')

    form = NewJournalEntry()
    verify_form = LoginForm()

    if form.validate_on_submit() and verify_form.validate_on_submit():
        user = User.auth(verify_form.l_username.data,
                         verify_form.l_password.data)
        if (user.id != g.user.id) and (user.status != 'member' or 'emeritus'):
            try:
                report = SalesReport(
                    # TODO should be pulled from g.user
                    member_id=g.user.id,
                    date=datetime.date.today(),
                    racks_am=form.am_racks.data,
                    racks_pm=form.pm_racks.data,
                    gf=form.gf.data,
                    vegan=form.vegan.data,
                    vgf=form.vgf.data,
                    sales=form.sales.data,
                    pizza=form.pizza.data,
                    notes=form.notes.data,
                    # weather=get_weather(),
                    weather='weather',  # from external API
                    aqi=get_aqi(),
                    witness_id=user.id,
                )
                db.session.add(report)
                db.session.commit()
                return redirect('/')

            except IntegrityError:
                flash('form not valid')
                return redirect(f"{sr_URL}/new")
        else:
            flash('Witnessing Member not valid')
            return redirect(f"{sr_URL}/new")
    else:
        return render_template(
            'salesreport.html',
            form=form,
            verify_form=verify_form,
            user=g.user,
            )

    return render_template(
        'salesreport.html',
        form=form,
        verify_form=verify_form,
        user=g.user,
        mode='Submit'
    )


# edit_report - POST GET
@app.route(f"{sr_URL}/edit", methods=["GET", "POST"])
def edit_report():
    """ edits report on certain date"""


# delete report - though this should not destroy record but move to archive db

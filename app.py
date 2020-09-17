"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

from flask_debugtoolbar import DebugToolbarExtension

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

@app.route('/users/new')
def create_new_user_html():
    """ Route to create new user form"""
    return render_template('newuserform.html')

@app.route('/users/new', methods="POST")
    """ POST new user to database """"
def add_new_user():
    """ Takes form data to create new user """
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    username = request.form['username']
    password = request.form['password'] # TODO needs to be hashed password
    img_url = request.form['imageURL']
    status = request.form['status']

    # new_user = User(
    #     username=username,
    #     first_name=first_name,
    #     last_name=last_name,
    #     password=password,
    #     img_url=img_url
    #     status=status
    # )

    new_user = User.register(cls,
                username,
                password,
                first_name,
                last_name,
                img_url,
                status)

    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<username>')
    """ GET user data """
    def get_user(username):
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

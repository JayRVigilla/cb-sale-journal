""" Models for CD Sales Journal"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """ Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Class for User"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True)
    username = db.Column(
            db.String,
            nullable=False)
    first_name = db.Column(
            db.String,
            nullable=False)
    last_name = db.Column(
            db.String,
            nullable=False)
    img_url = db.Column(
            db.String,
            default='https://i.pinimg.com/originals/b4/00/85/b400851a6b07f8877a9236f275bd8d4f.jpg')
    password = db.Column(
            db.String,
            nullable=False)
    # viable options will be candidate, member, emeritus, former_member
    status = db.Column(
            db.String,
            default='candidate')

    @classmethod
    def register(cls, username, password, first_name, last_name, img_url, status):
        """ Register new user """
        hashed = bcrypt.generate_password_hash(password).decode("utf8")

        user = User(
                username=username,
                password=hashed,
                first_name=first_name,
                last_name=last_name,
                img_url=img_url,
                status=status
                )
        db.session.add(user)
        return user

    @classmethod
    def auth(cls, username, password):
        """ Authenticate user """
        u = User.query.filter_by(username=username).first()

        if u:
            is_auth = bcrypt.check_password_hash(u.password, password)
            if is_auth:
                return u
        return False

    @classmethod



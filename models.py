""" Models for CD Sales Journal"""

from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

def connect_db(app):
    """ Connect to database"""

      db.app = app
      db.init_app(app)

class User(db.Model):
    """ Class for User"""

    __tablename__ = 'users'

    username = db.Column(
                db.String,
                primary_key=True,
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
        hashed = bcrypt.generate_password(password)
        hashed_utf8 = hashed.decode("utf8")

    return cls(username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            img_url=img_url,
            status=status
            )

    @classmethod
    def auth(cls, username, password):
        """ Authenticate user """
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password)
        return u
        else:
            return False

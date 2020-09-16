""" Models for CD Sales Journal"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  """ Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
  """ Class for User"""

  __tablename__ = 'users'

  id = db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)
  first_name = db.Column(
              db.String,
              nullable=False)
  last_name = db.Column(
              db.String,
              nullable=False)
  img_url = db.Column(
              db.String,
              default='https://i.pinimg.com/originals/b4/00/85/b400851a6b07f8877a9236f275bd8d4f.jpg')
  hashed_password = db.Column(
              db.String,
              nullable=False)
  # viable options will be candidate, member, emeritus, former_member
  status = db.Column(
              db.String,
              default='candidate')
              
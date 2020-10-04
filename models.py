""" Models for CD Sales Journal"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# import datetime


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
        nullable=False,
        unique=True)
    first_name = db.Column(
        db.String,
        nullable=False)
    last_name = db.Column(
        db.String,
        nullable=False)
    img_url = db.Column(
        db.String,
        default='https://i.pinimg.com/originals/b4/00/85/b400851a6b07f8877a9236f275bd8d4f.jpg'
        )
    password = db.Column(
        db.String,
        nullable=False)
    # options will be candidate, member, emeritus, former_member
    status = db.Column(
        db.String,
        default='candidate')

    @classmethod
    def hash_pwd(cls, password):
        return bcrypt.generate_password_hash(password).decode("utf8")

    @classmethod
    def register(cls,
                 username,
                 password,
                 first_name,
                 last_name,
                 img_url,
                 status):

        """ Register new user """

        user = User(
            username=username,
            password=User.hash_pwd(password),
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
            if bcrypt.check_password_hash(u.password, password):
                return u
        else:
            return False


class SalesReport(db.Model):
    """ Class for SalesReports """

    __tablename__ = 'sales-reports'

    id = db.Column(
        db.Integer,
        primary_key=True)
    member_id = db.Column(
        db.Integer,
        nullable=False)
    date = db.Column(
        db.DateTime,
        # default=datetime.date,
        nullable=False)
    racks_am = db.Column(
        db.Float,
        nullable=False)
    racks_pm = db.Column(
        db.Float,
        nullable=False)
    gf = db.Column(
        db.Integer,
        nullable=False)
    vegan = db.Column(
        db.Integer,
        nullable=False)
    vgf = db.Column(
        db.Integer,
        nullable=False)
    sales = db.Column(
        db.Float,
        nullable=False)
    pizza = db.Column(
        db.String,
        nullable=False)
    notes = db.Column(
        db.String,
        nullable=False)
    weather = db.Column(
        db.String,
        nullable=False)  # TODO received from third party api
    aqi = db.Column(
        db.Integer,
        nullable=False)  # TODO received from third party api
    witness_id = db.Column(
        db.Integer,
        nullable=False)

    @classmethod
    def create_report(
        cls,
        member_id,
        date,
        racks_am,
        racks_pm,
        gf,
        vegan,
        vgf,
        sales,
        pizza,
        notes,
        weather,
        aqi,
        witness_id
    ):
        """ Creates new sales report to db """

        report = SalesReport(
            member_id,
            date,
            racks_am,
            racks_pm,
            gf,
            vegan,
            vgf,
            sales,
            pizza,
            notes,
            weather,
            aqi,
            witness_id
        )

        return report

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, URL, Optional

class UserForm(FlaskForm):
    """ Form for adding users, includes member witness data """

    username = StringField('Username', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    img_url = URL('Username', validators=[Optional()])
    status = SelectField('Membership Status', choices=[('candidate', 'Candidate'), ('member', 'Member'), ('emeritus', 'Emeritus'), ('former_member', 'Former Member')], validators=[Optional()])

    w_username = StringField('Username', validators=[InputRequired()])
    w_pwd = PasswordField('Password', validators=[InputRequired()])

class LoginForm(FlaskForm):
    """" Login form """ "

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

    language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
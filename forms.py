from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import (InputRequired, Length, URL, Optional)
# from wtforms_alchemy import model_form_factory


class UserForm(FlaskForm):
    """ Form for adding users, includes member witness data """
    username = StringField('Username', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=6)])
    img_url = StringField(
        'Image URL',
        validators=[
            URL(),
            Optional(strip_whitespace=True)])
    status = SelectField(
        'Membership Status',
        choices=[
            ('candidate', 'Candidate'),
            ('member', 'Member'),
            ('emeritus', 'Emeritus'),
            ('former_member', 'Former Member')],
        validators=[Optional()])


class LoginForm(FlaskForm):
    """" Login form """

    l_username = StringField('Username', validators=[InputRequired()])
    l_password = PasswordField(
                'Password',
                validators=[
                    InputRequired(),
                    Length(min=6)]
                )


class PrePopulatedForm(UserForm):
    """ PrePopulatedForm takes UserForm Object
        allows form to render with pre-existing values

        example: PrepopulatedForm(obj=UserForm)
    """


class SalesReport(FlaskForm):
    """" Form for nightly sales reporting """

    am_racks = IntegerField('am_racks', validators=[InputRequired()])
    pm_racks = IntegerField('pm_racks', validators=[InputRequired()])
    gf = IntegerField('gf', validators=[InputRequired()])
    vegan = IntegerField('vegan', validators=[InputRequired()])
    vgf = IntegerField('vgf', validators=[InputRequired()])
    sales = IntegerField('sales', validators=[InputRequired()])
    pizza = StringField('pizza', validators=[InputRequired()])
    notes = StringField('notes', validators=[InputRequired()])

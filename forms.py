from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SelectField,
                     IntegerField,
                     TextAreaField,
                     SelectMultipleField,
                     )
from wtforms.fields.html5 import DateField
from wtforms.validators import (InputRequired, Length, URL, Optional)
# from wtforms_alchemy import model_form_factory
# import datetime


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
            ('former_member', 'Former Member'),
            ('former_candidate', 'Former Candidate'),
            ], validators=[Optional()])


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


class JournalEntry(FlaskForm):
    """" Form for nightly sales reporting """

    am_racks = IntegerField('am_racks', validators=[InputRequired()])
    pm_racks = IntegerField('pm_racks', validators=[InputRequired()])
    gf = IntegerField('gf', validators=[InputRequired()])
    vegan = IntegerField('vegan', validators=[InputRequired()])
    vgf = IntegerField('vgf', validators=[InputRequired()])
    sales = IntegerField('sales', validators=[InputRequired()])
    pizza = StringField('pizza', validators=[InputRequired()])
    notes = TextAreaField('notes', validators=[InputRequired()])

class EditJournalEntry(JournalEntry):
    """ Prepopulates Journal entry form for editing """

class SearchSalesReports(FlaskForm):
    """ For for searching Sales Reports """

    # Dates: radio for on a date OR between dates
    date_on = DateField('On Date', format='%Y-%m-%d')
    date_from = DateField('from date', format='%Y-%m-%d')
    date_to = DateField('to date', format='%Y-%m-%d')
    # Day: Which day of the week? check boxes
    day = SelectMultipleField('On a day', choices=[('monday', 'Mon'),
                                     ('tuesday', 'Tues'),
                                     ('wednesday', 'Wed'),
                                     ('thursday', 'Thurs'),
                                     ('friday', 'Fri'),
                                     ('saturday', 'Sat'),
                                     ('sunday', 'Sun'),
                                      ])
    # Pizza: contains any of the listed ingredients --> comma or space separate multiples?
    
    # Rack Count AM: greater than, equal to, or less than check boxes and number input
    # Rack Count PM
    # Sales: greater than, equal to, or less than check boxes and number input
    # Notes: contains any of the search terms --> comma or space separate multiples?
    # Weather: same
    # Member: must be int
    # Witness: must be int

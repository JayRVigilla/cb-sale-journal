from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SelectField,
                     IntegerField,
                     TextAreaField,
                     SelectMultipleField,
                     widgets,
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


# https://gist.github.com/juzten/2c7850462210bfa540e3
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# class CompareNumberField(SelectField):
#     widget = widgets.TextInput()


class SearchSalesReports(FlaskForm):
    """ For for searching Sales Reports """

    # Dates: radio for 'on a date' OR 'between dates'
    # date_sort = SelectField('Sort By Date', choices=[
    #     DateField('On Date', format='%Y-%m-%d'),
    #     DateField('from date', format='%Y-%m-%d'),
    #     DateField('to date', format='%Y-%m-%d')
    # ])
    date_on = DateField('On Date', format='%Y-%m-%d')
    date_from = DateField('from date', format='%Y-%m-%d')
    date_to = DateField('to date', format='%Y-%m-%d')
    # Day: Which day of the week? check boxes
    day = MultiCheckboxField('On a day', choices=[('monday', 'Mon'),
                                                  ('tuesday', 'Tues'),
                                                  ('wednesday', 'Wed'),
                                                  ('thursday', 'Thurs'),
                                                  ('friday', 'Fri'),
                                                  ('saturday', 'Sat'),
                                                  ('sunday', 'Sun'),
                                                  ])
    # Pizza: contains any of the listed ingredients -->
    #   comma or space separate multiples?
    pizza = StringField('pizza ingredients')
    # Rack Count AM: <, =, > than check boxes and number input
    am_racks = IntegerField('AM Racks')
    # Rack Count PM
    pm_racks = IntegerField('PM Racks')
    gf = IntegerField('gf')
    vegan = IntegerField('vegan')
    vgf = IntegerField('vgf')
    # Sales: greater than, equal to, or less than check boxes and number input
    sales = IntegerField('sales')
    # Notes: contains any of the search terms -->
    #   comma or space separate multiples?
    notes = StringField('notes')
    # Weather: same
    weather = StringField('Weather')
    aqi = IntegerField('Weather')
    # Member: must be int
    member = IntegerField('Member')
    # Witness: must be int
    witness = IntegerField('Witness')

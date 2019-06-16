from flask_wtf import Form
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired


class SearchForm(Form):
    choices = [('Stars', 'Stars'),
                ('Forks', 'Forks'),
                ('Contributors', 'Contributors')]
    select = SelectField('Sort repositories by:', choices=choices)
    search = StringField('', validators=[DataRequired()])

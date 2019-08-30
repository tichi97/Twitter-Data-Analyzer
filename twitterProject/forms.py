from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    name = StringField('Enter a username', validators=[DataRequired()])
    submit = SubmitField('Search')

class TrendForm(FlaskForm):
    name = StringField('Enter a trend topic', validators=[DataRequired()])
    submit = SubmitField('Search')

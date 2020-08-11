from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    name = StringField('Enter a username', validators=[InputRequired()])
    submit = SubmitField('Search')

class TrendForm(FlaskForm):
    trend = StringField('Enter a trend or topic', validators=[InputRequired()])
    trendsubmit = SubmitField('Search')

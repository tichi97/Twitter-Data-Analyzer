from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b1550409f9179f616eeae71d4710b0be'

from twitterProject import routes

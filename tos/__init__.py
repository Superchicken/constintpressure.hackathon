from flask import Flask, g, render_template
from tos.blueprints.terms import terms

# app configuration
app = Flask(__name__)
app.config.from_object('tos.settings')


app.register_blueprint(terms, url_prefix='/terms')


# index
@app.route('/')
def hello():
    return render_template('base.html')

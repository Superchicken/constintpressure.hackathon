from flask import Flask, g, render_template
from tos.blueprints.services import services
from tos.blueprints.agreements import agreements
from firebase import firebase

from tos import settings


# app configuration
app = Flask(__name__)
app.config.from_object('tos.settings')
app.register_blueprint(services, url_prefix='/services')
app.register_blueprint(agreements, url_prefix='/agree')


# app handlers
@app.before_request
def before_request():
    # firebase configuration
    if not hasattr(g, 'firebase'):
        g.firebase = firebase.FirebaseApplication(settings.FIREBASE_URL, None)


# index
@app.route('/')
def index():
    return render_template('base.html')

from flask import Blueprint, jsonify


terms = Blueprint('terms', __name__)


@terms.route('/something')
def something():
    return jsonify(data=dict(hello='there'))
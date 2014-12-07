from flask import Blueprint, g, jsonify, request
from webargs import Arg
from webargs.flaskparser import use_args


services = Blueprint('services', __name__)


service_args = {
    'data': Arg(dict),
    'name': Arg(unicode),
    'full_terms_url': Arg(str)
}


@services.route('', methods=['POST'])
@use_args(service_args)
def post_services(args):
    """
    Sample Request data:

    {
      "name": NAME,
      "data": {
        "terms": [
          {
            "policy_name" : POLICY_NAME,
            "policy_desc": POLICY_DESC,
            "policy_values": POLICY_OPTIONS
          },
        ],
        "full_terms_url": URL
      }
    }
    """
    
    data = request.get_json()
    
    try:
        result = g.firebase.put('/services',
                                args.get('name', None),
                                args.get('data', {}),
                                params={'print': 'silent'},
                                headers={'X_FANCY_HEADER': 'VERY FANCY'})
    except:
        pass
    
    return jsonify({'success': True})


@services.route('/', methods=['GET'])
def get_services():
    """ Get the collection of all services
    """
    
    result = g.firebase.get('/services', None)
    return jsonify(dict(services=result))
    
    
@services.route('/<service_id>', methods=['GET'])
def get_service(service_id):
    """ Get a single service's data
    """

    result = g.firebase.get('/services', service_id)
    return jsonify(dict(service=result))

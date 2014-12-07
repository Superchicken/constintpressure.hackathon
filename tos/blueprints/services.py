from flask import Blueprint, g, jsonify, request


services = Blueprint('services', __name__)


@services.route('', methods=['POST'])
def post_services():
    """
    Sample Request data:
    
    {
      "name": NAME,
      "data": {
        "terms": {
              "TERM" : [OPTIONS]
        },
        "full_terms_url": URL
      }
    }
    """
    
    data = request.get_json()
    
    try:
        result = g.firebase.put('/services',
                                data.get('name', None),
                                data.get('data', {}),
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

import hashlib
from flask import Blueprint, g, jsonify, request


agreements = Blueprint('agreements', __name__)


@agreements.route('', methods=['POST'])
def agree():
    """ Insert Agreements from user into database
    
    Sample Request data:
    
    {
      "user": EMAIL_ADDRESS,
      "service": SERVICE,
      "terms": {
        "TERM" : VALUE
      },
      "email_verified": false
    }
    """
    
    data = request.get_json()
    data['email_verified'] = False
    
    
    # check index for existence, GET
    user_service_key = '{0}:{1}'.format(data.get('user'),
                                        data.get('service'))
    hash_value = hashlib.sha224(user_service_key).hexdigest()
    
    try:
        hash_exist = g.firebase.get('/agreements_index', hash_value)
    except:
        hash_exist = None
    
    
    if not hash_exist:
        # write to agreements with hash, PUT
        try:
            result = g.firebase.post('/agreements',
                                     data,
                                     params={'print': 'pretty'},
                                     headers={'X_FANCY_HEADER': 'VERY FANCY'})
            
             # write hash to index, PUT  
            index_result = g.firebase.put('/agreements_index',
                                     hash_value,
                                     result.get('name'),
                                     params={'print': 'silent'},
                                     headers={'X_FANCY_HEADER': 'VERY FANCY'})
                                 
        except Exception, e:
            result = None
    else:
        result = None
    
    # email agreement
    return jsonify({'agreement': result})

from collections import OrderedDict
from datetime import datetime
import hashlib
import os
import smtplib

from email.mime.text import MIMEText
from flask import abort, Blueprint, g, jsonify, request, render_template
from premailer import transform
from webargs import Arg
from webargs.flaskparser import use_args

from tos import settings


agreements = Blueprint('agreements', __name__)


def valid_terms(args):
    """ Form validation for service terms
    """

    result = g.firebase.get('/services', args.get('service'))

    if result is None:
        return False

    try:
        terms = args.get('terms', [])

        if len(terms) > 0:
            for agree_term in terms:
                policy = agree_term.get('name')
                value = agree_term.get('value')

                # find the policy name in the terms array
                found_policy = False
                for service_term in result.get('terms', []):
                    if policy == service_term.get('policy_name') and \
                       value in service_term.get('policy_values', []):
                        found_policy = True
                        break

                if found_policy == False:
                    return False
        else:
            return False

    except ValueError:
        return False

    return True


agreement_args = {
    'user': Arg(unicode),
    'service': Arg(unicode),
    'terms': Arg(list, default=[])
}


@agreements.route('', methods=['POST'])
@use_args(agreement_args)
def agree(args):
    """ Insert Agreements from user into database

    Sample Request data:

    {
      "user": EMAIL_ADDRESS,
      "service": SERVICE,
      "terms": [
        {
          "name": POLICY_NAME,
          "value": POLICY_VALUE
        }
      ]
    }
    """

    # Validation
    args['email_verified'] = False
    if not valid_terms(args):
        return abort(400)

    # Check index for existence, GET
    # Where is my database integrity firebase?
    user_service_key = '{0}:{1}'.format(args.get('user'),
                                        args.get('service'))
    hash_value = hashlib.sha224(user_service_key).hexdigest()

    try:
        hash_exist = g.firebase.get('/agreements_index', hash_value)
    except:
        hash_exist = None

    if hash_exist is None:
        # Write to agreements with hash, POST
        try:
            result = g.firebase.post('/agreements',
                                     args,
                                     params={'print': 'pretty'},
                                     headers={'X_FANCY_HEADER': 'VERY FANCY'})

             # Write hash to index, PUT
            index_result = \
                g.firebase.put('/agreements_index',
                               hash_value,
                               result.get('name'),
                               params={'print': 'silent'},
                               headers={'X_FANCY_HEADER': 'VERY FANCY'})
                                 
        except Exception, e:
            result = None
    else:
        result = None

    # send email
    if result:
        # render template with agreement information
        terms = OrderedDict()
        for term in args.get('terms', []):
            policy, value = term.get('name'), term.get('value')
            terms[policy] = value

        activation_id=result.get('name')
        context = dict(terms=terms,
                       service=args.get('service'),
                       activate_link='{0}#/activate/{1}'.
                                      format(request.url_root, activation_id),
                       deactivate_link=\
                            '{0}#/deactivate/{1}'.\
                            format(request.url_root, activation_id))
                       
        template = render_template('email.html', **context)

        # format the email
        email_subject = \
            'Your Terms of Service Agreement With {0} - {1}'.\
            format(args.get('service'),
                   datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

        headers = '\r\n'.join(['from: {}'.format(settings.SMTP_USERNAME),
                               'subject: {}'.format(email_subject),
                               'to: {}'.format(args.get('user')),
                               'mime-version: 1.0',
                               'content-type: text/html'])

        # fancy premailer email
        email = '{0}{1}{2}'.format(headers, '\r\n\r\n', transform(template))

        # send the email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls() # required by gmail
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail('ethanholmes@deepaksandhu.com',
                        args.get('user'),
                        email)
        server.quit()

        # email agreement
        return jsonify(dict(success=True))

    return jsonify(dict(success=False))


@agreements.route('/<firebase_agreement_id>', methods=['PUT'])
def put_activate(firebase_agreement_id):
    """ Activation Link Clicked
        Update email_verified in database
    """
    try:
        agreement_node = g.firebase.get('/agreements/', firebase_agreement_id)
    except:
        agreement_node = None
        
    if agreement_node is None:
        return jsonify(dict(success=False,
                            message='Invalid ID'))

    email_verified = agreement_node.get('email_verified')
    
    if email_verified == True:
        return jsonify(dict(success=False,
                            message='This email has already been verified'))
    try:
        put_result = \
            g.firebase.put('/agreements/{}'.format(firebase_agreement_id),
                            'email_verified',
                            True,
                            params={'print': 'pretty'},
                            headers={'X_FANCY_HEADER': 'VERY FANCY'})
    except:
        return jsonify(dict(success=False,
                            message='Failure inserting data, sorry :\'('))
                                
    return jsonify(dict(success=True,
                        message='You have successfully verified you\'re human'))


@agreements.route('/<service_id>/<user_email>', methods=['GET'])
def get_validated(service_id, user_email):
    """ Let Companies Ask us if an email is registered to their service
        Give them a list of terms the user has/hasn't agreed to
    """

    try:
        agreements = g.firebase.get('/agreements', None)
        for agreement_id, agreement_body in agreements.iteritems():
            if agreement_body.get('user') == user_email:
                terms = agreement_body.get('terms')
                return jsonify(dict(valid=True, terms=terms))
    except:
        return jsonify(dict(valid=False))


@agreements.route('/notme/<firebase_agreement_id>', methods=['DELETE'])
def delete_deactive(firebase_agreement_id):
    """ This isn't me link clicked
        Remove db entries for that agreement
    """

    agreement = g.firebase.get('/agreements', firebase_agreement_id)

    if agreement is None:
        return jsonify(dict(success=False, message='Invalid ID'))

    if agreement.get('email_verified') == True:
        return jsonify(dict(success=False, message='ID already activated'))

    user_service_key = '{0}:{1}'.format(agreement.get('user'),
                                        agreement.get('service'))
    hash_value = hashlib.sha224(user_service_key).hexdigest()

    g.firebase.delete('/agreements', firebase_agreement_id)
    g.firebase.delete('/agreements_index', hash_value)

    return jsonify(dict(success=True, message='Successfully deactivated'))

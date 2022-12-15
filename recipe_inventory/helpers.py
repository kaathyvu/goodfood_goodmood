from functools import wraps
from flask import request, jsonify, json
import decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = request.json['token']
        if not token or token == 'none':
            return jsonify({'message': 'User sign-in required. Token is missing'}), 401
        
        return our_flask_function(token, *args, **kwargs)
    return decorated
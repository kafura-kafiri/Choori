import hashlib


def get_hexdigest(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg.encode())
    return m.hexdigest()


def set_password(raw_password):
    import random
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s$%s' % ('sha256', salt, hsh)


def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    algo, salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)

import jwt

# e_jwt = jwt.encode({'username': 'shahin', 'password': 'qarebaqi'}, 'secret', algorithm='HS256')
# payload = jwt.decode(e_jwt, 'secret', algorithms=['HS256'])
# print(payload)

from functools import wraps
from sanic.response import json


def roles_required(roles):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                key = request.form['key'][0] if request.form['key'][0] else request.args['key'][0]
                del[request.form['key']]
                payload = jwt.decode(key, 'secret', algorithms=['HS256'])
            except:
                return json({'status': 'not_authorized'}, 403)
            print('####')
            print(roles)
            print(payload['roles'])
            print('####')
            if not roles or (payload['roles'] and not set(payload['roles']).isdisjoint(roles)):
                rv = await f(request, payload, *args, **kwargs)
                return rv
            else:
                return json({'status': 'roles_disjoint', 'roles_required': roles}, 403)
        return decorated_function
    return decorator

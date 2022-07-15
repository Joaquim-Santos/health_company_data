import functools
from flask import request


def validate_request_local(func):
    @functools.wraps(func)
    def wrapper_validate_request(*args, **kwargs):
        if '/api/signup' in request.url:
            kwargs['user_credentials'] = {
                'authorization': 'Basic Sm9hcXVpbVNhbnRvczpOYXRoQDI2MDIyMDIw',
                'access-token': 'token_test'
            }
        else:
            kwargs.update({
                'user_credentials': {
                        'username': 'user_test',
                        'access-token': 'token_test'
                    }
            })

        return func(*args, **kwargs)

    return wrapper_validate_request

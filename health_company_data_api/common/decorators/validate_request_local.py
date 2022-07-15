import functools


def validate_request_local(func):
    @functools.wraps(func)
    def wrapper_validate_request(*args, **kwargs):
        kwargs.update({
            'user_credentials': {
                    'username': 'user_test',
                    'access-token': 'token_test'
                }
        })

        return func(*args, **kwargs)

    return wrapper_validate_request

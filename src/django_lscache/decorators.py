def lscache(view_func):
    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)
        return response

    return wrapper

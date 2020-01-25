def singleton(f):
    def wrapper():
        d = wrapper.__dict__

        try:
            return d['']
        except KeyError:
            d[''] = f()

        return d['']

    wrapper.__name__ = f.__name__

    return wrapper

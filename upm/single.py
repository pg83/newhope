def singleton(f):
    #return singleton3(f)
        
    code = """
def {name2}(f):
    def {name1}():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return {name1}
"""

    name1 = f.__name__.upper()
    name2 = (f.__module__ + '_holder').replace('.', '_')
    code = code.replace('{name1}', name1).replace('{name2}', name2)
    ctx = {'f': f}

    try:
        return __yexec__(code, module_name=f.__module__ + '.singleton')[name2](f)
    finally:
        ctx.clear()


class singleton3(object):
    __slots__ = ('f', 'r')
    
    def __init__(self, f):
        self.f = f

    def __call__(self):
        try:
            return self.r
        except AttributeError:
            self.r = self.f()
        
        return self.r


def singleton4(f):
    d = globals()
    
    def wrapper():
        key = f.__module__ + f.__name__

        try:
            return d[key]
        except KeyError:
            d[key] = f()

        return d[key]

    return wrapper


def singleton5(f):
    def wrapper():
        d = wrapper.__dict__
        
        try:
            return d['x']
        except KeyError:
            d['x'] = f()
            
        return d['x']

    return wrapper

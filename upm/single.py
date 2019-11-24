def singleton(f):
    return singleton3(f)
    
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


def singleton3(f):
    v = []

    def wrapper(*args, **kwargs):
        if not v:
            v.append(f(*args, **kwargs))

        return v[0]

    return wrapper

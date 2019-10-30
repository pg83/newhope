@y.singleton
def my_funcs():
    return {}


@y.singleton
def callbacks():
    return {}


@y.singleton
def all_my_funcs():
    return []


@y.lookup
def lookup(name):
    return my_funcs()[name]


def register_func_callback(func):
    callbacks()[func.__name__] = func


def main_reg(func, **kwargs):
    my_funcs()[func.__name__] = func

    return func


def register_func_generator(info):
    all_my_funcs().append(info)


register_func_callback(main_reg)

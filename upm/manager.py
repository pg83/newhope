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


@y.singleton
def defer_constructors():
    return []


def register_defer_constructor(f):
    defer_constructors().append(f)


def defer_constructor(func):
    register_defer_constructor(func)

    return func


def run_all_defer_constructors():
    for f in defer_constructors():
        f()


@y.singleton
def main_entry_points():
    return []


def register_entry_point(f):
    main_entry_points().append(f)


def main_entry_point(f):
    register_entry_point(f)

    return f


@y.singleton
def defer_constructors():
    return []


def register_defer_constructor(f):
    defer_constructors().append(f)


def defer_constructor(func):
    register_defer_constructor(func)

    return func


@defer_constructor
def main():
    if '/psy' in y.verbose:
        import atexit
        atexit.register(y.print_stats)
        

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


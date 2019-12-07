@y.singleton
def main_entry_points():
    return []


def register_entry_point(f):
    main_entry_points().append(f)


def main_entry_point(f):
    register_entry_point(('m', f))

    return f


def verbose_entry_point(f):
    register_entry_point(('v', f))

    return f

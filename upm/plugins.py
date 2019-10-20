from .iface import y


def load_plugins(where):
    y.load_plugins(where, globals())


load_plugins(['builtin'])

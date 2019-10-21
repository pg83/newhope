from upm_modlst import my_modules


def find_function(name):
    subst = {
        'xpath': 'run_xpath_simple'
    }

    name = subst.get(name, name)

    for m in my_modules().values():
        if name in m.__dict__:
            return m.__dict__[name]

    raise AttributeError(name)


class IFace(object):
    def __init__(self):
        self._c = {}

    def __getattr__(self, name):
        if name not in self._c:
            self._c[name] = find_function(name)

        return self._c[name]


y = IFace()

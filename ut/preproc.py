undefined = object()


@y.singleton
def is_debug():
    return 'preproc=debug' in ''.join(y.sys.argv)


class Defines(dict):
    def __init__(self, defs):
        self.__dict__ = self
        self.update(defs)

        def defined(x):
            is_debug() and print(x)
            return not x is undefined

        self.defined = defined

    def __missing__(self, key):
        is_debug() and print('missing', key)
        return undefined


class Preproc(object):
    def __init__(self, l, text):
        self.t = text
        self.d = Defines(l)
        self.r = []
        self.v = []

    def run(self):
        for l in self.t.split('\n'):
            _, val = self.command(l)
            self.r.append(val)

        return '\n'.join(self.r) + '\n'

    def command(self, l):
        ll = l.strip()

        if ll and ll[0] == '#':
            p = ll.find(' ')

            if p < 0:
                p = len(ll)

            cmd = ll[1:p]
            fill = l[:-len(ll)]

            try:
                f = getattr(self, 'do_' + cmd)
            except AttributeError:
                return False, l

            data = ll[p + 1:]
            res = f(data) or ''

            is_debug() and print(repr(cmd), repr(data), repr(fill + res), f.__name__)

            return True, fill + res

        return False, l

    def do_define(self, l):
        x, y = l.split(' ', 1)

        self.d[x] = eval(y, self.d)

        return x + ' = ' + repr(self.d[x])

    def do_undef(self, l):
        self.d.pop(l.strip())

        return 'del ' + l.strip()

    def do_if(self, l):
        self.v.append(False)
        return self.do_elif(l)

    def do_elif(self, l):
        if not self.v[-1]:
            is_debug() and print(l, eval(l, self.d))

            if eval(l, self.d):
                self.v[-1] = True

                return 'if 1:'

        return 'if 0:'

    def do_else(self, l):
        if self.v[-1] == False:
            self.v[-1] = True
            return 'if 1:'

        return 'if 0:'

    def do_endif(self, l):
        assert self.v.pop() is not None

    def do_exclude(self, l):
        if eval(l, self.d):
            is_debug() and print('will exclude ' + l)
            return 'if 0:'

        is_debug() and print('will include ' + l)
        return 'if 1:'

    def do_endex(self, l):
        pass

    def do_print_state(self, l):
        print '\n'.join(self.r)


@y.singleton
def global_defines():
    return {
        'arch': y.platform.machine(),
	'os': y.platform.system().lower(),
    }


def preprocess_text(text, defines=global_defines()):
    ps = y.globals.by_prefix
    fs = y.globals.file_data

    def check(*els):
        for el in els:
            el = chr(35) + el

            if el in ps and y.burn(text) in ps[el]:
                return True

    if check('if', 'ex'):
        try:
            return Preproc(defines, text).run()
        except Exception as e:
            raise Exception('shit happen while parsing ' + text) from e

    return text


__loader__._preproc = preprocess_text

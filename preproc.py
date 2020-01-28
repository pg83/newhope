undefined = object()


def split_0(x):
    a, b = x.split(' ', 1)

    return a.strip(), b.strip()


def get_spaces(x):
    ch = ''

    for ch in x:
         if ch in ' \t':
             res += ch

    return ch


class Undefined(dict):
    def __init__(self, d):
        self.__dict__ = self
        self.update(d)

        def defined(x):
            return x is not undefined

        self.defined = defined

    def __missing__(self, d):
        return undefined


def r0(self, v, d):
    if v == 'define':
        a, b = split_0(d)

        self._c._e._d[a] = b
    elif v == 'undef':
        self._c._e._d.pop(d)
    elif v == 'error':
        raise Exception('shit happen')
    else:
        return False

    return True


class Line(object):
    def __init__(self, l):
        self._l = l

    def render(self, emit):
        emit.emit_line(self._l)


class Else(object):
    def __init__(self, ctx, parent):
        self._c = ctx
        self._l = []
        self._p = parent

        for typ, val in self._c.tok:
            if typ == 's':
                self._l.append(Line(val))
            elif typ == 't':
                v, d = val

                if r0(self, v, d):
                    continue
                elif v == 'endif':
                    return
                elif v == 'if':
                    self._l.append(IfP(d, selr._c))

                    continue
                else:
                    print('bug else', typ, val)
                    assert False

    def render(self, emit):
        if self._p._u:
            return

        self._p._u = True

        for l in self._l:
            l.render(emit.clone())


class Elif(object):
    def __init__(self, ctx, parent, data):
        self._l = []
        self._c = ctx
        self._p = parent
        self._d = data

        for typ, val in self._c.tok:
            if typ == 's':
                self._l.append(Line(val))
            elif typ == 't':
                v, d = val

                if v == 'endif':
                    return
                elif v == 'else':
                    return self._l.append(Else(self._c, self._p))
                elif v == 'if':
                    self._l.append(IfP(d, self._c))

                    continue
                else:
                    print('bug elif', typ, val)
                    assert False

    def render(self, emit):
        if self._p._u:
            return

        self._p._u = True

        if eval(self._d, emit._d):
            for l in self._l:
                l.render(emit.clone())

class IfP(object):
    def __init__(self, data, ctx):
        self._l = []
        self._d = data
        self._c = ctx
        self._u = True

        for typ, val in self._c.tok:
            if typ == 's':
                self._l.append(Line(val))
            else:
                v, d = val

                if r0(self, v, d):
                    continue
                elif v == 'else':
                    return self._l.append(Else(self._c, self))
                elif v == 'elif':
                    return self._l.append(Elif(self._c, self, d))
                elif v == 'if':
                    self._l.append(IfP(d, self._c))
    
                    continue
                elif v == 'endif':
                    return
                else:
                    assert False

    def render(self, emit):
        self._u = True

        if eval(self._d, emit._d):
            for l in self._l:
                l.render(emit.clone())


class Root(object):
    def __init__(self, ctx):
        self._c = ctx
        self._l = []

    def run(self):
        for tp, val in self._c.tok:
            if tp == 's':
                self._l.append(Line(val))
            else:
                v, d = val

                if r0(self, v, d):
                    continue
                elif v == 'if':
                    self._l.append(IfP(d, self._c))
                else:
                    print('bug', v, d)
                    assert False

    def render(self, emit):
        for l in self._l:
            l.render(emit)


class Preproc(object):
    def __init__(self, d):
        self._d = Undefined(d)
        self._d['def'] = lambda x: (x in self._d)

    def run(self, text):
        class Ctx(object):
            def __init__(self, tok, emit):
                self.tok = tok
                self._e = emit

        class Emit(object):
            def emit_line(self, l):
                if self.skip:
                    pass
                else:
                    print(l[self.n * 4:])

            def __init__(self, skip, glob, n, parent):
                self._d = glob
                self.skip = skip
                self.n = n
                self.p = parent

            def clone(self):
                return Emit(self.skip, self._d, self.n + 1, self)

        emit = Emit(False, Undefined(self._d), 0, None)

        r = Root(Ctx(self.tokenize(text), emit))
        r.run()
        r.render(emit)

    def tokenize(self, text):
        for l in text.split('\n'):
            ll = l.strip()

            if ll and ll[0] == '#':
                ll = ll[1:]

                try:
                    func, params = ll.split(' ', 1)
                except ValueError:
                    func = ll
                    params = None
    
                yield ('t', (func, params))
            else:
                yield ('s', l)

    def render(self, emit):
        for x in self._l:
            x.render(Emit())

code = '''
print x

#define a 1

a + b == c

#define b 2

#if defined(a)
    #if defined(b)
        print(a + b)
    #else
        print(bad)
    #endif
    print y
#endif
'''

#Preproc({}).run(code)

with open('qw', 'r') as f:
    Preproc({}).run(f.read())


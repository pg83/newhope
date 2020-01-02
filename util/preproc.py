undefined = object()


class Defines(dict):
    def __init__(self, defs):
        self.__dict__ = self
        self.update(defs)

        def defined(x):
            print x
            return not x is undefined

        self.defined = defined

    def __missing__(self, key):
        print 'missing', key
        return undefined


class Preproc(object):
    def __init__(self, defines, text):
        self.t = text
        self.d = Defines(defines)
        self.s = ['C']
        self.r = []
        self.v = []
        
    def run(self):
        for l in self.t.split('\n'):
            print 'line', l, self.s[-1]
            res, val = self.command(l)
            
            if res:
                self.r.append(val)
            elif self.s[-1] == 'S':
                self.r.append('')
            elif self.s[-1] == 'C':
                self.r.append(l)

        #print self.v, self.s

        #assert len(self.v) == 0
        #assert len(self.s) == 1 and self.s[0] == 'C' 
                
        return '\n'.join(self.r)

    def command(self, l):
        ll = l.strip()
        
        if ll and ll[0] == '#':
            p = ll.find(' ')

            if p < 0:
                p = len(ll)

            cmd = ll[1:p]
            fill = l[:-len(ll)]

            try:
                f = getattr(self, 'do_' + self.s[-1].lower() + '_' + cmd)
            except AttributeError:
                return False, l

            data = ll[p + 1:]
            res = f(data) or ''
            
            print repr(cmd), repr(data), repr(fill + res), f.__name__

            return True, fill + res

        return False, l

    def do_c_define(self, l):
        x, y = l.split(' ', 1)
        
        self.d[x] = eval(y, self.d)

        print('do define', x, '=', self.d[x])
        
        return x + ' = ' + repr(self.d[x])
        
    def do_s_define(self, l):
        pass
    
    def do_c_undef(self, l):
        self.d.pop(l.strip())

        return 'locals().pop("' + l.strip() + '")'
        
    def do_s_undef(self, l):
        pass
    
    def do_c_if(self, l):
        self.s.append('C')
        self.v.append(False)
        self.do_c_elif(l)

    def do_s_if(self, l):
        self.v.append(None)

    def do_c_elif(self, l):
        self.s.pop()
        
        if not self.v[-1]:
            print l, eval(l, self.d)
            
            if eval(l, self.d):
                self.v[-1] = True
                self.s.append('C')
            else:
                self.s.append('S')
        else:
            self.s.append('S')

    def do_s_elif(self, l):
        pass

    def do_c_else(self, l):
        self.s.pop()
        
        if self.v[-1] == False:
            self.v[-1] = True
            self.s.append('C')
        else:
            self.s.append('S')

    def do_s_else(self, l):
        pass

    def do_c_endif(self, l):
        self.s.pop()
        assert self.v.pop() is not None

    def do_s_endif(self, l):
        if self.v.pop() is not None:
            self.s.pop()


@y.singleton
def global_defines():
    return {
        'arch': y.platform.machine(),
	'os': y.platform.system().lower(),
    }


def preprocess_text(text, defines=global_defines()):
    return text

    if '#' in text:
        res = Preproc(defines, text).run()

        print(res)
        
        return res

    return text


__loader__._preproc = preprocess_text

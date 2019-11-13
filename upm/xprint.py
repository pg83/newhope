def xxformat(*args, **kwargs):
    def iter_t():
        for x in args:
            yield x

        if 'text' in kwargs:
            yield kwargs.pop('text')

    text = ' '.join(y.fixx(x) for x in iter_t())

    return process_color(text, kwargs.pop('init', ''), kwargs)
                

def xxprint(*args, **kwargs):
    kwargs.pop('where', y.sys.stderr).write(xxformat(*args, **kwargs) + '\n')


def process_color(text, init, kwargs):
    verbose = kwargs.get('verbose', y.verbose)
    cm = y.color_map_func()
    rst = ('c', '')

    def process_part1(s, parts):
        text = parts.pop()

        while True:
            pos = text.find('{')
            
            if pos >= 0:
                break

            if not parts:
                break

            part = parts.pop()
            text = text + part

        if pos < 0:
            yield ('c', s[-1])
            yield ('t', text)
            yield rst

            return
        
        part = text[:pos]

        yield ('c', s[-1])
        yield ('t', part)
        yield rst

        text = text[pos:]
        pos = text.find('}')

        if pos < 0:
            yield ('c', s[-1])
            yield ('t', text)
            yield rst

            return

        nc = text[1:pos]
        next = text[pos + 1:]

        add = ''

        if nc not in cm:
            pp = nc.split(':')

            if len(pp) == 2 and pp[0] in cm:
                add = '{' + pp[0] + '}' + kwargs[pp[1]] + '{}'
            else:
                yield ('c', s[-1])
                yield ('t', text[:pos + 1])
                yield rst
        else:
            if nc in ('rst', 'reset', ''):
                s = s[:-1]
            else:
                s.append(nc)

        parts.append(next)
        
        if add:
            parts.append(add)

    def process_part(s, parts):
        while parts:
            #print sum([len(x) for x in c[1]], 0), c[1]

            for x in process_part1(s, parts):
                yield x

            while parts and not parts[-1]:
                parts.pop()

    def combine():
        s = [init or '']
        last = []

        def join(l):
            if l[0][0] == 'c':
                c = l[-1][1]
                
                if verbose and '/rc' in verbose:
                    return '[' + c + ']'

                return cm[c]
            else:
                return ''.join([x[1] for x in last])

        for p in process_part(s, [text]):
            if p[0] == 't' and not p[1]:
                continue

            if not last:
                last.append(p)
            else:
                if last[0][0] == p[0]:
                    last.append(p)
                else:
                    yield join(last)
                    last = [p]

        if last:
            yield join(last)

    return ''.join(combine())

        
@y.lookup
def lookup(xp):
    if xp.startswith('xprint_'):
        color=xp[7:]

        def func(*args, **kwargs):
            print >>y.sys.stderr, xxformat(*args, init=color, **kwargs)
        
        func.__name__ = xp

        return func

    raise AttributeError()

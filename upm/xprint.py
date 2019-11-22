def xxformat(*args, **kwargs):
    def iter_t():
        for x in args:
            yield x

        if 'text' in kwargs:
            yield kwargs.pop('text')

    text = ' '.join(y.fixx(x) for x in iter_t())

    if 'init' in kwargs:
        return '{' + kwargs['init'] + '}' + text + '{}'
    
    return text
                

def xxprint(*args, **kwargs):
    kwargs.pop('where', y.stderr).write(xxformat(*args, **kwargs) + '\n')


def process_color(text, init, kwargs):
    verbose = kwargs.get('verbose', y.verbose)
    raw = kwargs.get('raw', False)
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
                
                if raw:
                    return {'color': c}
                
                if verbose and '/rc' in verbose:
                    return '[' + c + ']'

                return cm[c]
            else:
                res = ''.join([x[1] for x in last])

                if raw:
                    return {'text': res}

                return res

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

    if raw:
        return list(combine())
            
    return ''.join(combine())

        
@y.lookup
def lookup(xp):
    if xp.startswith('xprint_'):
        color=xp[7:]

        def func(*args, **kwargs):
            xxprint(*args, init=color, **kwargs)
        
        func.__name__ = xp

        return func

    raise AttributeError()


def gen_text():
    return '{g}' + ('dhfkjgfsdjhfsdfhjkjdfhg' * 10 + '\n') * 10 + 'xxx{b}' + ('78653475347547' * 10 + '\n') * 5 + '{w}' + 'djfhdjkfgkjgf' * 10 + '{}' + ('73673578364583456' * 5 + '\n') * 10 + '{}'


def reduce_by_key(iter, keyf):
    tmp = []

    for i in iter:
        if not tmp:
            tmp.append(i)
        else:
            if keyf(i) == keyf(tmp[-1]):
                tmp.append(i)
            else:
                yield tmp
                tmp = [i]

    if tmp:
        yield tmp

        
def reshard_text(text, nn):
    def iter1():
        cur = None
    
        for i in process_color(text, '{}', dict(raw=True)):
            if 'color' in i:
                cur = i['color']
            else:
                for ch in i['text']:
                    yield (ch, cur)


    def split1():
        cur = []
        
        for ch in iter1():
            if ch[0] == '\n':
                yield cur
                cur = []
            else:
                cur.append(ch)

        if cur:
            yield cur

    def reshard_line(l, n):
        while l:
            yield l[:n]
            l = l[n:]
            
    def do():
        for l in split1():
            for sl in reshard_line(l, nn):
                yield list(reduce_by_key(sl, keyf=lambda x: x[1]))

    def combine(l):
        text = ''.join([x[0] for x in l])
        color = l[0][1]

        return {'text': text, 'color': color}

    def iter2():
        for l in do():
            yield [combine(x) for x in l]

    return list(iter2())

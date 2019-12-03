def xxformat(*args, **kwargs):
    def iter_t():
        for x in args:
            yield x

        if 'text' in kwargs:
            yield kwargs.pop('text')

    text = ' '.join(y.fixx(x) for x in iter_t())

    if 'init' in kwargs:
        text = '{' + kwargs['init'] + '}' + text + '{}'
    
    return text
                

def xxprint(*args, **kwargs):
    kwargs.pop('where', y.stderr).write(xxformat(*args, **kwargs) + '\n')


@y.singleton
def my_cm():
    return y.deep_copy(y.COLOR_TABLE)
    

def process_color(text, init, kwargs):
    verbose = kwargs.get('verbose', y.verbose)
    raw = kwargs.get('raw', False)
    cm = my_cm()
    rst = ('c', '')

    def process_stack(s, text):
        while text:
            p = text.find('{')

            if p < 0:
                yield ('t', text)

                return

            yield ('t', text[:p])

            text = text[p:]

            p = text.find('}')

            if p < 0:
                yield ('t', text)

                return

            c = text[:p + 1]
            text = text[p + 1:]

            if c == '{}':
                s.pop()
                
                yield ('c', s[-1])
            elif c in cm:
                s.append(c)

                yield ('c', c)
            else:
                yield ('t', c)
                
    out_txt = (verbose and '/rc' in verbose) or ('txt' in y.config.get('color', ''))

    def combine():
        s = [init or '']
        last = []

        def join(l):
            if l[0][0] == 'c':
                c = l[-1][1]
                
                if raw:
                    return {'color': c}

                if out_txt:
                    return c

                return cm[''] + cm[c]
            else:
                res = ''.join([x[1] for x in last])

                if raw:
                    return {'text': res}

                return res

        for p in process_stack(s, text):
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

    raise AttributeError(xp)



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


def run_color_test():
    text = '''
{w}{g}982{} | {b}18:32:34{} | {y}ut.iface    {} | {ds}D{} | {bs}will run defer constructors {}{}
{w}{g}982{} | {b}18:32:34{} | {y}ut.iface    {} | {ds}D{} | {bs}done {}{}
{w}{g}982{} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}spawn <coro entry_point, from <loop main>, created>{}{}
{w}{g}982{} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}spawn <coro flush_streams, from <loop main>, created>{}{}
{w}{g}958{} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}<coro entry_point, from <loop main>, created> step in{}{}
{w}{g}33 {} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}<coro flush_streams, from <loop main>, created> step in{}{}
{w}{g}33 {} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}<coro flush_streams, from <loop main>, suspended> step out{}{}
{w}{g}958{} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}<coro entry_point, from <loop main>, suspended> step out{}{}
{w}{g}345{} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}reschedule <coro entry_point, from <loop main>, suspended>{}{}
{w}{g}9  {} | {b}18:32:34{} | {y}ut.coro     {} | {ds}D{} | {bs}<coro entry_point, from <loop main>, suspended> step in{}{}
'''
    
    y.sys.stderr.write(process_color(text.strip() + '\n', '', {'verbose': '/rc'}))
    y.sys.stderr.flush()
    

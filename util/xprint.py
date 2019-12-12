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
    strip_colors = kwargs.get('strip_colors', False)
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

                if strip_colors:
                    return ''

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

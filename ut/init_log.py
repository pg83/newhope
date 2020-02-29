def get_log():
    f = y.sys._getframe()

    while 'init_log' in f.f_globals.__name__:
        f = f.f_back

    return f.f_globals.__ylog__()


@y.lookup
def log_lookup(name):
    if name in ('debug', 'info', 'warning', 'error', 'critical', 'exception'):
        def func(msg, *args, **kwargs):
            if not '%' in msg: 
                msg = msg + ' ' + ' '.join(str(x) for x in args)
                args = ()
            elif msg == '%s':
                msg = ' '.join(str(x) for x in args)
                args = ()

            return getattr(get_log(), name)(msg, *args, **kwargs)

        return func

    raise AttributeError()


class ColoredFormatter(y.logging.Formatter):
    def __init__(self, fmt):
        dls = {
            'protocol': '{s}',
            'debug': '{bs}',
            'info': '{g}',
            'verbose': '{b}',
            'warning': '{y}',
            'error': '{r}',
            'critical': '{r}',
        }

        for l in list(dls.keys()):
            dls[l.upper()[0]] = dls[l]

        self.styles = dls
        self.fmt = fmt

    def format(self, record):
        res = self.fmt
        extra = record.__dict__

        if 'status' not in extra:
            extra['status'] = 'none'

        if '_target' in extra:
            extra['target'] = extra.pop('_target')

        colors = {
            'fail': '{br}',
            'done': '{bb}',
            'init': '{by}',
            'fini': '{bc}',
            'none': '{bs}',
        }

        def replace(k, v):
            return res.replace('%(' + k + ')', v)

        def on_levelname(k, l):
            return replace(k, l[:1].upper())

        def on_status(k, s):
            c = colors.get(s, '{bw}')
            f = funcs['on_target']

            funcs['on_target'] = lambda k, v: f(k, v, color=c[2])

            return replace(k, (c + s.upper() + '{}    ')[:10])

        def on_target(k, t, color='b'):
            return res.replace('{target}', '{' + color + '}' + t + '{}')

        funcs = dict((x.__name__, x) for x in (on_levelname, on_status, on_target))

        for k in sorted(extra.keys()):
            res = funcs.get('on_' + k, replace)(k, str(extra[k]))

        res = res.replace('{bs}NONE{} | ', '')

        return res


def init_logger(log_level='DEBUG'):
    if 'pip' in y.sys.argv:
        return

    #y.logging.raiseExceptions = False
    old_factory = y.logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.asctime = y.datetime.datetime.fromtimestamp(int(y.time.time())).strftime('%H:%M:%S')
        record.name = record.name[:10]

        return record

    y.logging.setLogRecordFactory(record_factory)

    fmt = '{w}{m}%(asctime){} | {br}%(levelname){} | %(status) | {dw}%(msg){}{}'

    class Stream(object):
        def write(self, t):
            y.stderr.write(t)

        def flush(self):
            pass

    @y.lookup
    def lookup(name):
        return {'log_stream': Stream()}[name]

    screen_handler = y.logging.StreamHandler(stream=y.log_stream)
    screen_handler.setLevel(log_level)
    screen_handler.setFormatter(ColoredFormatter(fmt))

    y.logging.root.addHandler(screen_handler)
    y.logging.root.setLevel('DEBUG')

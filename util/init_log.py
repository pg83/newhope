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

        y.logging.Formatter.__init__(self, fmt, '%H:%M:%S')

    def format(self, record):
        style = self.styles.get(record.levelname[0])

        if style:
            record = y.deep_copy(record)
            record.msg = style + record.msg + '{}'

        return y.logging.Formatter.format(self, record)


def init_logger(log_level='INFO'):
    y.logging.raiseExceptions = False        
    old_factory = y.logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.thr = y.threading.get_ident() % 997
        record.name = record.name[:14]
        
        return record

    y.logging.setLogRecordFactory(record_factory)
    
    fmt = '{w}{g}%(thr)-3s{} | {b}%(asctime)s{} | {y}%(name)-12s{} | {bs}%(levelname).1s{} | %(message)s{}'

    class Stream(object):
        def __init__(self):
            self.s = y.stderr

        def write(self, t):
            self.s.write(t)

        def flush(self):
            pass
    
    screen_handler = y.logging.StreamHandler(stream=Stream())
    screen_handler.setLevel(log_level)
    screen_handler.setFormatter(ColoredFormatter(fmt))

    y.logging.root.addHandler(screen_handler)
    y.logging.root.setLevel('DEBUG')

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
        
        y.logging.Formatter.__init__(self, fmt, '%H:%M:%S')
        
    def format(self, record):
        res = self.fmt

        funcs = {
            'levelname': lambda x: x[:1].upper(),
            'msg': lambda x: (x + '    ')[:10]
        }

        if (target := record.__dict__.get('_target')) is not None:
            record.text = '{' + record.msg[2] + '}' + target + '{}'        
        
        for k, v in record.__dict__.items():
            res = res.replace('%(' + k + ')', funcs.get(k, lambda x: x)(str(v)))
        
        return res
    
    
def init_logger(log_level='INFO'):
    #y.logging.raiseExceptions = False        
    old_factory = y.logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)

        try:
            record.thr = str(y.current_coro().thread_id)

            if len(record.thr) == 1:
                record.thr = '0' + record.thr
        except Exception:
            record.thr = ''

        record.name = record.name[:10]
        record.msg = record.msg.strip()
        record.text = ''

        if len(record.msg) > 15:
            record.text = record.msg
            record.msg = '{bg}INFO{}'

        return record

    y.logging.setLogRecordFactory(record_factory)
    
    fmt = ' {w}{g}%(thr){} | {b}%(asctime)s{} | {br}%(levelname){} | %(msg) | %(text) {}'

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

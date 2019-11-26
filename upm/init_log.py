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

#y.logging.basicConfig(level='DEBUG')

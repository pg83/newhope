def my_eh(typ, val, tb):
    print typ, val, tb


def my_trace(frame, event, arg):
    print frame, event, arg
    
    return my_trace


def my_exept_hook(type, value, traceback):
    print type, value, traceback


@y.defer_constructor
def init():
    y.sys.excepthook = my_exept_hook


def iter_frames(frame=None):
    frame = frame or y.inspect.currentframe()

    while frame:
        yield frame
        frame = frame.f_back


@y.cached()
def text_from_file(path):
    return open(path).read().split('\n')


def mod_key(f):
    try:
        return len(f.f_globals['__ytext__'])
    except:
        pass

    return -1


@y.cached(key=mod_key)
def text_from_module(f):
    return f.f_globals['__ytext__'].split('\n')


def calc_text(f, fname):
    for i in (lambda: text_from_module(f), lambda: text_from_file(fname), lambda: []):
        try:
            return i()
        except:
            pass

    return []


def iter_tb_info(tb):
    while tb:
        f = tb.tb_frame
        co = f.f_code
        lineno = tb.tb_lineno - 1
        filename = co.co_filename
        name = co.co_name
        tb = tb.tb_next

        yield filename, lineno, name, f


def iter_frame_info(frames):
    for f in frames:
        fname = f.f_code.co_filename or f.f_globals['__file__']
        ln = f.f_lineno - 1
        func_name = f.f_code.co_name

        yield fname, ln, func_name, f


def iter_full_info(iter):
    for fname, ln, func_name, f in iter:
        lines = calc_text(f, fname)

        if not lines:
            lines = []

        if len(lines) < ln:
            text = []
        else:
            def iter():
                for i, l in enumerate(lines[ln - 1: ln + 2]):
                    if not l.strip():
                        continue

                    yield i + ln - 1, l.replace('\t', '    ')
                                        
            text = list(iter())
            
        yield (fname, ln, func_name, text)


def max_substr(lines):
    def calc(ss):
        for _, l in lines:
            if not l.startswith(ss):
                if ss:
                    return ss[:-1]
                else:
                    return ss

        return calc(ss + ' ')

    return calc('')


def format_trace(l):
    fname, ln, func_name, text = l

    yield ' {w}In {dg}' + fname + '{}, in {g}' + func_name + '{}:{}'

    if not text:
        return
        
    ss = max_substr(text)
        
    l1 = text[0][0]
    l2 = text[-1][0]

    max_len = len(str(l2))

    for lnn, t in text:
        yield (6 - len(str(lnn))) * ' ' + '{b}' + str(lnn) + ': ' + {ln: '{r}'}.get(lnn, '{w}') + t[len(ss):] + '{}{}'


def format_tbv(tb_line=''):
    value = y.sys.exc_info()[1]
    type = y.sys.exc_info()[0]
    
    if tb_line:
        tb_line = ', ' + tb_line

    return '{r}Exception of type {type}: {exc}{tb_line}:{}'.replace('{type}', str(type)).replace('{exc}', str(value)).replace('{tb_line}', tb_line)


def current_frame():
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        return sys.exc_info()[2].tb_frame.f_back


def format_tbx(tb_line=''):
    if not y.verbose:
        return format_tbv(tb_line=tb_line)

    tb = y.sys.exc_info()[2]

    def iter_exc():
        yield format_tbv(tb_line=tb_line)

        for x in iter_full_info(reversed(list(iter_tb_info(tb)))):
            for l in format_trace(x):
                yield l

    def iter_fr():
        yield '{g}Traceback: {line}{}'.replace('{line}', tb_line)
            
        for x in iter_full_info(list(iter_frame_info(iter_frames(current_frame())))):
            for l in format_trace(x):
                yield l

    return '\n'.join((tb and iter_exc or iter_fr)())


def print_tbx(*args, **kwargs):
    try:
        y.xxprint(format_tbx(*args, **kwargs))
    except Exception as e:
        y.traceback.print_exc(e)

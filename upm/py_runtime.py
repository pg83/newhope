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


def main_thread_dead():
    for t in y.threading.enumerate():
        if 'Main' in t.getName() and not t.isAlive():
            return True

            
def iter_all_frames(frame):
    return iter_all_frames_1(iter_frames(frame))


def iter_all_frames_1(frames):
    for f in frames:
        fname = f.f_code.co_filename or f.f_globals['__file__']
        ln = f.f_lineno - 1
        func_name = f.f_code.co_name

        def calc_text():
            for i in (lambda: f.f_globals['__ytext__'], lambda: open(fname).read(), lambda: ''):
                try:
                    return i()
                except Exception as e:
                    pass

        lines = calc_text().split('\n')

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


def format_trace_list(lst):
    for l in lst:
        fname, ln, func_name, text = l

        yield ' {w}In {dg}' + fname + '{}, in {g}' + func_name + '{}:{}'

        if not text:
            continue
        
        ss = max_substr(text)
        
        l1 = text[0][0]
        l2 = text[-1][0]

        max_len = len(str(l2))

        for lnn, t in text:
            yield (6 - len(str(l1))) * ' ' + '{b}' + str(lnn) + ': ' + {ln: '{r}'}.get(lnn, '{w}') + t[len(ss):] + '{}{}'


def format_tbv(tb_line=''):
    value = y.sys.exc_info()[1]
    type = y.sys.exc_info()[0]
    
    if tb_line:
        tb_line = ', ' + tb_line

    return '{r}Exception of type {type}: {exc}{tb_line}:{}'.replace('{type}', str(type)).replace('{exc}', str(value)).replace('{tb_line}', tb_line)


def format_tbx(tb_line=''):
    if not y.verbose:
        return format_tbv(tb_line=tb_line)

    tb = y.sys.exc_info()[2]

    if tb:
        tb_next = tb

        while tb_next.tb_next:
            tb_next = tb_next.tb_next

        frame = tb_next.tb_frame
    else:
        frame = y.sys._getframe()

    def iter():
        if tb:
            yield format_tbv(tb_line=tb_line)
        else:
            yield '{g}Traceback: {line}{}'.replace('{line}', tb_line)

        for l in format_trace_list(iter_all_frames(frame)):
            yield l

    return '\n'.join(iter())


def print_tbx(*args, **kwargs):
    y.xxprint(format_tbx(*args, **kwargs))

def monkey_patch():
    i = y.inspect
    getmodule = i.getmodule

    def my_get_module(name, _filename=None):
        if _filename:
            try:
                return __loader__._by_name[_filename[:-3].replace('/', '.')]
            except Exception:
                y.print_tbx()

        return getmodule(name, _filename=_filename)

    i.getmodule = my_get_module


monkey_patch()


def patch_ssl():
    ssl = y.ssl
    _create_default_context = ssl.create_default_context

    def create_default_context(*args, **kwargs):
        ctx = _create_default_context(*args, **kwargs)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        return ctx

    ssl.create_default_context = create_default_context
    ssl._create_default_https_context = create_default_context


patch_ssl()


def my_eh(typ, val, tb):
    print(typ, val, tb)


class PGProfiler(object):
    def __init__(self):
        self.d = []
        self.i = {}
        self.w = True
        self.t = y.threading.get_ident
        self.n = 0

    def my_trace(self, frame, event, arg):
        if not self.w:
            return

        self.n += 1

        lineno = frame.f_lineno
        path = frame.f_code.co_filename

        self.d.append((self.get_id(lineno), self.get_id(path), self.get_id(self.t())))

        return self.my_trace

    def heavy(self):
        lines = calc_text(frame, path)
        data ='\n'.join(lines[lineno-2:lineno + 1])

        try:
            arg = str(arg)
        except Exception as e:
            arg = e

        print(frame, event, arg, data)

    def get_id(self, k):
        i = self.i

        if k not in i:
            i[k] = len(i)

        return i[k]

    def dumps(self):
        try:
            self.w = False
            res = {'d': self.d, 'i': self.i}

            return y.encode_prof(res)
        finally:
            self.w = True

    def loads(self, v):
        res = y.decode_prof(v)

        self.i = res['i']
        self.d = res['d']

    def load_from_file(self, path):
        with open(path, 'r') as f:
            self.loads(f.buffer.read())

    def show_stats(self):
        def iter_keys():
            for l, f, t in self.d:
                yield (l, f)

        i = self.i
        i = dict((y, x) for x, y in i.items())
        d = y.collections.defaultdict(int)

        for x in iter_keys():
            d[x] += 1

        def iter_nk():
            for k, v in d.items():
                nk = str(i[k[1]]) + ':' + str(i[k[0]])

                yield nk, v

        res = sorted(list(iter_nk()), key=lambda x: -x[1])

        for i, j in res:
            print(i, j)

    def run(self, args):
        self.load_from_file(args[0])
        self.show_stats()


def my_exept_hook(type, value, traceback):
    print(type, value, traceback)


@y.defer_constructor
def init():
    @y.main_entry_point
    async def cli_dev_profile(args):
        PGProfiler().run(args)

    y.sys.excepthook = my_exept_hook

    if 'pg' in y.config.get('profile', ''):
        prof = PGProfiler()

        @y.run_at_exit
        def dump_data():
            try:
                with open('data.prof', 'w') as f:
                    data = prof.dumps()
                    f.buffer.write(data)
            except Exception as e:
                y.stderr.write(str(e) + '\n')

        y.globals.trace_function = prof.my_trace


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
    except Exception:
        pass

    return -1


@y.cached(key=mod_key)
def text_from_module(f):
    return f.f_globals['__ytext__'].split('\n')


def calc_text(f, fname):
    for i in (lambda: text_from_module(f), lambda: text_from_file(fname), lambda: []):
        try:
            return i()
        except Exception:
            pass


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

    yield ' {bw}In {bdg}' + fname + '{}, in {bg}' + func_name + '{}:{}'

    if not text:
        return

    ss = max_substr(text)

    l1 = text[0][0]
    l2 = text[-1][0]

    max_len = len(str(l2))

    for lnn, t in text:
        yield (6 - len(str(lnn))) * ' ' + '{bb}' + str(lnn) + ': ' + {ln: '{br}'}.get(lnn, '{bw}') + t[len(ss):] + '{}{}'


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
        return y.sys.exc_info()[2].tb_frame.f_back


def format_tbx(tb_line='', frame=None):
    if not y.verbose:
        return format_tbv(tb_line=tb_line)

    if frame:
        tb = None
    else:
        tb = y.sys.exc_info()[2]

    def iter_exc():
        yield format_tbv(tb_line=tb_line)

        for x in iter_full_info(reversed(list(iter_tb_info(tb)))):
            for l in format_trace(x):
                yield l

    def iter_fr():
        yield '{g}Traceback: {line}{}'.replace('{line}', tb_line)

        for x in iter_full_info(list(iter_frame_info(iter_frames(frame or current_frame())))):
            for l in format_trace(x):
                yield l

    return '\n'.join((tb and iter_exc or iter_fr)())


def print_tbx(*args, **kwargs):
    try:
        y.xxprint(format_tbx(*args, **kwargs))
    except Exception as e:
        y.traceback.print_exc(e)


def print_all_stacks():
    try:
        for k, v in list(y.sys._current_frames().items()):
            y.print_tbx(tb_line=str(k), frame=v)
    except Exception:
        y.print_tbx()


class AbortHandler(object):
    def __init__(self):
        self.sys = y.sys
        self.f1 = format_tbx
        self.f2 = y.traceback.format_exc
        self.cf = current_frame

    def handle(self):
        o = self.sys.stderr

        try:
            try:
                o.write(self.f1() + '\n')
                if y.verbose:
                    o.write(self.f1(frame=self.cf()) + '\n')
            except:
                o.write(self.f2())
        finally:
            o.flush()


y.globals.abort_handler = AbortHandler().handle

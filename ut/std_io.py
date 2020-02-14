stdio_lock = y.threading.Lock()


class StdIO(object):
    def __init__(self, s):
        self.s = s

    def write(self, t):
        with stdio_lock:
            self.s.buffer.write(t.encode('utf-8'))
            self.s.buffer.flush()

    def flush(self):
        with stdio_lock:
            self.s.flush()


@y.singleton
def is_debug():
    return 'debug' in y.config.get('color', '')


def safe_print(*args):
    y.sys.__stderr__.write((' '.join(str(x) for x in args)) + '\n')


class ColorStdIO(object):
    def __init__(self, s):
        self.q = y.queue.SimpleQueue()
        self.s = s
        self.p = ''
        self.f = {'strip_colors': not self.isatty()}

        self.t = y.threading.Thread(target=self.flush_periodicaly)
        self.t.daemon = True
        self.t.start()

        self.tt = y.threading.Thread(target=self.flush_q)
        self.tt.daemon = True
        self.tt.start()

    def flush_q(self):
        while True:
            try:
                self.q.get()()
            except Exception as e:
                try:
                    safe_print(e)
                finally:
                    y.os.abort()
    
    def flush_periodicaly(self):
        while True:
            try:
                y.time.sleep(0.3 * y.random.random())
                self.flush()
            except Exception as e:
                try:
                    safe_print(e)
                finally:
                    y.os.abort()

    def isatty(self):
        return self.s.isatty()

    def can_colorize(self, t):
        if len(t) > 100000:
            return False

        return not is_debug()

    def colorize_0(self, t):
        return y.process_color(t, '', self.f)

    def colorize(self, t):
        if not self.can_colorize(t):
            return t

        try:
            return self.colorize_0(t)
        except IndexError:
            pass

        def iter_lines():
            for l in t.split('\n'):
                try:
                    yield self.colorize_0(l)
                except IndexError:
                    yield l

        return '\n'.join(iter_lines())

    def get_part(self):
        try:
            return self.p
        finally:
            self.p = ''

    def write(self, t):
        if not t:
            return

        self.q.put(lambda: self.do_write(t))

    def do_write(self, t):
        with stdio_lock:
            if len(t) > 8192:
                self.flush_impl()
                self.write_part(t)
            else:
                self.p += t

                if len(self.p) > 8192:
                    self.flush_impl()

    def write_part(self, p):
        if p:
            try:
                self.s.buffer.write(self.colorize(p).encode('utf-8'))
            except AttributeError:
                self.s.buffer.write(p)

        self.s.buffer.flush()
        self.s.flush()

    def flush_impl(self):
        self.write_part(self.get_part())

    def flush(self):
        ev = y.threading.Event()

        def f():
            self.do_flush()
            ev.set()

        self.q.put(f)

        ev.wait()

    def do_flush(self):
        with stdio_lock:
            self.extra_flush()
            self.flush_impl()

    def slave(self):
        self.flush()

        return self.s

    def close(self):
        with stdio_lock:
            self.flush_impl()
            self.s.close()

    def fileno(self):
        return self.s.fileno()

    @property
    def encoding(self):
        return self.s.encoding


class ColorStdErr(ColorStdIO):
    def __init__(self):
        ColorStdIO.__init__(self, y.sys.stderr)

    def extra_flush(self):
        try:
            y.sys.stdout.flush_impl()
        except Exception:
            pass


class ColorStdOut(ColorStdIO):
    def __init__(self):
        ColorStdIO.__init__(self, y.sys.stdout)

    def extra_flush(self):
        try:
            y.sys.stderr.flush_impl()
        except Exception:
            pass


@y.defer_constructor
def init_stdio():
    init_stdio_0()


def init_stdio_0():
    y.sys.stdout = ColorStdOut()
    y.sys.stderr = ColorStdErr()


@y.contextlib.contextmanager
def without_color():
    try:
        y.sys.stdout = y.sys.__stdout__
        y.sys.stderr = y.sys.__stderr__

        yield
    finally:
        init_stdio()


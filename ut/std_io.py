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


class ColorStdIO(object):
    def __init__(self, s):
        self.s = s
        self.p = ''
        self.f = {'strip_colors': not self.isatty()}

    def isatty(self):
        return self.s.isatty()

    def can_colorize(self, t):
        if len(t) > 100000:
            return False

        return not is_debug()

    def colorize_0(self, t):
        #return t
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

        with stdio_lock:
            if len(t) > 4096:
                self.flush_impl()
                self.write_part(t)
            else:
                self.p += t

                if len(self.p) > 4096:
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
        with stdio_lock:
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


@y.defer_constructor
def init_stdio():
    y.sys.stdout = ColorStdIO(y.sys.stdout)
    y.sys.stderr = ColorStdIO(y.sys.stderr)

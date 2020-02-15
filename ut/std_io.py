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
                try:
                    t = t.decode('utf-8')
                except Exception:
                    pass

                self.p += t

                if len(self.p) > 8192:
                    self.flush_impl()

    def write_part(self, p):
        if not p:
            return

        self.clear_sl()

        try:
            self.s.buffer.write(self.colorize(p).encode('utf-8'))
        except AttributeError:
            self.s.buffer.write(p)

        self.draw_sl()
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


def stream_wrapped(stream):
    try:
        stream.can_colorize

        return True
    except AttributeError:
        pass

    return False


@y.singleton
def columns():
    try:
        return y.shutil.get_terminal_size().columns
    except OSError:
        return 100


class StatusBar(object):
    def __init__(self, columns):
        self._v = ''
        self._c = columns

    def cb(self, columns):
        self._c = columns

        return self._v

    def set_data(self, v):
        self._v = v

    def get_columns(self):
        return self._c


class FakeStatusBar(object):
    def set_data(self, v):
        pass

    def get_columns(self):
        return 1


@y.contextlib.contextmanager
def with_status_bar(stream):
    if stream_wrapped(stream):
        try:
            sb = StatusBar(columns())
    
            stream.set_sb_cb(sb.cb)
            yield sb
        finally:
            stream.set_sb_cb(None)
    else:
        yield FakeStatusBar()


class ColorStdErr(ColorStdIO):
    def __init__(self):
        self._cb = None
        ColorStdIO.__init__(self, y.sys.stderr)

    def extra_flush(self):
        try:
            y.sys.stdout.flush_impl()
        except Exception:
            pass

    def clear_sl(self):
        if self._cb:
            self.s.write("\r\033[K")

    def draw_sl(self):
        if self._cb:
            self.s.write('\r' + self._cb(columns()) + '\r')

    def set_sb_cb(self, cb):
        self.clear_sl()
        self._cb = cb


class ColorStdOut(ColorStdIO):
    def __init__(self):
        ColorStdIO.__init__(self, y.sys.stdout)

    def extra_flush(self):
        try:
            y.sys.stderr.flush_impl()
        except Exception:
            pass

    def clear_sl(self):
        pass

    def draw_sl(self):
        pass


@y.defer_constructor
def init_stdio():
    y.sys.stdout = ColorStdOut()
    y.sys.stderr = ColorStdErr()
    #pass

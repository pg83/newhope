import curses


class Term(object):
    def __init__(self, w):
        self.p = None
        self.root = True
        self.w = w
        self.c = [Window(self, self.w)]
        #self.c[0].w.nodelay(1)

        @y.lookup
        def lookup(name):
            return getattr(self.c[0].w, name)
        
        @y.read_callback('terminal', 'the one')
        def redraw(arg):
            cmd = arg['command']

            if cmd == 'redraw':
                self.redraw()
            elif cmd == 'status bar':
                status_bar()(arg)
                
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

            color_map = {
                'red': Color(curses.COLOR_RED, -1).set_bold(),
                'green': Color(curses.COLOR_GREEN, -1).set_bold(),
                'rst': Color(0),
                'yellow': Color(curses.COLOR_YELLOW, -1).set_bold(),
                'white': Color(curses.COLOR_WHITE, -1).set_bold(),
                'blue': Color(curses.COLOR_BLUE, -1).set_bold(),
                'darkgray': Color(curses.COLOR_WHITE, -1).set_dim(),
            }

            y.add_color_aliases(color_map)

            self.m = color_map
            
    def redraw(self):
        self.main_window().erase()
        
        for w in self.c:
            w.redraw()

        self.main_window().refresh()
            
    def update_screen(self):
        curses.doupdate()

    def main_window(self):
        return self.c[0]

    @property
    def painter(self):
        return self.main_window.o

    
@y.singleton
def terminal_channel():
    return y.write_channel('terminal', 'common')


@y.cached()
def get_color_num(fg, bg):
    try:
        get_color_num.__c
    except AttributeError:
        get_color_num.__c = 16

    get_color_num.__c += 1

    curses.init_pair(get_color_num.__c, fg, bg)            
    
    return get_color_num.__c


class Color(object):
    def __init__(self, fg=-1, bg=-1, num=-1):
        if num >= 0:
            self.attr = curses.color_pair(num)
        else:
            self.attr = curses.color_pair(get_color_num(fg, bg))

    def set_bold(self):
        self.attr |= curses.A_BOLD

        return self
        
    def set_standout(self):
        self.attr |= curses.A_STANDOUT

        return self

    def set_normal(self):
        self.attr |= curses.A_NORMAL

        return self

    def set_dim(self):
        self.attr |= curses.A_DIM

        return self
    
        
class Window(object):
    def __init__(self, p, w):
        self.p = p
        self.w = w
        self.root = False            
        self.c = []
        self.o = FakeWidget(self)
        self.w.notimeout(True)
        self.set_default_background()

    def set_background_color(self, ch, attrs):
        self.w.bkgd(ch, attrs.attr)

    def set_default_background(self):
        self.set_background_color(' ', Color(num=0))
        
    @property
    def rect(self):
        return y.wh_rect(self.real_width(), self.real_height())
    
    def real_width(self):
        return self.w.getmaxyx()[1]
    
    def real_height(self):
        return self.w.getmaxyx()[0]
        
    def redraw(self):
        self.draw_content()
        
        for w in self.c:
            w.redraw()
                                    
    def set_painter(self, o):
        self.o = o
            
    def draw_content(self):
        self.o.draw_content()
        
    def sub_window(self, r):
        res = Window(self, self.w.derwin(r.h, r.w, r.y, r.x))
        
        self.c.append(res)

        return res

    def border(self):
        self.w.border()
        
    def box(self):
        self.w.box()

    def refresh(self):
        self.w.refresh()
        
    def erase(self):
        self.w.erase()
        
    def find_term(self):
        t = self

        while not t.root:
            t = t.p

        assert t.p is None

        return t

    
class Widget(object):
    def __init__(self, w):
        self.w = w
        w.set_painter(self)

    @property
    def parent(self):
        return self.w.p.o
        
    @property
    def rect(self):
        return self.w.rect
    
    def set_background_color(self, ch, attrs):
        self.w.set_background_color(ch, attrs)

    def left_part(self, w):
        return self.sub_window(self.rect.set_width(w))

    def right_part(self, w):
        r = self.rect
        
        return self.sub_window(r.move_right(w).set_width(r.w - w))        

    def upper_part(self, h):
        return self.sub_window(self.rect.set_height(h))
    
    def lower_part(self, h):
        r = self.rect
        
        return self.sub_window(self.rect.move_down(h).set_height(r.h - h))
    
    def add_string(self, p, s, attr=None):
        if attr:
            self.w.w.addstr(p.y, p.x, s.encode('utf-8'), attr.attr)
        else:
            self.w.w.addstr(p.y, p.x, s.encode('utf-8'))

    def find_term(self):
        return self.w.find_term()

    def clear_window(self):
        self.w.w.clear()

    def sub_window(self, r):
        return self.w.sub_window(r)

    def border(self):
        self.w.border()
        
    def box(self):
        self.w.box()
    
    @property
    @y.cached_method
    def terminal(self):
        return self.find_term()

    def read_line(self):
        return self.w.w.getstr()

    def echo_on(self):
        self.w.w.echo()

    def echo_off(self):
        self.w.w.noecho()

        
class FakeWidget(Widget):
    def __init__(self, w):
        Widget.__init__(self, w)

    def on_resize(self):
        pass
        
    def draw_content(self):
        pass
    

class LayoutWidget(Widget):
    def __init__(self, la, w):
        Widget.__init__(self, w)
        self.la = la
        
    def draw_content(self):
        self.la.draw_content()

    def on_resize(self):
        self.la.on_resize()

        
class Layout(object):
    def __init__(self, w):
        self.p = LayoutWidget(self, w)

    @property
    def window(self):
        return self.p.w
    
    @property
    def painter(self):
        return self.p
        
    @property
    def rect(self):
        return self.painter.rect

    def sub_window(self, r):
        return self.painter.sub_window(r)
    
    
class BorderLayout(Layout):
    def __init__(self, w, ctor):
        Layout.__init__(self, w)
        self.ctor = ctor
        self.child = None
        self.on_resize()

    def draw_content(self):
        self.child.draw_content()
        self.painter.box()

    def on_resize(self):
        self.child = self.ctor(self.sub_window(self.rect.add_border()))

    
class Vertical2Layout(Layout):
    def __init__(self, w, w1, ctor1, w2, ctor2):
        Layout.__init__(self, w)
        self.w1 = w1
        self.ctor1 = ctor1
        self.child1 = None
        self.w2 = w2
        self.ctor2 = ctor2
        self.child2 = None
        self.on_resize()

    def on_resize(self):
        r = self.rect
        w = (self.w1 * r.w) / (self.w1 + self.w2)

        self.child1 = self.ctor1(self.sub_window(r.set_width(w)))
        self.child2 = self.ctor2(self.sub_window(r.set_width(r.w - w).move_right(w)))

    def draw_content(self):
        self.child1.draw_content()
        self.child2.draw_content()


class EndPoint(Layout):
    def __init__(self, w, ctor):
        Layout.__init__(self, w)
        self.widget = None
        self.ctor = ctor
        self.on_resize()
        
    def on_resize(self):
        self.widget = self.ctor(self.window)

    def draw_content(self):
        self.widget.draw_content()

    
class TextView(Widget):
    def __init__(self, w):
        Widget.__init__(self, w)
        self.text = ''
        self.on_resize()
        
    def on_resize(self):
        r = self.rect
        
        self.ss = r.h * r.w * 3
        
    @property
    def lines(self):
        return self.text.split('\n')
        
    def append(self, text):
        self.text = (self.text + text)[-self.ss:]

    def write(self, text):
        self.append(text)
        self.flush()
        
    def flush(self):
        self.terminal.redraw()
            
    def draw_content(self):
        if not self.text:
            return

        r = self.rect
        t = self.terminal
        lines = list(y.reshard_text(self.text, r.w))[-r.h:]

        for i, l in enumerate(lines):
            x = 0
            
            for p in l:
                self.add_string(y.Point(x, i), p['text'], attr=t.m[p['color']])
                x += len(p['text'])


class StatusLine(Widget):
    def __init__(self, w):
        Widget.__init__(self, w)
        self.text = ''
        self.set_background_color(' ', Color(curses.COLOR_WHITE, curses.COLOR_BLUE).set_dim().set_bold())
        
        @y.read_callback('build results', 'the one')
        @y.read_callback('status bar', 'the one')
        def on_text(arg):
            if 'message' in arg:
                txt = arg['message']

                if txt.strip():
                    self.text = (self.text.strip() + ', ' + txt)[1 - self.rect.w:]
                else:
                    self.text = (self.text + txt)[1 - self.rect.w:]

                self.text += ' ' * (self.rect.w - 1 - len(self.text))
                    
            if 'color' in arg:
                self.set_background_color(' ', arg['color'])
        
    def on_resize(self):
        pass

    def draw_content(self):
        self.add_string(y.Point(0, 0), self.text)


@y.singleton
def status_bar():
    return y.write_channel('status bar', 'common')


class LineLayoutBase(Layout):
    def __init__(self, w, ctor1, ctor2):
        Layout.__init__(self, w)
        self.child1 = None
        self.ctor1 = ctor1
        self.child2 = None
        self.ctor2 = ctor2
        
    def draw_content(self):
        self.child1.draw_content()
        self.child2.draw_content()

        
class StatusLineLayout(LineLayoutBase):
    def __init__(self, w, ctor):
        LineLayoutBase.__init__(self, w, ctor, StatusLine)
        self.on_resize()
        
    def on_resize(self):
        r = self.rect

        self.child1 = self.ctor1(self.sub_window(r.dec_height().move_down(1)))
        self.child2 = self.ctor2(self.sub_window(r.set_height(1)))

        
class FooterLineLayout(LineLayoutBase):
    def __init__(self, w, ctor):
        LineLayoutBase.__init__(self, w, ctor, StatusLine2)
        self.on_resize()
        
    def on_resize(self):
        r = self.rect

        self.child1 = self.ctor1(self.sub_window(r.dec_height()))
        self.child2 = self.ctor2(self.sub_window(r.set_height(1).move_down(r.h - 1)))

        
class StatusLine2(Widget):
    def __init__(self, w):
        Widget.__init__(self, w)
        self.set_background_color(' ', Color(curses.COLOR_WHITE, curses.COLOR_RED).set_dim().set_bold())
        self.values = {}
        
        @y.read_callback('status bar', 'another one')
        def on_message(arg):
            if 'key' in arg:
                self.values[arg['key']] = arg['value']
        
    def on_resize(self):
        pass

    def draw_content(self):
        text = ' | '.join('{k}: {v}'.format(k=k, v=v) for k, v in self.values.items())
        text += '-' * (self.rect.w - len(text) - 1)
        
        self.add_string(y.Point(0, 0), text)


def run_with_curses(func):
    def wrapper(*args, **kwargs):
        def run(stdscr):
            @y.read_callback('DEATH', 'restore mode')
            def finalize(arg):
                stdscr.keypad(0)

                curses.echo()
                curses.nocbreak()
                curses.endwin()
            
            curses.curs_set(2)
            
            return func(Term(stdscr), *args, **kwargs)

        f = lambda: curses.wrapper(run)

        try:
            return f()
        except Exception as e:
            if 'could not find terminfo database' in str(e):
                y.os.environ['TERMINFO'] = '/usr/share/terminfo'

                return f()
            else:
                raise e
            
    return wrapper


def run_curses_app(f):
    @y.run_with_curses
    def func(term):            
        return f(term)

    return func()

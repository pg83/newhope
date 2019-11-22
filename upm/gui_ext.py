import curses
from curses import textpad


C = {}

                                    
class BuildView(y.TextView):
    def __init__(self, w):
        y.TextView.__init__(self, w)

        @y.read_callback('build results', 'build view')
        def on_message(arg):
            if 'text' in arg:
                self.append(arg['text'])

    def draw_content(self):
        y.TextView.draw_content(self)
        self.w.w.vline(0, self.rect.w - 1, ord(' ') | y.Color(curses.COLOR_WHITE, curses.COLOR_MAGENTA).set_dim().attr, self.rect.h)

        
class YIC(y.code.InteractiveConsole, y.TextView):
    def __init__(self, w):
        y.code.InteractiveConsole.__init__(self)
        y.TextView.__init__(self, w)
        self.set_background_color(' ', y.Color(curses.COLOR_WHITE, curses.COLOR_BLACK).set_dim().set_bold())

        @y.read_callback('yic', 'common')
        def cb(arg):
            self.interact()
        
    def raw_input(self, prompt=None):
        return C['text_box_1'].edit()
            
    def write(self, data):
        y.TextView.write(self, '{w}' + data + '{}')


class TextBox(y.Widget):
    def __init__(self, w):
        y.Widget.__init__(self, w)
        C['text_box_1'] = self
        self.set_background_color(' ', y.Color(curses.COLOR_WHITE, curses.COLOR_BLUE).set_dim().set_bold())
        
    def on_resize(self):
        pass

    def draw_content(self):
        pass
    
    def edit(self):
        return textpad.Textbox(self.w.w, True).edit()

    
class YICLayout(y.LineLayoutBase):
    def __init__(self, w):
        y.LineLayoutBase.__init__(self, w, lambda w: y.EndPoint(w, YIC), lambda w: y.EndPoint(w, TextBox))
        self.on_resize()
        
    def on_resize(self):
        r = self.rect

        self.child1 = self.ctor1(self.sub_window(r.dec_height(1)))
        self.child2 = self.ctor2(self.sub_window(r.set_height(1).move_down(r.h - 1)))


def construct_make_gui():
    def ctor_build_view():
        return BuildView
      
    def ctor_yic_layout():
        return YICLayout
               
    def ctor_text_layout(func):
        return lambda w: y.EndPoint(w, func)

    def ctor_vertical():
        return lambda w: y.Vertical2Layout(w, 2, ctor_text_layout(ctor_build_view()), 1, ctor_yic_layout())

    def ctor_status_line():
        return lambda w: y.StatusLineLayout(w, ctor_vertical())
      
    def ctor_status_line2():
        return lambda w: y.FooterLineLayout(w, ctor_status_line())

    return ctor_status_line2()

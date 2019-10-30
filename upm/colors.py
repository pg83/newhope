@y.singleton
def color_map_func():
    RED = u'\u001b[31;1m'
    GREEN = u'\u001b[32;1m'
    RESET = u'\u001b[0m'
    YELLOW = u'\u001b[33;1m'
    WHITE = u'\u001b[37;1m'
    BLUE = u'\u001b[34;1m'


    COLOR_MAP = {
        'red': RED,
        'green': GREEN,
        'reset': RESET,
        'yellow': YELLOW,
        'white': WHITE,
        'blue': BLUE,
    }

    return COLOR_MAP


def get_color(n):
    return color_map_func()[n]


def colorize(text, color):
    return get_color(color) + text + get_color('reset')

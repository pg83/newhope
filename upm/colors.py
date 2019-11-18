@y.singleton
def color_map_func():
    RED = u'\u001b[31;1m'
    GREEN = u'\u001b[32;1m'
    RESET = u'\u001b[0m'
    YELLOW = u'\u001b[33;1m'
    WHITE = u'\u001b[37;1m'
    BLUE = u'\u001b[34;1m'
    DGRAY = u'\u001b[1;30m'

    COLOR_MAP = {
        'red': RED,
        'green': GREEN,
        'rst': RESET,
        'yellow': YELLOW,
        'white': WHITE,
        'blue': BLUE,
        'darkgray': DGRAY,
    }

    for k in list(COLOR_MAP.keys()):
        if k == 'rst':
            kk = ''
        elif k.startswith('dark'):
            kk = 'd' + k[4]
        else:
            kk = k[0]

        COLOR_MAP[kk] = COLOR_MAP[k]
        
    for k in list(COLOR_MAP.keys()):
        COLOR_MAP['{' + k + '}'] = COLOR_MAP[k]

    return COLOR_MAP


def get_color(n):
    return color_map_func()[n]


def colorize(text, color):
    return get_color(color) + text + get_color('')

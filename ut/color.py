ATTRIBUTES = dict(
    list(zip(
        [
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
        ], list(range(1, 9)))))

del ATTRIBUTES['']

ATTRIBUTES['light'] = ATTRIBUTES['bold']

HIGHLIGHTS = dict(
    list(zip([
        'on_grey',
        'on_red',
        'on_green',
        'on_yellow',
        'on_blue',
        'on_magenta',
        'on_cyan',
        'on_white'
    ], list(range(40, 48)))))

COLORS = dict(
    list(zip([
        'steel',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ], list(range(30, 38)))))

COLORS['reset'] = 0


def get_code(code):
    return "\033[{}m".format(code)


def get_color_0(color, on_color):
    res = ''

    if color is not None:
        res += get_code(COLORS[color])

    if on_color is not None:
        res += get_code(HIGHLIGHTS[on_color])

    return res


def color_key(color, on_color):
    return str(color) + '-' + str(on_color)


def iter_all_colors():
    for c in list(COLORS.keys()) + [None]:
        for o in list(HIGHLIGHTS.keys()) + [None]:
            yield color_key(c, o), get_color_0(c, o)


CC = dict(iter_all_colors())
            

def get_color_ext(color, on_color=None, attrs=[]):
    res = CC[color_key(color, on_color)]

    for attr in attrs:
        res += get_code(ATTRIBUTES[attr])

    return res


def iter_synonyms():
    for c in COLORS:
        if c == 'reset':
            continue
        
        yield c[0], c
        yield c, c


def iter_combo():
    attrs = [[], ['bold'], ['dark'], ['bold', 'dark']]

    for s, c in iter_synonyms():
        for a in attrs:
            if len(s) == 1:
                aa = [x[0] for x in a]
            else:
                aa = a

            name = ''.join(aa + [s])
            b = [x for x in a]
            
            yield name, c, b
            yield '{' + name + '}', c, b


def iter_full_table():
    for n, c, a in iter_combo():
        yield n, get_color_ext(c, on_color=None, attrs=a)

    for r in ('', 'rst', 'reset'):
        yield r, get_code(0)
        yield '{' + r + '}', get_code(0)
        

COLOR_TABLE = dict(iter_full_table())


def get_color(n):
    return COLOR_TABLE[n]


def colorize(text, color):
    return get_color(color) + text + get_color('')

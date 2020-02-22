import sys
import os


mod = sys.argv[1]
p = os.path.abspath(sys.executable)
pp = os.path.basename(p)
base = os.path.dirname(os.path.dirname(p))


def iter_dirs():
    yield base + '/lib/' + pp

    for x in sys.argv[2:]:
        yield os.path.abspath(x)


ppath = ''


for path in iter_dirs():
    print('start', path)
    os.system(sys.executable + ' ./find_modules.py ' + path + ' >> ./mods.py')
    ppath += ':' + path
    print('done', path)

os.system('PYTHONPATH=' + ppath + ' ' + sys.executable + ' ' + base + '/tools/freeze/freeze.py ' + mod + ' ./mods.py')

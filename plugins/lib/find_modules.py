import os
import sys


def find_modules():
    pr = sys.argv[1]
    assert os.path.isdir(pr)
    no = ['idlelib.idle', 'this', '_abcoll']

    for a, b, c in os.walk(pr):
        for d in b + c:
            if d.endswith('.py'):
                d = d[:-3]
                p = a + '/' + d
                p = p[len(pr) + 1:]
                m = p.replace('/', '.')

                if m in no:
                    continue

                if m.startswith('test.'):
                    continue

                cmd = '''
try:
    sys.stderr.write("{m}\n")
    import {m}
except:
    pass
'''
                print cmd.format(m=m).replace('-', '_')

find_modules()

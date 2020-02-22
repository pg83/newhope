import os
import sys


def skip(x):
    sys.stderr.write('skip ' + str(x) + '\n')


def find_modules():
    pr = sys.argv[1]
    assert os.path.isdir(pr)
    no = ['idlelib.idle', 'this', '_abcoll']

    for a, b, c in os.walk(pr):
        if not os.path.isfile(a + '/__init__.py'):
            continue

        for d in b + c:
            if d.endswith('.py'):
        
                d = d[:-3]
                p = a + '/' + d
                p = p[len(pr) + 1:]

                if '.' in p:
                    skip(p)

                    continue

                m = p.replace('/', '.')

                if m in no:
                    skip(m)

                    continue

                if m.startswith('test.'):
                    skip(m)

                    continue

                if '.test.' in m:
                    skip(m)

                    continue

                if '.tests.' in m:
                    skip(m)

                    continue
        
                if ' ' in m:
                    skip(m)

                    continue

                cmd = '''
try: 
    sys.stderr.write("{m}\\n") 
    import {m} 
except:
    pass

'''
                sys.stdout.write(cmd.format(m=m).replace('-', '_'))

find_modules()

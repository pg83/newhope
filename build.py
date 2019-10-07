import os
import json
import random
import subprocess


def prepare_pkg(fr, to):
    os.system('cd ' + fr + ' && tar -czf ' + to + ' .')

    return to


def build_package(pkg):
    where = '/workdir/' + str(int(random.random() * 1000000000))
    result = where + '_pkg'

    os.makedirs(where)
    os.makedirs(result)

    data = '\n'.join(pkg['build']) + '\n'

    if 'url' in pkg:
        data = data.replace('$(URL)', pkg['url']).replace('$(URL)', pkg['url'])

    p = subprocess.Popen(['/bin/bash', '-s'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, cwd=where)
    out, err = p.communicate(data)

    with open(where + '/text.json', 'w') as f:
        f.write(json.dumps({'out': out, 'err': err}))

    return prepare_pkg(where, result + '/package.tar.gz')

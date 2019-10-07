import os
import json
import random
import subprocess
import fcntl
import sys

from all import RES


def resolve_deps(ids):
    by_id = {}

    for a in RES:
        if 'id' in a:
            by_id[a['id']] = a

    return [by_id[x] for x in ids]


def get_pkg_link(id):
    p = '/repo/' + id
    m = '/managed/' + id

    if not os.path.isdir(m):
        with open(p, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if not os.path.isdir(m):
                    os.makedirs(m)
                    subprocess.check_output(['tar', '-zxf', p, '.'], cwd=m, shell=False)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return m


def prepare_pkg(fr, to):
    tmp = to + '_' + str(int(random.random() * 100000000))

    subprocess.check_output(['tar', '-czf', tmp, '.'], cwd=fr, shell=False)
    os.rename(tmp, to)

    return to


def build_package(pkg):
    print >>sys.stderr, '++++++++++++++++++++++', pkg

    deps = resolve_deps(pkg.get('deps', []))
    my_id = str(int(random.random() * 1000000000))
    where = '/workdir/' + my_id
    result = '/repo/' + pkg['id']

    os.makedirs(where)

    def iter_lines():
        for d in deps:
            try:
                get_pkg_link(d['id'])
            except Exception as e:
                build_package(d)

            yield 'cd ' + get_pkg_link(d['id'])

            for l in d.get('prepare', []):
                yield l

        yield 'cd ' + where

        for l in pkg['build']:
            yield l

    data = '\n'.join(iter_lines()) + '\n'

    if 'url' in pkg:
        data = data.replace('$(URL)', pkg['url']).replace('$(URL)', pkg['url'])

    print >>sys.stderr, '-----------------', data, '---------------------'

    p = subprocess.Popen(['/bin/bash', '-s'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, cwd=where)
    out, err = p.communicate(data)

    with open(where + '/text.json', 'w') as f:
        f.write(json.dumps({'out': out, 'err': err}))

    return prepare_pkg(where, result)

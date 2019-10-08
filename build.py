import os
import json
import random
import subprocess
import fcntl
import sys


def resolve_deps(ids):
    from all import RES

    by_id = {}

    for a in RES:
        if 'id' in a:
            by_id[a['id']] = a

    return [by_id[x] for x in ids]


def cons_to_name(c):
    return '-'.join([c['host'], c['libc'], c['target']])


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


def to_visible_name(pkg):
    return ((pkg['id'][:8] + '-' + cons_to_name(pkg['constraint']) + '-' + os.path.basename(pkg['url'])).replace('_', '-').replace('.', '-')).replace('--', '-')


def build_package(pkg):
    deps = resolve_deps(pkg.get('deps', []))
    my_id = str(int(random.random() * 1000000000))
    uniq_id = to_visible_name(pkg)
    where_install = '/private/' + uniq_id
    where_build = '/workdir/' + my_id
    result = '/repo/' + uniq_id

    os.makedirs(where_install)
    os.makedirs(where_build)

    def iter_lines():
        for d in deps:
            uniq_id = to_visible_name(d)

            try:
                get_pkg_link(uniq_id)
            except Exception as e:
                build_package(d)

            yield 'cd ' + get_pkg_link(uniq_id)

            for l in d.get('prepare', []):
                yield l

        yield 'cd ' + where_build

        for l in pkg['build']:
            yield l

    data = '\n'.join(iter_lines()) + '\n'

    for i in range(1, 3):
        data = data.replace('$(URL)', pkg.get('url', '')).replace('$(INSTALL_DIR)', where_install).replace('$(BUILD_DIR)', where_build)

    print >>sys.stderr, '-----------------', data, '---------------------'

    p = subprocess.Popen(['/bin/bash', '-s'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, cwd=where_install)
    out, err = p.communicate(data)

    if p.returncode:
        try:
            with open('config.log', 'r') as f:
                print >>sys.stderr, f.read()
        except Exception:
            pass

        raise Exception('shit happen: %s, %s' % (out, err))

    with open(where_install + '/text.json', 'w') as f:
        f.write(json.dumps({'out': out, 'err': err}))

    return prepare_pkg(where_install, result)

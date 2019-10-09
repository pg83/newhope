import os
import json
import random
import subprocess
import fcntl
import sys
import shutil


def get_pkg_link(p):
    m = '/managed/' + p[6:]

    if not os.path.isdir(m):
        with open(p, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if not os.path.isdir(m):
                    os.makedirs(m)
                    subprocess.check_output(['tar', '-Jxf', p, '.'], cwd=m, shell=False)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return m


def prepare_pkg(fr, to):
    print >>sys.stderr, 'will package', fr, 'to package', to

    tmp = to + '_' + str(int(random.random() * 100000000))

    subprocess.check_output(['tar', '-cJf', tmp, '.'], cwd=fr, shell=False)
    os.rename(tmp, to)
    shutil.rmtree(fr)

    print >>sys.stderr, 'done packaging'

    return to


def build_package(pkg, id_func):
    my_id = str(int(random.random() * 10000))
    uniq_id = id_func(pkg)
    where_install = '/private/' + uniq_id
    where_build = '/workdir/' + my_id + '-' + uniq_id
    result = '/repo/' + uniq_id

    print >>sys.stderr, 'will build', result, 'from', pkg['from']

    if os.path.isfile(result):
        print >>sys.stderr, result, 'already done'

        return result

    os.makedirs(where_install)
    os.makedirs(where_build)

    def iter_lines():
        yield 'env'

        for d in pkg.get('deps', []):
            yield 'cd ' + get_pkg_link(build_package(d, id_func))

            for l in d.get('prepare', []):
                yield l

        yield 'cd ' + where_build

        for l in pkg['build']:
            yield l

    data = '\n'.join(iter_lines()) + '\n'

    for i in range(1, 3):
        data = data.replace('$(URL)', pkg.get('url', '')).replace('$(INSTALL_DIR)', where_install).replace('$(BUILD_DIR)', where_build)

    print >>sys.stderr, '----------------- willl run\n', data, '\ndone ---------------------'

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

    try:
        return prepare_pkg(where_install, result)
    finally:
        print >>sys.stderr, result, 'done'

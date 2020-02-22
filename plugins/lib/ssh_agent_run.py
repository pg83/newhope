#!/bin/upm python

import os
import shutil
import time


run_sh = '''#!/bin/sh
. /etc/profile || true

exec su {user} -c "exec ssh-agent -D > {home}/.ssh_agent"
'''


prefix = '/etc/runit'


def iter_current():
    try:
        for x in os.listdir(prefix):
            if x.startswith('k_'):
                yield x
    except OSError:
        pass


def iter_users():
    yield 'root', '/root'

    for x in os.listdir('/home'):
        if '+' not in x:
            yield x, '/home/' + x


users = dict(iter_users())


folders_new = frozenset('k_' + x for x in users.keys())
folders_old = frozenset(iter_current())


to_add = folders_new - folders_old
to_rem = folders_old - folders_new


for f in to_rem:
    shutil.rmtree(prefix + '/' + f)


for f in to_add:
    user = f[2:]
    path = prefix + '/' + f

    os.mkdir(path)

    with open(path + '/run', 'w') as ff:
        ff.write(run_sh.replace('{user}', user).replace('{home}', users[user]))

    os.system('chmod +x ' + path + '/run')


time.sleep(5)

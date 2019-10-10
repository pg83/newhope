import os
import json
import random
import subprocess
import fcntl
import sys
import shutil
import gen_id
import hashlib

from user import add_tool_deps


def fix_fetch_url(src):
    fetch_url = 'wget -O - $(URL) | tar --strip-components 1 -x#f - ;'

    if '.bz2' in src:
        return fetch_url.replace('#', 'j')
    
    if '.xz' in src:
        return fetch_url.replace('#', 'J')
    
    return fetch_url.replace('#', 'z')


def install_dir(pkg):
    return '/managed/' + gen_id.to_visible_name(pkg)


def bin_dir(pkg):
    return install_dir(pkg) + '/bin'


def lib_dir(pkg):
    return install_dir(pkg) + '/lib'


def inc_dir(pkg):
    return install_dir(pkg) + '/include'


def subst_values(data, pkg, deps):
    src = pkg['url']

    subst = {
        '$(FETCH_URL)': fix_fetch_url(src),
        '$(URL)': src,
    }

    for x in deps:
        node = x['node']
        name = node['name']
            
        subst['$(' + name.upper() + '_BIN_DIR)'] = bin_dir(node)
        subst['$(' + name.upper() + '_LIB_DIR)'] = lib_dir(node)
        subst['$(' + name.upper() + '_INC_DIR)'] = inc_dir(node)
        
    for k, v in subst.items():
        data = data.replace(k, v)

    return data


def calc_mode(name):
    if '-gz-' in name[:15]:
        return 'z'

    if '-xz-' in name[:15]:
        return 'J'

    raise Exception('shit happen')

        
def get_pkg_link(p):
    n = p[6:]
    m = '/managed/' + n

    if not os.path.isdir(m):
        with open(p, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if not os.path.isdir(m):
                    os.makedirs(m)
                    subprocess.check_output(['tar', '-x' + calc_mode(n) + 'f', p, '.'], cwd=m, shell=False)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return m


def prepare_pkg_shell(fr, to):
    tmp = to + '_' + str(int(random.random() * 1000000))

    return """
        # will package %s to package %s
        cd %s && tar -czf %s .
        move %s %s
        rm rf %s
        # done
    """ % (fr, to, fr, tmp, tmp, to, fr)


def prepare_pkg(fr, to):
    print >>sys.stderr, 'will package', fr, 'to package', to

    tmp = to + '_' + str(int(random.random() * 1000000))
    subprocess.check_output(['tar', '-c' + calc_mode(to[6:]) + 'f', tmp, '.'], cwd=fr, shell=False)
    os.rename(tmp, to)
    shutil.rmtree(fr)

    print >>sys.stderr, 'done packaging'

    return to


def struct_dump(p):
    return hashlib.md5(json.dumps(p, sort_keys=True, indent=4)).hexdigest()

V = set()

def build_makefile_impl(node):
    if struct_dump(node) in V:
        return 

    V.add(struct_dump(node))
    # print >>sys.stderr, json.dumps(node, indent=4, sort_keys=True)

    for dep in node['deps']:
        for y in build_makefile_impl(dep):
            yield y

    def gen_one(tools):
        for t in tools:
            for y in build_makefile_impl(t):
                yield y

        work_dir = '/workdir/' + str(int(10000000000 * random.random()))
        vis_name = '/repo/' + gen_id.to_visible_name(node['node'])

        def iter_portion():
            yield 'if not %s' % vis_name
            
            for l in node['node']['build']:
                yield l

            for l in prepare_pkg_shell('$(BUILD_DIR)', '$(INSTALL_DIR)').split('\n'):
                yield l.strip()

            yield 'endif\n'

            for l in node['node'].get('prepare', []):
                yield l.strip()

        for l in subst_values('\n'.join(iter_portion()) + '\n', node['node'], node['deps'] + tools).replace('$(INSTALL_DIR)', vis_name).replace('$(BUILD_DIR)', work_dir).split('\n'):
            yield l.strip()

    prev = ''
    tools = []

    while True:
        data = '\n'.join(gen_one(tools))
        next_tools = add_tool_deps(node['node'], data)

        if len(next_tools) == len(tools):
            break

        prev = data
        tools = next_tools

    for l in data.split('\n'):
        yield l.strip()
        
def build_makefile(node):
    return '\n'.join(build_makefile_impl(node))

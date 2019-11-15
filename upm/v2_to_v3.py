import base64
import itertools
import hashlib


def mn(x):
    return '$MD' + x[3:]


def iter_deps(root):
    rn = root['trash']['restore_node']

    for d in root['deps']:
        yield rn(d)


def subst_values(data, root):
    root_node = root['node']

    def iter1():
        pkg_root = gen_pkg_path(root)[4:]
        
        yield ('$(INSTALL_DIR)', '$PD/' + pkg_root)
        yield ('$(BUILD_DIR)', '$WD/' + hashlib.md5(pkg_root).hexdigest())
        yield ('$(PKG_FILE)', '$RD/' + pkg_root)

    return y.subst_kv_base(data, iter1())
                               

def mgr_pkg(x):
    return '$MD' + x[3:]


def mgr_pkg_mark(x):
    return mgr_pkg(x) + '/done'


def gen_pkg_path(v):
    return '$RD/' + y.to_visible_name(v)


def uniq_deps(d):
    return y.uniq_list_2(d, gen_pkg_path)


def rmmkcd(q, suffix=''):
    return 'rm -rf {q} || true; mkdir -p {q}{s}; cd {q}{s}'.format(q=q, s=suffix)


def prepare_prepare(data, target):
    return '\n'.join(data).replace('$(CUR_DIR)', '$MD/' + target[4:])


def print_one_node(root):
    rn = root['trash']['restore_node']
    root_node = root['node']
    target = gen_pkg_path(root)
    nodes = list(uniq_deps([rn(x) for x in root['deps']]))
    naked = root_node.get('naked', False)
    inputs = [y.build_scripts_path()] + [mgr_pkg_mark(x[0]) for x in nodes] + root_node.get('inputs', [])

    int_node = {
        'output': target,
        'inputs': list(inputs),
    }

    def iter_part1():
        if not naked:
            yield '. init $@'

        for x in root_node.get('build', []):
            yield x

        prepare = prepare_prepare(root_node.get('prepare', []), target)
        meta = y.meta_to_build(root_node.get('meta', {}), None, target)
        data = '\n'.join([prepare, meta])

        if data:
            data = data.replace('{pkgroot}', mn(target)) + '\n'

            yield 'source write_build_file "' + base64.b64encode(data) + '"'
        else:
            yield 'touch "$IDIR/build"'
                
        if not naked:
            yield 'source footer'

    int_node['build'] = subst_values('\n'.join(iter_part1()), root).split('\n')

    return int_node

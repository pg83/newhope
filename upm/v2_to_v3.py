import base64
import itertools
import hashlib


def mn(x):
    return '$MD' + x[3:]


def install_dir(pkg):
    return '$PD/' + y.to_visible_name(pkg)


def bin_dir(pkg):
    return install_dir(pkg) + '/bin'


def lib_dir(pkg):
    return install_dir(pkg) + '/lib'


def inc_dir(pkg):
    return install_dir(pkg) + '/include'


@y.cached(key=y.calc_noid)
def get_subst_values(x):
    n = x['node']['name'].upper().replace('-', '_')

    return [
        ('$(MNGR_' + n + '_DIR)', mn(install_dir(x))),
        ('$(MNGR_' + n + '_BIN_DIR)', mn(bin_dir(x))),
        ('$(MNGR_' + n + '_LIB_DIR)', mn(lib_dir(x))),
        ('$(MNGR_' + n + '_INC_DIR)', mn(inc_dir(x))),
    ]


def iter_deps(root):
    rn = root['trash']['restore_node']

    for d in root['deps']:
        yield rn(d)


def get_subst_values_3(root):
    for x in itertools.chain([root], iter_deps(root)):
        for y in get_subst_values(x):
            yield y


def subst_values(data, root):
    root_node = root['node']

    def iter1():
        pkg_root = gen_pkg_path(root)[4:]
        
        yield ('$(INSTALL_DIR)', '$PD/' + pkg_root)
        yield ('$(BUILD_DIR)', '$WD/' + hashlib.md5(pkg_root).hexdigest())
        yield ('$(PKG_FILE)', '$RD/' + pkg_root)

    return y.subst_kv_base(data, iter1(), get_subst_values_3(root))


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


@y.singleton
def common_prepare_repl():
    return [
        ('$(ADD_PATH)', 'export PATH="$(CUR_DIR)/bin:$PATH"'),
        ('$(ADD_CFLAGS)', 'export CFLAGS="-I$(CUR_DIR)/include $CFLAGS"'),
        ('$(ADD_LDFLAGS)', 'export LDFLAGS="-L$(CUR_DIR)/lib $LDFLAGS"'),
        ('$(ADD_PKG_CONFIG)', 'export PKG_CONFIG_PATH="$(CUR_DIR)/lib/pkgconfig:$PKG_CONFIG_PATH"'),
        ('$(ADD_LIBS)', 'export LIBS="$LIBS "'),
    ]


def prepare_prepare(data, target):
    return y.subst_kv_base('\n'.join(data), common_prepare_repl()).replace('$(CUR_DIR)', '$MD/' + target[4:])


def to_bash(x):
    return '$' +  x[2] + 'D' + x[4:]


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
        
        if prepare:
            yield 'echo "' + base64.b64encode(prepare) + '" | source base64_decode > "$IDIR/build"'
        else:
            yield 'touch "$IDIR/build"'

        if not naked:
            yield 'source footer {codec}'.format(codec=root_node['codec'])

    int_node['build'] = subst_values('\n'.join(iter_part1()), root).split('\n')

    return int_node

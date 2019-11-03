import itertools


def mn(x):
    return '$(M)' + x[4:]


def install_dir(pkg):
    return '$(P)/' + y.to_visible_name(pkg)


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


@y.cached(key=y.calc_noid)
def get_subst_values_3(root):
    def do():
        for x in itertools.chain([root], iter_deps(root)):
            for y in get_subst_values(x):
                yield y

    return list(do())


def subst_values(data, root):
    root_node = root['node']

    def iter1():
        pkg_root = gen_pkg_path(root)

        yield ('$(INSTALL_DIR)', '$(P)/' + pkg_root[5:])
        yield ('$(BUILD_DIR)', '$(W)/' + y.calc_noid(root)[2:])
        yield ('$(PKG_FILE)', pkg_root)

    def iter2():
        if 'url' in root_node or 'pkg_full_name' in root_node:
            path = '$(MNGR_FETCH_URL_DIR)/' + root_node['pkg_full_name']
            mode = y.calc_mode(root_node['pkg_full_name'])
            tmpl = 'source untar_{ext} "{path}" {level}'

            yield ('$(FETCH_URL)', tmpl.format(ext=mode, path=path, level=1))
            yield ('$(FETCH_URL_2)', tmpl.format(ext=mode, path=path, level=2))
            yield ('$(FETCH_URL_FILE)', 'ln $(MNGR_FETCH_URL_DIR)/$(URL_BASE) $(URL_BASE)')

            if 'url' in root_node:
                yield ('$(URL)', root_node['url'])

            yield ('$(URL_BASE)', root_node['pkg_full_name'])

    return y.subst_kv_base(data, iter1(), iter2(), get_subst_values_3(root))


def mgr_pkg(x):
    return '$(M)' + x[4:]


def mgr_pkg_mark(x):
    return mgr_pkg(x) + '/done'


def gen_pkg_path(v):
    return '$(R)/' + y.to_visible_name(v)


def uniq_deps(d):
    return y.uniq_list_2(d, gen_pkg_path)


def rmmkcd(q, suffix=''):
    return 'rm -rf {q} || true; mkdir -p {q}{s}; cd {q}{s}'.format(q=q, s=suffix)


def print_one_node(root, reducer):
    rn = root['trash']['restore_node']
    root_node = root['node']
    target = gen_pkg_path(root)
    nodes = list(uniq_deps([rn(x) for x in root['deps']]))
    naked = root_node.get('naked', False)
    inputs = [mgr_pkg_mark(x[0]) for x in nodes] + root_node.get('inputs', []) + [y.build_scripts_path()]

    int_node = {
        'output': target,
        'inputs': list(reducer(inputs)),
    }

    def iter_part1():
        if not naked:
            yield 'set_path {scripts}'.format(scripts=y.build_scripts_dir())
            yield '. runtime; source prepare_env "$(INSTALL_DIR)" "$(BUILD_DIR)" "$(PKG_FILE)"; cat << EOF > run.sh; exec $YSHELL ./run.sh;'
            yield '. runtime; source header'

        for pkg_path, x in nodes:
            pdir = '$(M)' + pkg_path[4:]

            for p in x['node'].get('prepare', []):
                yield p.replace('$(ADD_PATH)', 'add_path $(CUR_DIR)/bin').replace('$(CUR_DIR)', pdir)

        if not naked:
            yield 'cd $BD'

        for x in root_node.get('build', []):
            yield x

        if not naked:
            yield 'source footer {codec}'.format(codec=root_node['codec'])

    def iter_part2():
        def get_path(x):
            return x[8:].strip()

        lines1 = []
        paths = []
        lines2 = []

        for l in iter_part1():
            ll = l.strip()

            if ll.startswith('set_path') or ll.startswith('add_path'):
                paths.append(ll)
            else:
                if paths:
                    lines2.append(l)
                else:
                    lines1.append(l)

        for l in lines1:
            yield l

        yield 'export PATH=' + ':'.join([get_path(x) for x in y.uniq_list_0(reversed(paths))])

        for l in lines2:
            yield l

    int_node['build'] = subst_values('\n'.join(iter_part2()), root).split('\n')

    return int_node

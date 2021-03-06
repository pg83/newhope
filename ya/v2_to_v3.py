import base64
import itertools
import hashlib


def mn(x):
    return '$MD' + x[3:]


def iter_deps(root):
    for d in root['deps']:
        yield y.restore_node(d)


def mgr_pkg(x):
    return '$MD' + x[3:]


def mgr_pkg_mark(x):
    return mgr_pkg(x) + '/build'


def gen_pkg_path(v):
    return '$RD/' + y.to_visible_name(v)


def uniq_deps(d):
    return y.uniq_list_2(d, gen_pkg_path)


def prepare_prepare(data, target):
    return '\n'.join(data).replace('$(CUR_DIR)', '$MD/' + target[4:])


def print_one_node(root):
    root_node = root['node']
    extra = root_node.get('extra_cmd', [])
    target = gen_pkg_path(root)
    nodes = list(uniq_deps([y.restore_node(x) for x in root['deps']]))
    naked = root_node.get('naked', False)
    inputs = [y.build_scripts_path()] + [mgr_pkg_mark(x[0]) for x in nodes] + [x['output'] for x in extra]

    int_node = {
        'output': target,
        'inputs': list(inputs),
    }

    def iter_part1():
        if not naked:
            yield '. "$2" && source init $@'

        prepare = prepare_prepare(root_node.get('prepare', []), target)
        meta = y.meta_to_build(root_node.get('meta', {}))
        data = '\n'.join([meta, prepare]).strip()
        data = data.replace('{pkgroot}', mn(target)) + '\n'
        data = base64.b64encode(data.encode('utf-8'))

        yield from root_node.get('build', [])

        if naked:
            yield 'source write_build_file "' + data.decode('utf-8') + '"'
        else:
            yield 'source fini "' + data.decode('utf-8') + '"'

    int_node['build'] = list(iter_part1())

    return [int_node] + extra

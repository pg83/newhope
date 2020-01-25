copy_many = """
copy_many() {
    shift
    shift
    for i in $@; do
        (cd $(dirname $i) && $YTAR -v -cf - .) | (cd $IDIR/ && $YTAR -v -Uxf -)
    done
}
copy_many $@
"""


def join_funcs(args_calcer, fixer=lambda x: x, ex_code=''):
    def wrapper():
        def iter_lines_0():
            for d in (copy_many, ex_code):
                yield from d.strip().split('\n')

        def iter_lines_1():
            for l in iter_lines_0():
                if l:
                    yield l

        res = {
            'node': {
                'build': list(iter_lines_1()),
            },
            'deps': args_calcer(),
        }

        infos = [y.restore_node_node(d) for d in res['deps']]

        res['node']['meta'] = y.join_metas([i.get('meta', {}) for i in infos], merge=['kind', 'flags', 'provides'])

        return y.fix_v2(fixer(res))

    return y.singleton(lambda: y.gen_func(wrapper))

copy_many = """
copy_many() {
    shift
    shift
    for i in $@
    do
        cp -R $(dirname $i)/* $IDIR/
    done
}

copy_many $@
"""

def join_funcs(args_calcer, fixer=lambda x: x):
    def wrapper(info):
        res = {
            'node': {
                'build': list(copy_many.strip().split('\n')),
                'constraint': info['info'],
            },
            'deps': args_calcer(info),
        }

        return fixer(res)

    return y.cached(f=lambda info: y.gen_func(wrapper, info))


def big_join_func(base, gen, args):
    descr = {
        'gen': gen,
        'base': base,
        'kind': ['join'],
    }

    descr['code'] = join_funcs(args, lambda x: y.fix_pkg_name(x, descr))

    return descr

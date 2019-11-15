def join_funcs(my_name, my_num, args, channel=y.write_channel('new functions', 'join')):
    @y.cached()
    def wrapper(info):
        deps = [arg(info) for arg in args]
        nodes = [y.restore_node_node(x) for x in deps]

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

        res = {
            'node': {
                'build': list(copy_many.strip().split('\n')),
                'name': my_name,
                'constraint': info['info'],
            },
            'deps': deps,
        }

        return res

    ygf = y.gen_func
    f1 = lambda info: ygf(wrapper, info)
    f1.__name__ = 'f1_' + my_name + str(my_num)
    f2 = y.cached()(f1)
    f2.__name__ = my_name + str(my_num)

    channel({'kind': ['join'], 'func': f2, 'args': [x.__name__ for x in args]})

    return [f2]

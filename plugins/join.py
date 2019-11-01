def join_funcs(my_name, my_num, args):
    if not args:
        return args

    if len(args) == 1:
        return args

    def wrapper(info):
        deps = [arg(info) for arg in args]
        nodes = [y.restore_node(x) for x in deps]

        res = {
            'node': {
                'build': ['cp -R $(MNGR_{N}_DIR)/* $IDIR/'.format(N=x['node']()['name'].upper()) for x in nodes],
                'name': my_name + str(my_num),
                'version': str(my_num),
                'prepare': sum([x['node']().get('prepare', []) for f in nodes], []),
            },
            'deps': deps,
        }

        return res

    wrapper.__name__ = my_name + str(my_num)

    return [y.options()(wrapper)]

def choose_best_build_env(envs):
    return sorted(envs, key=lambda x: -len(x))[0]


def choose_platform(what, p):
    descr = p.get(what, 'current')

    if descr == 'current':
        return y.current_host_platform()


def solve_build(cs_id):
    cs = y.all_common_sets()[cs_id]
    
    for p in cs['platforms']:
        solve_build_for_platform(cs, p)


def solve_build_for_platform(cs, p):
    conf = {
        'constraint': {'host': choose_platform('host', p), 'target': choose_platform('target', p)},
    }
    
    host_to_host = y.deep_copy({'host': conf['constraint']['host'], 'target': conf['constraint']['host']})
    host_to_target = y.deep_copy(conf['constraint'])

    conf['host_cc'] = y.iterate_best_compilers(host_to_host)[0]
    conf['target_cc'] = y.iterate_best_compilers(host_to_target)[0]
        
    arg = {
        'back_channel': y.uniq_write_channel('common solver'),
        'conf': conf,
    }    

    envs = []

    y.read_callback_from_channel(arg['back_channel'])(envs.append)
    y.build_env_channel()(arg)

    conf['build_env'] = choose_best_build_env(envs)

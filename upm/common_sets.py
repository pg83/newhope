@y.defer_constructor
@y.singleton
def all_common_sets():
    res = {}

    @y.gd_callback('COMMON_SET')
    def add_set(arg):
        res[arg['id']] = arg

    return res


@y.singleton
def cs_channel():
    return y.GEN_DATA_LOOP.write_channel('COMMON_SET', 'common channel')


@y.defer_constructor
def init_set_pg():
    cs_channel()({
       'id': 'pg-essentials',
       'packages': ['mc'],
       'platforms': [
            {'target': 'current', 'host': 'current', 'flags': []},
       ],
    })

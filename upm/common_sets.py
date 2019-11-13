@y.defer_constructor
@y.singleton
def all_common_sets():
    res = {}

    @y.read_callback('common set', 'collector')
    def add_set(arg):
        res[arg['id']] = arg

    return res


cs_channel = y.write_channel('common set', 'common channel')


@y.defer_constructor
def init_set_pg():
    cs_channel({
       'id': 'pg-essentials',
       'packages': ['mc'],
       'platforms': [
            {'target': 'current', 'host': 'current', 'flags': []},
       ],
    })

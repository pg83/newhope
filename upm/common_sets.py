@y.defer_constructor
@y.singleton
def all_common_sets():
    res = {}


    return res


@y.defer_constructor
def init_set_pg():
    {
       'id': 'pg-essentials',
       'packages': ['mc'],
       'platforms': [
            {'target': 'current', 'host': 'current', 'flags': []},
       ],
    }

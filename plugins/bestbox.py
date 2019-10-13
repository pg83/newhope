@helper
def bestbox1(info):
    cc = info['info']
    gen_func = info['generator_func']
    toybox1 = gen_func('toybox1')
    busybox1 = gen_func('busybox1')

    return {
        'node': {
            'kind': 'system',
            'name': 'bestbox1',
            'constraint': cc,
        },
        'deps': [toybox1(**cc), busybox1(**cc)],
    }

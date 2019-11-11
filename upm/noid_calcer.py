def calc_noid_base(v):
    if 'noid' in v:
        #assert v['noid'] == calc_noid_base_really(v)
        return v['noid']

    return calc_noid_base_really(v)


def calc_noid_base_really(v):
    return 'i:' + y.key_struct_ptr([v['node'], v['deps']])[2:]


def calc_noid(v):
    return 'i:' + y.key_struct_ptr([calc_noid_base(v), v['trash']['extra']])[2:]


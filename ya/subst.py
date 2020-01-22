def subst_kv_base(data, *iterables):
    for k, v in y.itertools.chain(*iterables):
        data = data.replace(k, v)

    return data

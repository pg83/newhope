def subst_kv_base(data, *iterables):
    for k, v in y.itertools.chain(*iterables):
        if '$(' not in data:
            break;

        data = data.replace(k, v)

    return data

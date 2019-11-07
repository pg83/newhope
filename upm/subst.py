import itertools


def subst_kv_base(data, *iterables):
    for k, v in itertools.chain(*iterables):
        data = data.replace(k, v)

        if 0:
            if '$(' not in data:
                break;

    return data

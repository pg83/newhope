import json


from upm_iface import y


def iter_all_tools():
    return list(y.iter_system_tools()) + list(y.iter_musl_cc_tools()) + list(y.iter_ndk_tools())


def group_by_cc():
    f = group_by_cc

    try:
        f.__res
    except AttributeError:
        f.__res = {}

        for x in iter_all_tools():
            k = y.small_repr_cons(x['node']['constraint'])

            if k in res:
                f.__res[k].append(x)
            else:
                f.__res[k] = [x]

    return f.__res


def find_toolchain_by_cc(cc):
    return group_by_cc()[y.small_repr_cons(cc)]

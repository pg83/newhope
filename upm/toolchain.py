import json


from upm_iface import y


@y.singleton
def iter_all_tools():
    return list(y.iter_system_tools()) + list(y.iter_musl_cc_tools()) + list(y.iter_ndk_tools())


@y.singleton
def group_by_cc():
    try:
        group_by_cc.__res
    except AttributeError:
        def calc():
            res = group_by_cc.__res

            for x in iter_all_tools():
                k = y.small_repr_cons(x['node']['constraint'])

                if k in res:
                    res[k].append(x)
                else:
                    res[k] = [x]

            return res

        group_by_cc.__res = calc()

    return res


def find_toolchain_by_cc(cc):
    return group_by_cc()[y.small_repr_cons(cc)]

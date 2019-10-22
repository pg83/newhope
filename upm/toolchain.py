import json


from upm_iface import y
from upm_cc import iter_system_tools, iter_musl_cc_tools, small_repr_cons
from upm_ndk import iter_ndk_tools
from upm_ft import struct_dump_bytes


def iter_all_tools():
    return list(iter_system_tools()) + list(iter_musl_cc_tools()) + list(iter_ndk_tools())


@y.singleton
def group_by_cc():
    res = {}

    for x in iter_all_tools():
        k = small_repr_cons(x['node']['constraint'])

        if k in res:
            res[k].append(x)
        else:
            res[k] = [x]

    return res


def find_toolchain_by_cc(cc):
    return group_by_cc()[small_repr_cons(cc)]

import json
import hashlib

from bb import res as bb_res
from cc import res as cc_res
from libc import res as lc_res


RES = bb_res + cc_res + lc_res


def complete(x):
    cc = x['constraint']

    return ('host' in cc) and ('target' in cc) and ('libc' in cc)


def find_compiler(host='x86_64', target='aarch64', libc='musl', **kwargs):
    def iter_libc():
        for x in RES:
            if x['kind'] == 'libc-source':
                yield x

    def iter_compilers():
        for x in RES:
            if x['kind'] == 'c/c++ compiler':
                if complete(x):
                    yield x
                else:
                    for lc in iter_libc():
                        x = json.loads(json.dumps(x))

                        x['constraint']['libc'] = lc['name']

                        assert complete(x)

                        yield {
                            'constraint': x['constraint'],
                            'compound': {
                                'compiler': x,
                                'libc': lc,
                            },
                        }


    for x in iter_compilers():
        cc = x['constraint']

        if cc['host'] == host:
            if cc['target'] == target:
                if cc['libc'] == libc:
                    yield x

import json
import hashlib

from bb import res as bb_res
from cc import res as cc_res
from libc import res as lc_res
from gen_id import gen_id

RES = bb_res + cc_res + lc_res


def find_compiler(host='x86_64', target='aarch64', libc='musl'):
    def iter_libc():
        for x in RES:
            if x['kind'] == 'libc-source':
                yield x

    def iter_compilers():
        for x in RES:
            if x['kind'] == 'c/c++ compiler':
                if 'id' in x:
                    yield x
                else:
                    for lc in iter_libc():
                        x = json.loads(json.dumps(x))

                        x['constraint']['libc'] = lc['name']

                        yield {
                            'id': gen_id([x, lc]),
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

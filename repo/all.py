import json
import hashlib

from bb import res as bb_res
from cc import res as cc_res
from libc import res as lc_res

res = bb_res + cc_res + lc_res

print json.dumps(res, indent=4, sort_keys=True)

def find_compiler(host='x86_64', target='aarch64', libc='musl'):
    def iter_libc():
        for x in res:
            if x['kind'] == 'libc':
                yield x

    def iter_compilers():
        for x in res:
            if x['kind'] == 'c/c++ compiler':
                if 'id' in x:
                    yield x
                else:
                    for lc in iter_libc():
                        x = json.loads(json.dumps(x))

                        x['constraint']['libc'] = lc['name']

                        yield {
                            'id': hashlib.md5(json.dumps([x, lc], sort_keys=True, indent=4)).hexdigest(),
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


for x in find_compiler(host='x86_64', target='aarch64', libc='uclibc'):
    print x

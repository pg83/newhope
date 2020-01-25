import json
import sys


patch = """
        import json

        if os.environ.get('DUMP'):
            print(json.dumps([x.__dict__ for x in extensions], sort_keys=True, indent=4))
            sys.stdout.flush()
            os._exit(0)
"""

class Skip(Exception):
    pass


def build_descr(el):
    pre = ''
    after = ''

    name = el['name']

    if name.startswith('_test'):
        pre = '*disabled*\n'
        after = '\n*static*\n'

    if 'audio' in name:
        raise Skip()

    bad = [
        'xxlimited',
        '_decimal',
        '_elementtree',
        'pyexpat',
    ]

    if name in bad:
        pre = '#'

    sources = []
    cflags = []
    ldflags = []

    cflags.extend(el['extra_compile_args'])
    ldflags.extend(el['extra_link_args'])

    def fix_inc(i):
        if '/Modules' in i:
            return '-I$(srcdir)' + i[i.find('/Modules'):]

        return i

    def flt_wl(l):
        for x in l:
            if 'h_path' in x:
                pass
            else:
                yield x

    def flt_wl_1(l):
        return list(flt_wl(l))

    for x in el['include_dirs']:
        if '/usr' in x:
            raise Skip()

        cflags.append(fix_inc(('-I' + x).replace('-IMo', '-I$(srcdir)/Mo')))

    for x in el['libraries']:
        cflags.append('-l' + x)

    for x in el['sources']:
        sources.append(x)

    cflags_d = []

    for x in el['define_macros']:
        if x[1]:
            cflags_d.append('#define ' + str(x[0]) + ' ' + str(x[1]))
        else:
            cflags_d.append('#define ' + str(x[0]))

    def flt_lib(ll):
        for l in ll:
            if l == '-lm':
                pass
            else:
                if l == '-l:libmpdec.so.2':
                    yield '-lmpdec'
                else:
                    yield l

    if cflags_d:
        add = '\n'.join(cflags_d) + '\n\n'

        for s in sources:
            s = 'Modules/' + s

            with open(s, 'r') as f:
                data = add + f.read()

            with open(s, 'w') as f:
                f.write(data)
    
    return pre + ' '.join([name] + flt_wl_1(sources) + flt_wl_1(list(flt_lib(cflags))) + flt_wl_1(list(flt_lib(ldflags)))) + after


def apply_patch(path, p, line):
    with open(path) as f:
        data = f.read()

    def iter():
        for ll in data.split('\n'):
            if line in ll:
                yield p

            yield ll

    data = '\n'.join(iter())

    with open(path, 'w') as f:
        f.write(data)


def main():
    if sys.argv[1] == 'patch':
        return apply_patch(sys.argv[2], patch, '# move ctypes to the end')

    with open(sys.argv[1]) as f:
        data = f.read()
        data = json.loads(data[data.find('['):])

    print('*static*')

    for el in data:
        try:
            print(build_descr(el))
        except Skip:
            print('skip', str(el), file=sys.stderr)


if __name__ == '__main__':
    main()

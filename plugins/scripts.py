@y.cached()
def gen_check_log(data):
    p1, p2, p3 = tuple(data.split('EOF'))

    args = p1.strip()
    tmpl = p2.strip()
    cmd = p3.strip()

    def iter_params():
        yield 'fgrep'
        yield args

        for p in tmpl.split('\n'):
            yield '-e'
            yield "'" + p.strip() + "'"

    grep = ' '.join(iter_params())
    cmd = cmd.format(grep=grep)

    return cmd


def scripts_data(no_last=False):
    def iter():
        for x in y.globals.file_data:
            k = x['name']

            if not k.startswith('sc/'):
                continue

            k = k[3:]
            v = x['data']
            func = {'check_log': gen_check_log}.get(k, lambda x: x)

            yield {'kind': 'file', 'path': 'bin/' + k, 'data': func(v)}

        for k, v in y.gen_extra_scripts():
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': v}

        if no_last:
            pass
        else:
            data = 'export PATH="{path}:$PATH" && . runtime'.format(path=build_scripts_dir())

            yield {'kind': 'file', 'path': 'build', 'data': data}

    return list(sorted(iter(), key=lambda x: x['path']))


def unpack_sh(no_last=False):
    for x in scripts_data(no_last=no_last):
        yield 'echo "{data}" | (base64 -D -i - -o - || base64 -d) > {fname}'.format(data=y.base64.b64encode(x['data'].encode('utf-8')).decode('utf-8'), fname=y.os.path.basename(x['path']))


@y.singleton
def build_scripts_dir():
    data = list(unpack_sh(no_last=True))
    ver = y.struct_dump_bytes(data)[:5]

    return '$MD/noarch-build-scripts-run-' + ver


def build_scripts_path():
    return build_scripts_dir() + '/build'


@y.singleton
def build_scripts_run():
    output = build_scripts_path()

    res = {
        'inputs': [],
        'output': build_scripts_path(),
        'build': [
            'export PATH=$PATH:/bin:/usr/bin:/usr/local/bin; rm -rf "{output}" || true && mkdir -p "{output}" && cd "{output}"'.format(output=build_scripts_dir()),
        ] + list(unpack_sh()),
    }

    res['hash'] = y.struct_dump_bytes(res)

    return res

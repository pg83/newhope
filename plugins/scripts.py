import sys
import base64
import hashlib


def scripts_data():
    def iter():
        for k, v in sys.builtin_modules['mod'].items():
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': v}

        for k, v in y.gen_extra_scripts():
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': v}

        for k, v in sorted(y.color_map_func().items()):
            yield {'kind': 'file', 'path': 'bin/' + {'reset': 'rsc'}.get(k, k), 'data': 'echo -n "' + v.encode('utf-8') + '"'}

    return list(sorted(iter(), key=lambda x: x['path']))


def unpack_sh():
    for x in scripts_data():
        yield 'echo "{data}" | (base64 -D -i - -o - || base64 -d) > {fname}'.format(data=base64.b64encode(x['data']), fname=os.path.basename(x['path']))


@y.singleton
def build_scripts_dir():
    data = list(unpack_sh())
    ver = y.struct_dump_bytes(data)[:5]

    return '$(M)/noarch-build-scripts-run-' + ver


def build_scripts_path():
    return build_scripts_dir() + '/done'


@y.singleton
def build_scripts_run():
    output = build_scripts_path()

    res = {
        'inputs': [],
        'output': build_scripts_path(),
        'build': [
            'rm -rf "{output}" || true && mkdir -p "{output}" && cd "{output}"'.format(output=build_scripts_dir()),
        ] + list(unpack_sh()) + [
            'echo 7 > done',
        ]
    }

    res['hash'] = y.struct_dump_bytes(res)

    return res

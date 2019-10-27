import sys


@y.singleton
def build_scripts():
    return build_scripts_run({})


@y.options(repacks=None, naked=True)
def build_scripts_run(info):
    def iter():
        for k, v in sys.builtin_modules['mod'].items():
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': v}

    data = list(sorted(iter(), key=lambda x: x['path']))

    return to_v2({
        'code': """
               set_path /bin:/usr/bin
               rm -rf $(INSTALL_DIR) || true; mkdir -p $(INSTALL_DIR); cd $(INSTALL_DIR)
               mkdir bin
""" + '\n'.join('$(APPLY_EXTRA_PLAN_' + str(i) + ')' for i in range(0, len(data))) + """
               export IDIR="$(INSTALL_DIR)"; export BDIR="$(BUILD_DIR)"; export PATH=`pwd`/bin:$PATH
               source build.lib
""",
        'version': y.struct_dump_bytes(data)[:4],
        'extra': data,
        'prepare': '$(ADD_PATH)',
        'codec': 'gz',
        'name': 'build_scripts_run',
    }, info)

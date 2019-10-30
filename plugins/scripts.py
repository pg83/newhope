import sys


@y.singleton
def build_scripts():
    return build_scripts_run({})


@y.options(repacks=None, naked=True)
def build_scripts_run(info):
    def iter():
        for k, v in sys.builtin_modules['mod'].items():
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': v}

        for k, v in y.gen_extra_scripts():
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': v}

        for k, v in sorted(y.color_map_func().items()):
            yield {'kind': 'file', 'path': 'bin/' + k, 'data': 'echo -n "' + v.encode('utf-8') + '"'}

    data = list(sorted(iter(), key=lambda x: x['path']))

    return y.to_v2({
        'code': """
               set -ex -o pipefail
               set_path /bin:/usr/bin:/usr/local/bin
               rm -rf $(INSTALL_DIR) || true; mkdir -p $(INSTALL_DIR); cd $(INSTALL_DIR)
               mkdir bin
""" + '\n'.join('$(APPLY_EXTRA_PLAN_' + str(i) + ')' for i in range(0, len(data))) + """
               export PATH=`pwd`/bin:$PATH;
               source set_env
               export IDIR="$(INSTALL_DIR)"; export BDIR="$(BUILD_DIR)"; export PKGF="$(PKG_FILE)"
               source prepare_tr_pkg "$IDIR" "$PKGF" && rm -rf $IDIR $BDIR
""",
        'version': y.struct_dump_bytes(data)[:4],
        'extra': data,
        'prepare': '$(ADD_PATH)',
        'codec': 'tr',
        'name': 'build_scripts_run',
    }, info)

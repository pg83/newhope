def toybox0(info, deps, codec):
    if y.xp('/info/info/host/os') == 'darwin':
        return system00(info)

    name = 'toybox-' + info['info']['host']['arch']
    ver = '0.8.1'

    return to_v2({
        'code': 'mkdir -p $(INSTALL_DIR)/bin && cd $(INSTALL_DIR)/bin && $(FETCH_URL_FILE) && cp %s toybox && chmod +x toybox' % name,
        'src': 'http://www.landley.net/toybox/downloads/binaries/' + ver + '/' + name,
        'version': ver,
        'deps': deps,
        'codec': codec,
    }, info)


@y.options(repacks=None)
def toybox2_run(info):
    return toybox0(info, [], 'gz')


@y.options(repacks=None)
def toybox1_run(info):
    return toybox0(info, [bestbox2_run(info), tar2_run(info), xz2_run(info)], 'xz')


@y.options(repacks=None)
def toybox_run(info):
    return toybox0(info, [bestbox1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)], 'xz')

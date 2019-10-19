def toybox0(info, deps, codec):
    if xp('/info/info/host/os') == 'darwin':
        return system00(info)

    name = 'toybox-' + info['info']['host']['arch']
    ver = '0.8.1'

    return {
        'code': 'mkdir -p $(INSTALL_DIR)/bin && cd $(INSTALL_DIR)/bin && $(FETCH_URL_FILE) && cp %s toybox && chmod +x toybox' % name,
        'src': 'http://www.landley.net/toybox/downloads/binaries/' + ver + '/' + name,
        'version': ver,
        'deps': deps,
        'codec': codec,
    }


@helper
def toybox2(info):
    return toybox0(info, [system0(info)], 'gz')


@helper
def toybox1(info):
    return toybox0(info, [bestbox2(info), tar2(info), xz2(info)], 'xz')


@helper
def toybox(info):
    return toybox0(info, [bestbox1(info), tar1(info), xz1(info), curl1(info)], 'xz')

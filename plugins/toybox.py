@helper
def toybox1(info):
    name = 'toybox-' + info['info']['host']
    ver = '0.8.1'

    return {
        'code': 'mkdir -p $(INSTALL_DIR)/bin && cd $(INSTALL_DIR)/bin && $(FETCH_URL_FILE) && cp %s toybox && chmod +x toybox' % name,
        'src': 'http://www.landley.net/toybox/downloads/binaries/' + ver + '/' + name,
        'version': ver,
    }

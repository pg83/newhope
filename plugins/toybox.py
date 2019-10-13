@helper
def toybox1(info):
    name = 'toybox-' + info['info']['host']

    return {
        'code': 'mkdir $(INSTALL_DIR)/original && cd $(INSTALL_DIR)/original && $(FETCH_URL_FILE) && cp %s toybox && chmod +x toybox' % name,
        'src': 'http://www.landley.net/toybox/downloads/binaries/latest/' + name,
    }

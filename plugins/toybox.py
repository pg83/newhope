@helper
def toybox_binary(info):
    name = 'toybox-' + info['info']['host']

    return {
        'code': """
            mkdir $(INSTALL_DIR)/bin
            cd $(INSTALL_DIR)/bin
            $(FETCH_URL_FILE)
            cp %s toybox
            chmod +x toybox
        """ % name,
        'src': 'http://www.landley.net/toybox/downloads/binaries/latest/' + name,
    }

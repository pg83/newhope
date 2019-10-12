@helper
def mbedtls1():
    return {
        'code': """
            rm -rf /usr/local
            $(FETCH_URL) make programs lib && make install
            cd /usr/local && mv * $(INSTALL_DIR)/

            #pragma cc
        """,
        'src': 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz',
    }

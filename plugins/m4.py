@helper
def m4(info):
    c = info['compilers']

    if len(c) == 1:
        cross = ''
    else:
        cross = '--host=' + c[1]['node']['prefix'][1][:-1] + ' --target=' + c[0]['node']['prefix'][1][:-1]

    return {
        'code': """
            #pragma cc

            ./configure %s --prefix=$(INSTALL_DIR) && make && make install
        """ % cross,
        'src': 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz',
    }

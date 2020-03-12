@y.package
def runit0():
    return {
        'code': '''
            source fetch "http://smarden.org/runit/runit-2.1.2.tar.gz" 0
            cd admin/runit-2.1.2/src

            source fake_binutils

            unlink gcc
            echo '#!/bin/sh' > gcc
            echo "$CC $CFLAGS \"\$@\"" >> gcc

            $YMAKE -j $NTHRS

            mkdir $IDIR/bin
            cp -pR $(cat TARGETS | grep local | grep -v runsvctrl | grep -v runsvstat | grep -v svwaitdown | grep -v svwaitup | sed -e s/\.local//) $IDIR/bin/
        ''',
        'meta': {
            'depends': ['make', 'c'],
        }
    }

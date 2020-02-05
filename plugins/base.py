@y.package
def base0():
    return {
        'code': """
            cd $IDIR
            mkdir -p etc etc/alt/ etc/upm/sources etc/upm/db pkg pkg/cache srv bin 
            touch pkg/profile
            echo '. ../pkg/profile' > etc/profile
            ln -s etc/alt/sh bin/sh 
            echo 'http://index.samokhvalov.xyz/index' > etc/upm/sources/00.index 
        """,
        'meta': {
            'kind': [],
        },
    }

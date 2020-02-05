@y.package
def base0():
    return {
        'code': """
            cd $IDIR
            mkdir -p etc etc/alt/ etc/upm/sources etc/upm/db pkg pkg/cache srv 
            echo 'http://index.samokhvalov.xyz/index' > etc/upm/sources/00.index 
        """,
        'meta': {
            'kind': [],
        },
    }

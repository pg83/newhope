@y.package
def base0():
    return {
        'code': """
            cd $IDIR
            mkdir /etc /etc/alt/ /etc/upm/ /pkg /srv 
            echo 'http://index.samokhvalov.xyz/index' > /etc/upm/00.index 
        """,
        'meta': {
            'kind': [],
        },
    }

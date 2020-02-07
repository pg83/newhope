@y.package
def upm0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release > $IDIR/bin/upm && chmod +x $IDIR/bin/upm  
        """,
        'version': 'd1842198cd96897ccaeb457d62dec5cf918d4356',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3'],
        },
    }

@y.package
def upm0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release > $IDIR/bin/upm && chmod +x $IDIR/bin/upm  
        """,
        'version': '6daf914b866ba7e8efb56a95507d08bef7e7e4a2',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3'],
        },
    }

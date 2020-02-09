@y.package
def upm0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release > $IDIR/bin/upm && chmod +x $IDIR/bin/upm  
        """,
        'version': '27c238c481f052b21726c6a6b9ee676ce540ca84',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3'],
        },
    }

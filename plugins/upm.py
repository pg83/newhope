@y.package
def upm0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release > $IDIR/bin/upm && chmod +x $IDIR/bin/upm  
        """,
        'version': '3dc11b867a938cd8e081201fd7c619fbd469c7fe',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3'],
        },
    }

@y.ygenerator()
def asciidoc0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/project/asciidoc/asciidoc/{version}/asciidoc-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '8.6.9',
        'meta': {
            'kind': ['box', 'tool'],
        }
    }

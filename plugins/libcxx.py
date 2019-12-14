@y.ygenerator()
def libcxx0():
    return {
        'code': """
             source fetch "http://releases.llvm.org/{version}/libcxx-{version}.src.tar.xz" 0
             mv libcxx* xxx
             mv xxx/* ./
             $(APPLY_EXTRA_PLAN_0)
             source mk.sh
        """,
        'version': '9.0.0',
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_libcxx.sh']['data']},
        ],
        'meta': {
            'kind': ['library'],
            'depends': ['libcxxrt'],
            'provides': [
                {'lib': 'c++'},
                {'env': 'CXXFLAGS', 'value': '"-isystem{pkgroot}/include $CXXFLAGS"'},
            ],
        },
    }

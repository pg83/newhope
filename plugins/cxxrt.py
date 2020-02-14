@y.package
def libcxxrt0():
    return {
        'code': """
             #pragma cc
             source fetch "https://github.com/pathscale/libcxxrt/archive/master.zip" 0
             mv libcxxrt* xxx
             mv xxx/* ./
             $(APPLY_EXTRA_PLAN_0)
             source mk.sh
        """,
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_libcxxrt.sh']['data']},
        ],
        'meta': {
            'kind': ['library'],
            'depends': ['libunwind', 'c'],
            'provides': [
                {'lib': 'cxxrt'},
                {'env': 'LIBCXXRT_INC', 'value': '"{pkgroot}/include"'},
            ],
        },
    }

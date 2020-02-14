@y.package
def libcxx0():
    if '{os}' == 'linux':
        sh = 'data/mk_libcxx.sh'
    else:
        sh = 'data/mk_libcxx_darwin.sh'

    return {
        'code': """
             #pragma cc
             source fetch "http://releases.llvm.org/{version}/libcxx-{version}.src.tar.xz" 0
             mv libcxx* xxx
             mv xxx/* ./
             $(APPLY_EXTRA_PLAN_0)
             source mk.sh
        """,
        'version': '9.0.0',
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name[sh]['data']},
        ],
        'meta': {
            'kind': ['library'],
            'depends': ['libcxxrt', 'c'],
            'provides': [
                {'env': 'CPPFLAGS', 'value': '"-w -I/Library/Developer/CommandLineTools/SDKs/MacOSX10.15.sdk -I{pkgroot}/include"'},
                {'lib': 'c++'},
            ],
        },
    }

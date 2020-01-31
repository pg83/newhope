@y.package
def libunwind0():
    return {
        'code': """
             #pragma cc
             source fetch "http://releases.llvm.org/{version}/libunwind-{version}.src.tar.xz" 0
             mv libunwind* xxx
             mv xxx/* ./
             $(APPLY_EXTRA_PLAN_0)
             cat src/AddressSpace.hpp | grep -v 'pragma comment' > tmp && mv tmp src/AddressSpace.hpp
             source mk.sh
        """,
        'version': '9.0.0',
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_libunwind.sh']['data']},
        ],
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'unwind'},
            ],
        },
    }

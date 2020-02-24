@y.package
def libunwind0():
    return {
        'code': """
             #pragma cc
             source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/libunwind-{version}.src.tar.xz" 0
             mv libunwind* xxx
             mv xxx/* ./
             $(F_0)
             cat src/AddressSpace.hpp | grep -v 'pragma comment' > tmp && mv tmp src/AddressSpace.hpp
             $YSHELL mk.sh
        """,
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_libunwind.sh']['data']},
        ],
        'meta': {
            'kind': ['library'],
            'depends': ['c'],
            'provides': [
                {'lib': 'unwind'},
            ],
        },
    }

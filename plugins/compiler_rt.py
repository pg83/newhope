@y.ygenerator()
def compiler_rt0():
    return {
        'code': """
             #pragma cc
             source fetch "http://releases.llvm.org/9.0.0/compiler-rt-9.0.0.src.tar.xz" 1
        """,
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'crt'},
            ],
        },
    }

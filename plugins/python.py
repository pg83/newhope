python_setup_local = """
# Fred Drake's interface to the Python parser
parser parsermodule.c

zlib zlibmodule.c

array arraymodule.c    # array objects
cmath cmathmodule.c _math.c # -lm # complex math library functions
math mathmodule.c _math.c # -lm # math library functions, e.g. sin()
_struct _struct.c    # binary structure packing/unpacking
time timemodule.c # -lm # time operations and variables
operator operator.c    # operator.add() and similar goodies
#_testcapi _testcapimodule.c    # Python C API test module
_random _randommodule.c    # Random number generator
_collections _collectionsmodule.c # Container types
_heapq _heapqmodule.c        # Heapq type
itertools itertoolsmodule.c    # Functions creating iterators for efficient looping
strop stropmodule.c        # String manipulations
_functools _functoolsmodule.c    # Tools for working with functions and callable objects
_elementtree -I$(srcdir)/Modules/expat -DHAVE_EXPAT_CONFIG_H -DUSE_PYEXPAT_CAPI _elementtree.c    # elementtree accelerator
#_pickle _pickle.c    # pickle accelerator
datetime datetimemodule.c    # date/time type
_bisect _bisectmodule.c    # Bisection algorithms

unicodedata unicodedata.c    # static Unicode character database

# access to ISO C locale support
_locale _localemodule.c  # -lintl

# Standard I/O baseline
_io -I$(srcdir)/Modules/_io _io/bufferedio.c _io/bytesio.c _io/fileio.c _io/iobase.c _io/_iomodule.c _io/stringio.c _io/textio.c


# Modules with some UNIX dependencies -- on by default:
# (If you have a really backward UNIX, select and socket may not be
# supported...)

fcntl fcntlmodule.c    # fcntl(2) and ioctl(2)
#spwd spwdmodule.c        # spwd(3)
grp grpmodule.c        # grp(3)
select selectmodule.c    # select(2); not on ancient System V

# Memory-mapped files (also works on Win32).
mmap mmapmodule.c

# Helper module for various ascii-encoders
binascii binascii.c

# Fred Drake's interface to the Python parser
parser parsermodule.c

cStringIO cStringIO.c
cPickle cPickle.c

_curses _cursesmodule.c
_curses_panel _curses_panel.c

_md5 md5module.c md5.c
_sha shamodule.c
_sha256 sha256module.c
_sha512 sha512module.c

readline readline.c
"""

find_modules = """
import os
import sys


def find_modules():
    pr = sys.argv[1]
    assert os.path.isdir(pr)
    no = ['idlelib.idle', 'this', '_abcoll']

    for a, b, c in os.walk(pr):
        for d in b + c:
            if d.endswith('.py'):
                d = d[:-3]
                p = a + '/' + d
                p = p[len(pr) + 1:]
                m = p.replace('/', '.')

                if m in no:
                    continue

                if m.startswith('test.'):
                    continue

                cmd = \"""
try:
    print >>sys.stderr, "{m}"
    import {m}
except:
    pass
\"""
                print cmd.format(m=m).replace('-', '_')

find_modules()
"""


def python_base(kind):
    return {
        'code': """
            source fetch "https://www.python.org/ftp/python/{version}/Python-{version}.tgz" 1
            $(APPLY_EXTRA_PLAN_0)
            $YSHELL ./configure $COFLAGS --prefix=$IDIR/python --enable-static --disable-shared --with-signal-module --with-system-ffi || exit1
            ##echo "#define HAVE_PTH 1" >> pyconfig.h
            ##echo "#undef HAVE_PTHREAD_H" >> pyconfig.h             
            $YMAKE -j2 || exit 1
            $YMAKE install

            env
            PYTHON=$IDIR/python/bin/python2.7
            mkdir good && cd good 
            $(APPLY_EXTRA_PLAN_1)
            $PYTHON ./find_modules.py $IDIR/python/lib/python2.7 > all_modules.py
            cat ./all_modules.py
            $PYTHON ../Tools/freeze/freeze.py ./all_modules.py
            echo '#define Py_FrozenMain Py_Main' >> frozen
            cat frozen.c >> frozen
            cat ../Modules/main.c >> frozen
            mv frozen frozen.c
            $YMAKE OPT="$CFLAGS" -j4
            mv all_modules python
            mkdir -p $IDIR/bin
            install -v -m755 python $IDIR/bin
        """,
        'version': '2.7.13',
        'extra': [
            {'kind': 'file', 'path': 'Modules/Setup.local', 'data': python_setup_local},
            {'kind': 'file', 'path': 'find_modules.py', 'data': find_modules},
        ],
        'meta': {
            'kind': kind,
            'depends': ['ncurses', 'iconv', 'intl', 'zlib', 'pkg_config', 'libffi', 'readline', 'termcap'],
            'soft': ['openssl'],
            'provides': [
                {'lib': 'python2.7'},
                {'env': 'PYTHON', 'value': '{pkgroot}/bin/python'},
            ],
        },
    }


@y.ygenerator(tier=0)
def python0():
    return python_base(['box'])


@y.ygenerator(tier=0)
def python_pth0():
    r = y.deep_copy(python_base([]))

    r['code'] = r['code'].replace('./configure', './configure --with-pth').replace('##', '')
    r['meta']['depends'].append('pth')
    r['meta']['env'] = [
        ('PTH', '--with-pth'),
    ]

    return r

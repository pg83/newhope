python_setup_local = """
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
"""

@y.ygenerator(tier=0, kind=['core', 'tool'])
def python0():
    return {
        'code': """
            source fetch "https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz" 1
            $(APPLY_EXTRA_PLAN_0)
            $YSHELL ./configure --prefix=$IDIR --disable-shared || exit1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'version': '2.7.13',
        'extra': [
            {'kind': 'file', 'path': 'Modules/Setup.local', 'data': python_setup_local},
        ],
        'meta': {
            'depends': ['ncurses', 'iconv', 'intl', 'zlib'],
            'soft': ['openssl'],
            'provides': [
                {'lib': 'python2.7'},
                {'env': 'PYTHON', 'value': '{pkg_root}/bin/python'},
            ],
        },
    }

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
spwd spwdmodule.c        # spwd(3)
grp grpmodule.c        # grp(3)
select selectmodule.c    # select(2); not on ancient System V

# Memory-mapped files (also works on Win32).
mmap mmapmodule.c

# Helper module for various ascii-encoders
binascii binascii.c

# Fred Drake's interface to the Python parser
parser parsermodule.c
"""


def python0(info, deps, codec):
    return {
        'code': """
            $(APPLY_EXTRA_PLAN_0)
            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared || exit 1
            make || exit 1
            make install
        """,
        'src': 'https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz',
        'deps': deps,
        'codec': codec,
        'extra': [
            {'kind': 'file', 'path': 'Modules/Setup.local', 'data': python_setup_local},
        ],
    }


@helper
def python1(info):
    return python0(info, [bestbox2(info), make2(info), tar2(info), xz2(info), curl2(info), musl2(info)], 'xz')


@helper
def python(info):
    return python0(info, [bestbox1(info), make1(info), tar1(info), xz1(info), curl1(info), musl1(info)], 'xz')

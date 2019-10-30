@y.cached()
def tool_test0(info, deps, codec):
    return y.to_v2({
        'code': """
           mkdir -p $IDIR/bin; echo 1 > $IDIR/bin/x
           which tar
           which xz1
        """,
        'deps': deps,
        'codec': codec,
    }, info)

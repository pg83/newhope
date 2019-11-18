def tool_test0():
    return {
        'code': """
           mkdir -p $IDIR/bin; echo 1 > $IDIR/bin/x
           which tar
           which xz1
        """
    }

@helper
def busybox():
    return {
        'code': """
        #pragma cc

        $(FETCH_URL)
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX
        ./busybox mv ./busybox $(INSTALL_DIR)/
        """,
        'src': 'https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2',
    }

@y.package
def base0():
    return {
        'code': """
            cd $IDIR
            mkdir -p etc etc/upm etc/runit pkg pkg/cache srv bin dev sys proc
            touch pkg/profile
            echo '. /pkg/profile' > etc/profile
            echo 'root:x:0:0:root:/root:/bin/sh' > etc/passwd

            cat > etc/group << "EOF"
root:x:0:
bin:x:1:
sys:x:2:
kmem:x:3:
tty:x:4:
tape:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
EOF
            echo 'nameserver 8.8.8.8' > etc/resolv.conf
        """,
        'meta': {
            'kind': ['tool'],
        },
    }

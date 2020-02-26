etc_profile = '''
. /pkg/profile

for i in $(ls /etc/profile.d/); do
    . "/etc/profile.d/$i"
done
'''


colors_sh = '''
# Сброс
Color_Off='\e[0m'       # Text Reset

# Обычные цвета
Black='\e[0;30m'        # Black
Red='\e[0;31m'          # Red
Green='\e[0;32m'        # Green
Yellow='\e[0;33m'       # Yellow
Blue='\e[0;34m'         # Blue
Purple='\e[0;35m'       # Purple
Cyan='\e[0;36m'         # Cyan
White='\e[0;37m'        # White

# Жирные
BBlack='\e[1;30m'       # Black
BRed='\e[1;31m'         # Red
BGreen='\e[1;32m'       # Green
BYellow='\e[1;33m'      # Yellow
BBlue='\e[1;34m'        # Blue
BPurple='\e[1;35m'      # Purple
BCyan='\e[1;36m'        # Cyan
BWhite='\e[1;37m'       # White

# Подчёркнутые
UBlack='\e[4;30m'       # Black
URed='\e[4;31m'         # Red
UGreen='\e[4;32m'       # Green
UYellow='\e[4;33m'      # Yellow
UBlue='\e[4;34m'        # Blue
UPurple='\e[4;35m'      # Purple
UCyan='\e[4;36m'        # Cyan
UWhite='\e[4;37m'       # White

# Фоновые
On_Black='\e[40m'       # Black
On_Red='\e[41m'         # Red
On_Green='\e[42m'       # Green
On_Yellow='\e[43m'      # Yellow
On_Blue='\e[44m'        # Blue
On_Purple='\e[45m'      # Purple
On_Cyan='\e[46m'        # Cyan
On_White='\e[47m'       # White

# Высоко Интенсивные
IBlack='\e[0;90m'       # Black
IRed='\e[0;91m'         # Red
IGreen='\e[0;92m'       # Green
IYellow='\e[0;93m'      # Yellow
IBlue='\e[0;94m'        # Blue
IPurple='\e[0;95m'      # Purple
ICyan='\e[0;96m'        # Cyan
IWhite='\e[0;97m'       # White

# Жирные Высоко Интенсивные
BIBlack='\e[1;90m'      # Black
BIRed='\e[1;91m'        # Red
BIGreen='\e[1;92m'      # Green
BIYellow='\e[1;93m'     # Yellow
BIBlue='\e[1;94m'       # Blue
BIPurple='\e[1;95m'     # Purple
BICyan='\e[1;96m'       # Cyan
BIWhite='\e[1;97m'      # White

# Высоко Интенсивные фоновые
On_IBlack='\e[0;100m'   # Black
On_IRed='\e[0;101m'     # Red
On_IGreen='\e[0;102m'   # Green
On_IYellow='\e[0;103m'  # Yellow
On_IBlue='\e[0;104m'    # Blue
On_IPurple='\e[0;105m'  # Purple
On_ICyan='\e[0;106m'    # Cyan
On_IWhite='\e[0;107m'   # White

export PS1="$BIRed\\h$BIGreen@\\u$BIBlue:\\w$BIWhite# $Color_Off"
'''


tmpdir_sh = '''
if test -z "$HOME"; then
    export HOME=$(getent passwd `whoami` | cut -d: -f6)
fi
export TMPDIR="$HOME/.tmpdir"
mkdir -p ""$TMPDIR"" || true
'''


group_sh = '''root:x:0:
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
'''


@y.package
def base0():
    return {
        'code': """
            cd $IDIR
            mkdir -p etc etc/upm etc/runit etc/runit/symlinks etc/profile.d pkg pkg/cache srv bin dev sys proc home root

            touch pkg/profile

            cd etc

            $(F_0)
            $(F_1)
            echo 'root:x:0:0:root:/root:/bin/sh' > passwd
            echo 'nameserver 8.8.8.8' > resolv.conf

            (
              cd profile.d
              $(F_3)
              $(F_4)
            )

            (
              cd runit/symlinks
              $(F_2)
              chmod +x run
            )
        """,
        'extra': [
            {'kind': 'file', 'path': 'profile', 'data': etc_profile},
            {'kind': 'file', 'path': 'group', 'data': group_sh},
            {'kind': 'file', 'path': 'run', 'data': y.builtin_data('data/stale_symlinks.py')},
            {'kind': 'file', 'path': '00-colors.sh', 'data': colors_sh},
            {'kind': 'file', 'path': '01-tmpdir.sh', 'data': tmpdir_sh},
        ],
        'meta': {
            'kind': ['tool'],
            'repacks': {},
        },
    }

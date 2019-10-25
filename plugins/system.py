def system00(info):
    return to_v2({
        'code': 'echo 1 > 2',
        'name': 'system',
        'version': '1.0.0',
        'deps': [],
        'codec': 'tr',
    }, info)


@y.options(repacks=None)
def system0(info):
    return system00(info)


@y.cached()
def devtools2(info):
    return [bestbox2_run(info), tar2_run(info), xz2_run(info), curl2_run(info), make2_run(info)]


@y.cached()
def devtools1(info):
    return [bestbox1_run(info), tar1_run(info), xz1_run(info), curl1_run(info), make1_run(info), python1_run(info)]


@y.cached()
def devtools(info):
    return [
        bestbox_run(info), coreutils_run(info), tar_run(info), xz_run(info),
        curl_run(info), make_run(info), python_run(info), m4_run(info),
    ]


@y.cached()
def devtools_last(info):
    return [
        bestbox_run(info), coreutils_run(info), tar_run(info), xz_run(info),
        curl_run(info), make_run(info), python_run(info), m4_run(info),
    ]

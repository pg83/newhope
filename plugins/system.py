@helper
def system0(info):
    return {
        'code': '',
        'name': 'system',
        'version': '1.0.0',
        'deps': [],
    }


@cached
def devtools2(info):
    return [bestbox2(info), tar2(info), xz2(info), curl2(info), make2(info), musl2(info)]


@cached
def devtools1(info):
    return [bestbox1(info), tar1(info), xz1(info), curl1(info), make1(info), musl1(info), python1(info)]


@cached
def devtools(info):
    return [bestbox(info), tar(info), xz(info), curl(info), make(info), musl(info), python(info), m4(info)]

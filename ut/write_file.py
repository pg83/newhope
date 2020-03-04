def is_tmp_name(x):
    if '-tmp.' in x:
        return True

    return x.endswith('-tmp')


def tmp_name(x):
    return x + '-tmp.' + str(y.random.random())


def write_file_0(path, data, mode):
    tmp = tmp_name(path)

    with open(tmp, mode) as f:
        f.write(data)
        f.flush()

    y.os.rename(tmp, path)


def write_file(path, data, mode='wb'):
    try:
        return write_file_0(path, data, mode)
    except Exception as e:
        y.info('can not write file, will retry', str(e))
        y.time.sleep(1)

    return write_file_0(path, data, mode)


def copy_file(to, fr):
    with open(fr, 'rb') as f:
        data = f.read()

    write_file(to, data)

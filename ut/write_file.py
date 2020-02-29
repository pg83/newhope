def write_file(path, data, mode='wb'):
    tmp = path + '-tmp.' + str(y.random.random())

    with open(tmp, mode) as f:
        f.write(data)
        f.flush()

    y.os.rename(tmp, path)


def copy_file(to, fr):
    with open(fr, 'rb') as f:
        data = f.read()

    write_file(to, data)

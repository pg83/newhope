def write_file(path, data):
    tmp = path + str(y.random.random())

    with open(tmp, 'wb') as f:
        f.write(data)
        f.flush()

    y.os.rename(tmp, path)

def fetch_data(url):
    def fetch_1(url):
        import urllib.request as urllib2

        return urllib2.urlopen(url).read()

    def fetch_2(url):
        return y.subprocess.check_output(['curl -s -S --retry 3 -L -k -o - ' + url], shell=True)

    def fetch_3(url):
        return y.subprocess.check_output(['curl -s -S --retry 3 -L -o - ' + url], shell=True)

    e = None

    for f in (fetch_1, fetch_2, fetch_1, fetch_3):
        try:
            res = f(url)

            if len(res) < 300:
                raise Exception('too small responce')

            return res
        except Exception as err:
            e = err
            y.xprint_r(e)

    if e:
        raise e


def fetch_http(root, url, name=None, untar=True):
    name = name or y.os.path.basename(url)
    fname = y.os.path.join(root, name)
    data = fetch_data(url)

    try:
        y.os.makedirs(root)
    except OSError:
        pass

    with open(fname, 'w') as f:
        f.buffer.write(data)

    if untar:
        if '.zip' in name:
            y.subprocess.check_output(['unzip ' + name], cwd=root, shell=True)
        else:
            y.subprocess.check_output(['tar -xf ' + name], cwd=root, shell=True)

    return fname

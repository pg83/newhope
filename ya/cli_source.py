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
            return f(url)
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


@y.main_entry_point
async def cli_pkg_source(arg):
    parser = y.argparse.ArgumentParser()

    parser.add_argument('--path', default='data', action='store', help='Where to store all')
    parser.add_argument('targets', nargs=y.argparse.REMAINDER)

    args = parser.parse_args(arg)
    args.path = y.os.path.abspath(args.path)

    async def find_func():
        funcs = await y.gen_mk_data(list(y.iter_cc()))
        print funcs 

        def do():
            for d in funcs:
                n = (d['gen'] + '-' + d['base']).replace('-', '_')
                c = d['code']

                yield n, c

        return dict(do())

    funcs = await find_func()

    print funcs

    @y.lookup
    def lookup(name):
        return funcs[name]

    def iter_urls():
        for t in args.targets:
            if t.startswith('http'):
                yield url
            else:
                t = t.replace('-', '_')
                node = y.restore_node_node(eval('y.' + t)())
                url = node.get('src') or node.get('url')

                if url:
                    yield url

                urls = node.get('urls')

                if urls:
                    for url in urls:
                        yield url
   
    for url in iter_urls():
        print('will fetch', url, fetch_http(args.path, url))

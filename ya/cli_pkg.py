import marshal
import time
import urllib.request as urllib2


def fetch_url_data(fr):
    return y.decode_prof(y.fetch_data(fr))


@y.main_entry_point
async def cli_pkg_init(args_):
    p = y.argparse.ArgumentParser()

    p.add_argument('--fr', default='http://index.samokhvalov.xyz', action='store', help='output repo')
    p.add_argument('--barebone', default=False, action='store_const', const=True, help='prepare structure for barebone install')
    p.add_argument('--where', default='.', action='store', help='where to find installation')
    p.add_argument('--target', default='lmx8', action='store', help='shorter form of target info')

    args = p.parse_args(args_)
    where = y.os.path.abspath(args.where)

    assert not args.barebone

    y.PkgMngr(args.target, where).init_place()


@y.main_entry_point
async def cli_pkg_search(args_):
    p = y.argparse.ArgumentParser()

    p.add_argument('--target', default=None, action='store', help='shorter form of target info')
    p.add_argument('--where', default=None, action='store', help='where to find installation')
    p.add_argument('--list-all', default=False, action='store_true', help='list dev packages')
    p.add_argument('pkg', nargs=y.argparse.REMAINDER)

    args = p.parse_args(args_)

    for p in y.PkgMngr(args.target, args.where).search_pkgs(args.pkg, list_all=args.list_all):
        y.info(p['path'], 'build at', p['ts'])


@y.main_entry_point
async def cli_pkg_add(args_):
    p = y.argparse.ArgumentParser()

    p.add_argument('--where', default=None, action='store', help='where to find installation')
    p.add_argument('pkg', nargs=y.argparse.REMAINDER)

    args = p.parse_args(args_)

    y.PkgMngr(path=args.where).install(args.pkg)


@y.main_entry_point
async def cli_pkg_showdb(args_):
   with y.PkgMngr().open_db() as db:
       print db.db

    
@y.verbose_entry_point
async def cli_pkg_sync_repo(args_):
    parser = y.argparse.ArgumentParser()

    parser.add_argument('--fr', default=[], action='append', help='input repo')
    parser.add_argument('--to', default='', action='store', help='output repo')

    args = parser.parse_args(args_)

    assert args.fr
    assert args.to

    try:
        y.os.makedirs(args.to)
    except OSError:
        pass

    for fr in args.fr:
        for x in y.os.listdir(fr):
            z = y.os.path.join(args.to, x)

            if y.os.path.isfile(z):
                y.info('already exists', z)
            else:
                y.info('copy file ', x, ' to ', z)
                y.shutil.copyfile(y.os.path.join(fr, x), z + '.tmp')
                y.os.rename(z + '.tmp', z)

    index = []

    y.info('will write index')

    for f in sorted(y.os.listdir(args.to)):
        if len(f) > 10:
            p = y.os.path.join(args.to, f)

            if f.endswith('-tmp'):
                y.os.unlink(p)
                continue

            index.append({'path': f, 'length': y.os.path.getsize(p), 'ts': int(1000000 * y.os.path.getmtime(p))})

    with open(args.to + '/index', 'w') as f:
        f.buffer.write(y.encode_prof(index))


from http.server import HTTPServer, BaseHTTPRequestHandler


@y.verbose_entry_point
async def cli_pkg_serve_repo(args_):
    parser = y.argparse.ArgumentParser()

    parser.add_argument('--fr', default='', action='store', help='path to repo')
    parser.add_argument('--port', default=80, action='store', help='listen port')

    args = parser.parse_args(args_)   

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            y.info('incoming connection')

            with open(args.fr + self.path, 'rb') as f:
                data = f.read()

            self.send_response(200)
            self.send_header('content-length', str(len(data)))
            self.end_headers()

            self.wfile.write(data)

    httpd = HTTPServer(('0.0.0.0', int(args.port)), SimpleHTTPRequestHandler)
    y.info('start server')
    httpd.serve_forever()

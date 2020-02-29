import marshal
import time
import urllib.request as urllib2


def fetch_url_data(fr):
    return y.decode_prof(y.fetch_data(fr))


@y.main_entry_point
def cli_pkg_init(args_):
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
def cli_pkg_search(args_):
    p = y.argparse.ArgumentParser()

    p.add_argument('--target', default=None, action='store', help='shorter form of target info')
    p.add_argument('--where', default=None, action='store', help='where to find installation')
    p.add_argument('--list-all', default=False, action='store_true', help='list dev packages')
    p.add_argument('pkg', nargs=y.argparse.REMAINDER)

    args = p.parse_args(args_)

    for p in y.PkgMngr(args.target, args.where).search_pkgs(args.pkg, list_all=args.list_all):
        y.info(p['path'], 'build at', p['ts'])


@y.main_entry_point
def cli_pkg_add(args_):
    p = y.argparse.ArgumentParser()

    p.add_argument('--where', default=None, action='store', help='where to find installation')
    p.add_argument('--index', default=False, action='store_const', const=True, help='add index, not package')
    p.add_argument('pkg', nargs=y.argparse.REMAINDER)

    args = p.parse_args(args_)

    if args.index:
        y.PkgMngr(path=args.where).add_indexes(args.pkg)
    else:
        y.PkgMngr(path=args.where).install(args.pkg)


@y.main_entry_point
def cli_pkg_del(args_):
    p = y.argparse.ArgumentParser()

    p.add_argument('--where', default=None, action='store', help='where to find installation')
    p.add_argument('pkg', nargs=y.argparse.REMAINDER)

    args = p.parse_args(args_)

    y.PkgMngr(path=args.where).delete_x(args.pkg)


@y.main_entry_point
def cli_pkg_up(args_):
    p = y.argparse.ArgumentParser()
    p.add_argument('--where', default=None, action='store', help='where to find installation')
    args = p.parse_args(args_)

    y.PkgMngr(path=args.where).install([])


@y.main_entry_point
def cli_pkg_showdb(args_):
   with y.PkgMngr().open_db() as db:
       print db.db


@y.verbose_entry_point
def cli_pkg_sync_repo(args_):
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
                y.debug('already exists', z)
            else:
                y.info('copy file ', x, ' to ', z)
                y.copy_file(z, x)
 
    index = y.build_index(args.to)

    y.info('will write index')
    y.write_file(args.to + '/index', y.encode_prof(index))


@y.verbose_entry_point
def cli_pkg_serve_repo(args_):
    parser = y.argparse.ArgumentParser()

    parser.add_argument('--fr', default='', action='store', help='path to repo')
    parser.add_argument('--port', default=80, action='store', help='listen port')

    args = parser.parse_args(args_)

    class ThreadingHTTPServer(y.socketserver.ForkingMixIn, y.http.server.HTTPServer):
        pass

    class RequestHandler(y.http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            y.info('incoming connection')

            with open(args.fr + self.path, 'rb') as f:
                data = f.read()

            self.send_response(200)
            self.send_header('content-length', str(len(data)))
            self.end_headers()

            self.wfile.write(data)

    httpd = ThreadingHTTPServer(("", int(args.port)), RequestHandler)
    y.info('start server')
    httpd.serve_forever()

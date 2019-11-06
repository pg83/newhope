def fetch_data(url):
   def fetch_1(url):
      return y.urllib2.urlopen(url).read()

   def fetch_2(url):
      return y.subprocess.check_output(['curl -o - ' + url], shell=True)

   for f in (fetch_1, fetch_2):
      try:
         return f(url)
      except Exception as e:
         print e

   if e:
      raise e


def fetch_http(root, url):
   name = y.os.path.basename(url)
   fname = y.os.path.join(root, name)
   data = fetch_data(url)

   try:
      y.os.makedirs(root)
   except OSError:
      pass

   with open(fname, 'w') as f:
      f.write(data)

   y.subprocess.check_output(['tar -xf ' + name], cwd=root, shell=True)

   return url


@y.main_entry_point
def cli_source(arg, verbose):
   parser = y.argparse.ArgumentParser()

   parser.add_argument('--path', default='data', action='store', help='Where to store all')
   parser.add_argument('targets', nargs=y.argparse.REMAINDER)

   args = parser.parse_args(arg)
   args.path = y.os.path.abspath(args.path)

   def iter_urls():
      host = y.current_host_platform()
      target = host
      cc = {'host': host, 'target': target}
      params = {'info': cc, 'compilers': {'deps': [], 'cross': False}}

      for t in args.targets:
         if t.startswith('http'):
            yield url
         else:
            node = y.restore_node_node(eval('y.' + t)(y.deep_copy(params)))
            url = node.get('src') or node.get('url')

            if url:
               yield url

            urls = node.get('urls')

            if urls:
               for url in urls:
                  yield url
               
   for url in iter_urls():
      print 'will fetch', url, fetch_http(args.path, url)

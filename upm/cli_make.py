@y.main_entry_point
def cli_make(arg):
   p = y.argparse.ArgumentParser()

   p.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
   p.add_argument('-f', '--path', default='gen', action='store', help='path to Makefile, "-" - read from stdin, "gen" - generate on the fly')
   p.add_argument('-r', '--root', default=None, action='store', help='main root for build files')
   p.add_argument('-i', '--install-dir', default=None, action='store', help='where to install packages')
   p.add_argument('-d', '--do-not-remove', default=None, action='store', help='не удалять даннные')
   p.add_argument('-s', '--shell', default=None, action='store', help='указать шелл для сборки')
   p.add_argument('--production', default=False, action='store_const', const=True, help='production execution')
   p.add_argument('targets', nargs=y.argparse.REMAINDER)

   args = p.parse_args(arg)
   local = not args.production

   if local and args.install_dir:
      raise Exception('do not do this, kids, at home')

   def calc_root():
      if args.root:
         return args.root

      if local:
         return y.upm_root()

      if args.production:
         return '/d'

      raise Exception('can not determine root')

   root = calc_root()

   def iter_replaces():
      if args.install_dir:
         yield ('$PD', args.install_dir)

      yield ('$MD', '$PREFIX/m')
      yield ('$RD', '$PREFIX/r')
      yield ('$WD', '$PREFIX/w')

      if local:
         yield ('$PD', '$PREFIX/p')

      if args.production:
         yield ('$PD', '/private')

      yield ('$PREFIX', root)

      if args.shell:
         yield ('$YSHELL', args.shell)

   shell_vars = dict(iter_replaces())
   parsed = False
   
   if args.path == 'gen':
      data = y.decode_internal_format(y.main_makefile(internal=True))
      parsed = True
   elif args.path == '-':
      data = y.sys.stdin.read()
   elif args.path:
      with open(args.path, 'r') as f:
         data = f.read()
   else:
      data = y.sys.stdin.read()

   threads = int(args.threads)

   if threads:
      y.run_makefile(data, shell_vars, [], args.targets, threads, parsed, pre_run=['workspace'])

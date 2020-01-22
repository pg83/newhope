import itertools


def check_arg_2(args, p, with_arg=False):
   res = {p: None}

   def flt():
      it = itertools.chain(args)

      for x in it:
         if x == p:
            res[p] = True

            if with_arg:
               for y in it:
                  res[p] = y

                  for z in it:
                     yield z

                  return

            for y in it:
               yield y

            return

         yield x

   return list(flt()), res[p]


def check_arg(args, params):
   old_len = len(args)

   for p in params:
      args, _ = check_arg_2(args, p)

   return args, len(args) != old_len


def parse_args(args):
    args, verbose = check_arg(args, ('-v', '--verbose'))
    args, profile = check_arg(args, ('--profile',))
    args, verbose_mode = check_arg_2(args, '-vm', True)

    if verbose_mode is None:
        args, verbose_mode = check_arg_2(args, '--verbose-mode', True)

    if verbose_mode:
        verbose = verbose_mode
    else:
        if verbose:
            verbose = '1'
        else:
            verbose = ''

    if len(args) < 2:
        args = args + ['help']

    return args, verbose, profile

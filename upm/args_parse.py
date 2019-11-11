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

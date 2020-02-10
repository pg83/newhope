def output_build_results(arg):
    if 'target' in arg:
        arg['_target'] = y.to_pretty_name(arg.pop('target'))

    if 'output' in arg:
        data = arg.pop('output').strip()

    if (status := arg.get('status', '')) == 'fail':
        arg['message'] = arg.get('message', '') + '\n' + data

    if 'message' in arg:
        y.build_results({'info': {'message': arg.pop('message'), 'extra': arg}})

    if 'info' in arg:
        y.info(arg['info']['message'], extra=arg['info']['extra'])


def run_make_0(mk, args):
    @y.lookup
    def lookup(name):
        return {'build_results': output_build_results}[name]

    return y.run_makefile(mk, args.targets, int(args.threads), pre_run=args.pre_run)

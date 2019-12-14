async def run_make_0(mk, args):
    is_debug = y.make_exec.is_debug
    
    async def do_run(build_results):
        @y.lookup
        def lookup(name):
            return {'build_results': build_results}[name]
        
        return await y.run_makefile(mk, args.targets, int(args.threads), pre_run=args.pre_run)
            
    async def do_run_log(ctl):
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

        return await do_run(output_build_results)
            
    return await y.spawn(do_run_log)

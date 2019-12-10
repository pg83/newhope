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
            
            if 'text' in arg:
                data = arg.pop('text').strip()
                ll = {'failure': 'info'}.get(arg.get('status', ''), 'debug')

                y.build_results({ll: '{w}' + data + '{}'})
            
            if 'message' in arg:
                colors = {
                    'fail': '{br}',
                    'done': '{bb}',
                    'init': '{by}',
                }

                msg = arg.pop('message')[:4].lower()
                color = colors.get(msg, '{bw}')
                msg = color + msg.upper() + '{}'
                
                y.build_results({'info': {'message': msg, 'extra': arg}})

            if 'debug' in arg:
                is_debug() and y.debug('%s', arg['debug'])
                
            if 'info' in arg:
                y.info(arg['info']['message'], extra=arg['info']['extra'])

        return await do_run(output_build_results)
            
    return await y.spawn(do_run_log)

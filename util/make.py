@y.singleton
def get_white_line():
    return '{w}-----------------------------------------------{}'


def prettify(arg, t):
    if 'target' in arg:
        tg = arg['target']
        cn = y.to_pretty_name(tg)
                    
        return t.replace(tg, cn).replace('[cname]', cn)
            
    return t


async def run_make_0(data, shell_vars, args):
    is_debug = y.make_exec.is_debug
    
    async def do_run(build_results):
        @y.lookup
        def lookup(name):
            return {'build_results': build_results}[name]
        
        return await y.run_makefile(data, shell_vars, args.targets, int(args.threads), pre_run=['workspace'])
        
    async def do_run_console(ctl):
        white_line = get_white_line()
      
        def output_build_results(arg):        
            pretty = lambda x: prettify(arg, x)
            
            if 'text' in arg:
                data = arg['text'].strip()
            
                y.build_results({'write': pretty(y.xxformat(white_line, '\n{bw}', data, '{}\n'))})
            
            if 'message' in arg:
                if arg.get('status', '') == 'failure':
                    color = '{br}'
                else:
                    color = '{bb}'
               
                y.build_results({'write': pretty(y.xxformat(white_line + '\n' + color + arg['message'] + '{}\n'))})

            if 'write' in arg:
                y.stderr.write(arg['write'])

        return await do_run(output_build_results)
    
    async def do_run_log(ctl):
        def output_build_results(arg):        
            pretty = lambda x: prettify(arg, x)

            if 'text' in arg:
                data = arg['text'].strip()
                ll = {'failure': 'info'}.get(arg.get('status', ''), 'debug')

                y.build_results({ll: pretty('{w}' + data + '{}')})
            
            if 'message' in arg:
                color = {'failure': '{r}'}.get(arg.get('status', ''), '{b}')
               
                y.build_results({'info': pretty(color + arg['message'] + '{}')})

            if 'debug' in arg:
                is_debug() and y.debug('%s', arg['debug'])
                
            if 'info' in arg:
                y.info('%s', arg['info'])

        return await do_run(output_build_results)
            
    return await y.spawn(do_run_log)

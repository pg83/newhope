@y.singleton
def get_white_line():
    return '{w}-----------------------------------------------{}'


def build_callback(x):
    return y.BUILD_LOOP.read_callback(x)


def results_callback():
    return build_callback('RESULTS')


@y.singleton
def build_results_channel():
    return y.BUILD_LOOP.write_channel('RESULTS', 'common')


def run_make_0(data, parsed, shell_vars, args):
    build_results = build_results_channel()
    
    def do_run():    
        @results_callback()
        def on_react_status(arg):
            if arg.get('status', '') == 'build complete':
                raise y.StopNow()
            
        @results_callback()
        def on_check_status(arg):
            status = ''
        
            if arg.get('status', '') == 'failure':
                status = 'build complete'
            
            if arg.get('retcode', 0):
                status = 'build complete'

            if status:
                build_results({'status': status})
        
        @y.signal_channel.read_callback()
        def on_sig_int(arg):
            if arg['signal'] == 'INT':
                build_results({'message': 'SIGINT happens', 'status': 'failure'})
                
        return y.run_makefile(data, shell_vars, [], args.targets, int(args.threads), parsed, pre_run=['workspace'], bypass_streams=args.proxy)
        
    def do_run_console():
        white_line = get_white_line()
      
        @results_callback()
        def output_build_results(arg):        
            def pretty(t):
                if 'target' in arg:
                    tg = arg['target']
                    cn = y.to_pretty_name(tg)
                    
                    return t.replace(tg, cn).replace('[cname]', cn)
            
                return t

            if 'text' in arg:
                data = arg['text'].strip()
            
                build_results({'write': pretty(white_line + '\n' + '{w}' + data + '{}\n')})
            
            if 'message' in arg:
                if arg.get('status', '') == 'failure':
                    color = '{r}'
                else:
                    color = '{b}'
               
                build_results({'write': pretty(white_line + '\n' + color + arg['message'] + '{}\n')})

            if 'write' in arg:
                y.stderr.write(arg['write'])
                
        return do_run()
    
    y.BUILD_LOOP.run_loop(init=[do_run_console])

    return 0

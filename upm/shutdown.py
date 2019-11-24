@y.defer_constructor
def init_shutdown():
    def register_sigint_handler():
        @y.signal_channel.read_callback()
        def on_sigint_shutdown(arg):
            if arg['signal'] == 'INT':
                on_sigint_shutdown_0()

    @y.singleton
    def on_sigint_shutdown_0():
        bcy = y.broadcast_channel('SIGNAL')

        def exit_handler(*args):
            y.os._exit(6)

        t = y.time.time()

        @y.run_by_timer(0.1)
        def death_handler():
            if y.time.time() > t + 0.5:
                y.run_down_once()
            
            if y.time.time() > t + 1.5:
                try:
                    y.xprint_red('DEATH handler')
                finally:
                    exit_handler()

        death_handler()

    def register_shutdown():
        cb = []

        def run_cb():
            for d in reversed(cb):
                try:
                    d()
                except:
                    pass

        @y.signal_channel.read_callback()
        def on_shutdown(arg):
            if arg['signal'] == 'DOWN':
                if 'on_shutdown' in arg:
                    cb.append(arg['on_shutdown'])  
                elif 'when' in arg:
                    run_cb()
        
        #y.signal_channel({'signal': 'DOWN', 'on_shutdown': lambda: y.print_all_stacks()})

    register_sigint_handler()
    register_shutdown()


@y.defer_constructor
def init_signals():
    bcy = y.broadcast_channel('SIGNAL')

    def init_sigint():
        def sig_handler(*args):
            bcy({'args': args, 'signal': 'INT'})

        y.sys.modules['__main__'].real_handler = sig_handler

    init_sigint()
        
    @y.signal_channel.read_callback()
    def on_sigint_caret(arg):
        if arg['signal'] == 'INT':
            y.stderr.write('\n')

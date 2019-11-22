def init_vault():
    def vault1():
        @y.main_channel.read_callback()
        def on_new_msg(msg):
            try:
                msg['func']()
            except SystemExit as e:
                raise e
            except:
                try:
                    y.print_tbs()
                except:
                    pass

                raise SystemExit(1)

    def vault():
        try:
            return y.MAIN_LOOP.run_loop(init=vault1)
        finally:
            #y.run_down_once()
            pass

    y.homeland_queue.put(vault)

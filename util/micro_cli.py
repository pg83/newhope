@y.main_entry_point
async def cli_offload(args):
    print await y.async_loop.offload(lambda: y.subprocess.check_output("ls -la", shell=True))

    
@y.main_entry_point
async def cli_pubsub(args):
    ps = y.PubSubLoop()

    async def f1(ctl, inq):
        yield y.EOP(y.ACCEPT('A'), y.PROVIDES('B'))

        yield y.ELEM(2)
        yield y.EOP()
        
        async for i in inq:
            i = i.data.data
            #y.info('got f1', i)
            print 'f1', i
            yield y.ELEM(i)
            yield y.EOP()

        yield y.FIN()

    async def f2(ctl, inq):
        yield y.EOP(y.ACCEPT('B'), y.PROVIDES('A'))

        yield y.ELEM(1)
        yield y.EOP()

        async for i in inq:
            i = i.data.data
            #y.info('got f2', i)
            print 'f2', i
            yield y.ELEM(i)
            yield y.EOP()

        yield y.FIN()

    ps.wrap_coro(f1)
    ps.wrap_coro(f2)

    await ps.run()


@y.main_entry_point
async def cli_template(args):
    d = y.collections.deque([1, 2, 3])

    if args[0] == 'sync':
        for i in y.deque_iter_sync(d):
            print i
    else:
        async for i in y.deque_iter_async(d):
            print i


@y.main_entry_point
async def cli_timeout(args):
    tout = int(args[0])
    pid = y.os.fork()

    if pid:
        y.time.sleep(tout)
        y.os.kill(pid, y.signal.SIGINT)
        y.os.waitpid(pid, 0)
        y.os._exit(0)
    else:
        import os
        
        os.execv(args[1], args[1:])

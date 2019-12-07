@y.verbose_entry_point
async def cli_offload(args):
    print await y.async_loop.offload(lambda: y.subprocess.check_output("ls -la", shell=True))


@y.verbose_entry_point
async def cli_test_ctx(args):
    async def func1():
        c = y.current_coro()
        
        while True:
            await c.sleep(1)
            print(c)
            
    async def func2():
        c = y.current_coro()
        
        while True:
            await c.sleep(2)
            print(c)
    
    a1 = y.current_coro().spawn(func1)
    a2 = y.current_coro().spawn(func2)

    await a1
    await a2

    
@y.asyncio.coroutine
def awkward_suspend():
    yield

    
@y.verbose_entry_point
async def cli_test_q(args):
    q = y.QQ(y.async_loop)
    #q = y.MTQ()
    #q = y.PQ()
    
    async def func1(ctl):
        while True:
            for i in range(0, 2000):
                print await q.async_pop()
                await ctl.sched_yield()
                q.push(int(y.random.random() * 1000))
                q.push(int(y.random.random() * 1000))
            
    async def func3(ctl):
        while True:
            for i in range(0, 500):
                print await q.async_pop()
                await q.async_pop()
                await ctl.sched_yield()
                q.push(int(y.random.random() * 1000))
            
    async def func2(ctl):
        while True:
            for i in range(0, 100):
                q.push(int(y.random.random() * 1000))
            
            await ctl.sched_yield()
        
            for i in range(0, 100):
                await q.async_pop()
        
    c = []
        
    for i in range(0, 20):
        c.append(y.spawn(func1, 'func1_' + str(i)))
        c.append(y.spawn(func2, 'func2_' + str(i)))
        c.append(y.spawn(func3, 'func3_' + str(i)))

    for x in c:
        await x
        
    
@y.verbose_entry_point
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


@y.verbose_entry_point
async def cli_template(args):
    d = y.collections.deque([1, 2, 3])

    if args[0] == 'sync':
        for i in y.deque_iter_sync(d):
            print i
    else:
        async for i in y.deque_iter_async(d):
            print i


@y.verbose_entry_point
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

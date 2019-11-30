@y.main_entry_point
async def cli_pubsub(args):
    ps = y.PubSubLoop()

    async def f1(ctl, inq):
        print 'f1'
        yield y.EOP(y.ACCEPT('A'), y.PROVIDES('B'))

        yield y.ELEM(2)
        yield y.EOP()
        
        async for i in inq:
            i = i.data.data
            print 'f1', i
            
            yield y.ELEM(i)
            yield y.EOP()

        yield y.FIN()

    async def f2(ctl, inq):
        print 'f2'
        yield y.EOP(y.ACCEPT('B'), y.PROVIDES('A'))

        yield y.ELEM(1)
        yield y.EOP()

        async for i in inq:
            i = i.data.data
            print 'f2', i
            
            yield y.ELEM(i)
            yield y.EOP()

        yield y.FIN()

    ps.wrap_coro(f1)
    ps.wrap_coro(f2)

    await ps.run()

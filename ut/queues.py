import collections as cc


NOV = '$'


class QQ(object):
    def __init__(self, loop):
        self.l = loop
        self.q = cc.deque()
        self.c = cc.deque()

    def cycle(self):
        while True:
            try:
                c = self.c.popleft()
            except IndexError:
                return

            try:
                v = self.q.popleft()
            except IndexError:
                return self.c.append(c)

            #print 'ZZZZZZZZZZZZZ', c, v
            c(v)

    def pop_0(self, fut):
        def cb(v):
            #print 'XXXXXXXX', fut, v
            fut.set_result(v)
        
        self.c.append(cb)
        self.cycle()

    async def async_pop(self):
        fut = self.l.create_future(y.set_name(lambda: self.pop_0(fut), 'qq_pop'))
        await fut
        res = fut.result()

        return res
    
    def push(self, v):
        self.q.append(v)
        self.cycle()
        
    
class MTQ(object):
    def __init__(self, *args):
        self.q = y.queue.SimpleQueue()

    def push(self, v):
        self.q.put(v)

    def pop(self):
        return self.q.get()
    
    async def async_pop(self):
        return self.pop()

    def try_pop(self):
        try:
            return self.q.get_nowait()
        except y.queue.Empty:
            return NOV

        
class PQ(object):
    def __init__(self, *args):
        self.r, self.w = y.os.pipe()

    def push(self, v):
        y.os.write(self.w, y.struct.pack('I', v))

    async def async_pop(self):
        return self.pop()
    
    def pop(self):
        return y.struct.unpack('I', y.os.read(self.r, 4))[0]
    

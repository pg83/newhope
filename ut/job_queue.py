def wrap_pair(res, err):
    def wrapper():
        if err:
            raise err

        return res

    return wrapper


class JobQueue(object):
    def __init__(self, numthrs):
        self._inq = y.queue.SimpleQueue()
        self._ouq = y.queue.SimpleQueue()
        self._t = [y.threading.Thread(target=self.run) for x in range(0, numthrs)]

        for t in self._t:
            t.start()

    def run(self):
        while True:
            try:
                (res, err) = (self._inq.get()(), None)
            except StopIteration:
                return
            except Exception as e:
                (res, err) = (None, e)

            self._ouq.put(wrap_pair(res, err))

    def put(self, job):
        self._inq.put(job)

    def get(self):
        return self._ouq.get()()

    def stop(self):
        def stop_iter():
            raise StopIteration()

        for _ in self._t:
            self.put(stop_iter)

    def join(self):
        for t in self._t:
            t.join()


@y.verbose_entry_point
def cli_test_jobqueue(args):
    jq = JobQueue(4)

    def wrap(n):
        return lambda: n

    for i in range(0, 1000):
        jq.put(wrap(i))

    sum = 0

    for i in range(0, 1000):
        sum += jq.get()

    jq.stop()
    jq.join()

    print sum


def iter_deque(q):
    while True:
        try:
            yield q.popleft()
        except IndexError:
            yield None


class ProducerQueue(object):
    def __init__(self, numthrs, prod, cons):
        self._jq = JobQueue(numthrs)
        self._p = prod
        self._c = cons

    def run(self):
        q = y.collections.deque()

        def iter_q():
            for el in iter_deque(q):
                if el is None:
                    q.append(self._jq.get())
                else:
                    yield el

        def wrap(el):
            return lambda: self._c(el)

        for el in self._p(iter_q()):
            self._jq.put(wrap(el))


@y.verbose_entry_point
def cli_test_prodqueue(args):
    def prod(q):
        lst = []

        for i in range(0, 1000):
            el = {
                'output': i,
                'lst': lst,
                'inputs': [(int(y.random.random() * 100000000) % len(lst)) for x in range(0, min(len(lst), 2))]
            }

            lst.append(el)

        for l in lst:
            yield l

        sun = 0
        cnt = 0

        for l in lst:
            for el in q:
                break

            sun += el
            cnt += 1

        print sun, cnt

    def cons(el):
        return sum([el['lst'][x]['output'] for x in el['inputs']], 0)

    pq = ProducerQueue(4, prod, cons)
    pq.run()

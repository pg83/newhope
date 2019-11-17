def inc_counter():
    c = [int(y.random.random() * 10000)]

    def func():
        c[0] += 1
        return c[0]

    return func

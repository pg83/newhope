MASK32 = 2**32 - 1
MASK64 = 2**64 - 1


def srandom(initstate, initseq):
    rng = [0, (initseq << 1) & MASK64 | 1]
    random(rng)
    rng[0] += initstate
    rng[0] &= MASK64
    random(rng)

    return rng


def random(rng):
    oldstate, inc = rng
    rng[0] = (oldstate * 6364136223846793005 + inc) & MASK64
    xorshifted = (((oldstate >> 18) ^ oldstate) >> 27) & MASK32
    rot = (oldstate >> 59) & MASK32

    return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & MASK32


class PCGRandom(object):
    def __init__(self, state, seq):
        self.rng = srandom(state, seq)

    def next_random(self):
        return random(self.rng)

    def next_float(self):
        while (res := self.next_random() / (MASK32 + 1.0)) >= 1.0:
            pass

        return res
    
    def iter_float(self):
        while True:
            yield self.next_float()

    def iter_int(self):
        while True:
            yield self.next_random()

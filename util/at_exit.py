@y.singleton
def at_exit():
    AT_EXIT = []

    return AT_EXIT


def run_at_exit(f):
    at_exit().append(f)

    return f


def run_handlers():
    ae = at_exit()
    
    while ae:
        xx = [y for y in ae]
        ae.clear()
        
        for x in reversed(xx):
            try:
                x()
            except:
                pass

        ae = at_exit()

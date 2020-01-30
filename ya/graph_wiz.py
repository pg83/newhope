def build_dot_script_0(mk):
    lst = mk.lst

    def fix(x):
        return x[1:].replace('/', '-').replace('-', '')

    def iter():
        yield 'digraph G {'

        for c in lst:
            if c.get('cmd'):
                for a in mk.nums_to_str(c['deps1']):
                    for b in mk.nums_to_str(c['deps2']):
                        yield '    ' + fix(a) + ' -> ' + fix(b) + ';'

        yield '}'

    return '\n'.join(iter()) + '\n'

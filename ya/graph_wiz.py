def build_dot_script_0(mk):
    lst = mk.lst

    def fix(x):
        return x[1:].replace('/', '-').replace('-', '').replace('+', '').replace('.', '')

    def iter():
        yield 'digraph G {'

        for c in lst:
            if c.get('cmd'):
                c = mk.restore_node(c)

                for a in c['deps1']:
                    for b in c['deps2']:
                        yield '    ' + fix(a) + ' -> ' + fix(b) + ';'

        yield '}'

    return '\n'.join(iter()) + '\n'

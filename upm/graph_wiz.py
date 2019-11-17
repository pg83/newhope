def build_dot_script():
    lst = y.decode_internal_format(y.main_makefile(internal=True))

    def fix(x):
        return x[1:].replace('/', '-').replace('-', '')

    def iter():
        yield 'digraph G {'
        
        for c in lst:
            if c.get('cmd'):
                for a in c['deps1']:
                    for b in c['deps2']:
                        yield '    ' + fix(a) + ' -> ' + fix(b) + ';'

        yield '}'

    return '\n'.join(iter()) + '\n'

import sys
import base64


def subst(v):
    def iter_subst():
        yield ('$MD', '$PREFIX/m')
        yield ('$RD', '$PREFIX/r')
        yield ('$WD', '$PREFIX/w')
        yield ('$PD', '$PREFIX/p')

    return y.subst_kv_base(v, iter_subst())


async def build_sh_script(targets):
    res = [1]
    await y.run_makefile(y.main_makefile(), res, targets, 1)
    res = res[1:]

    def iter_cmd():
        for cmd in res:
            try:
                input = subst(cmd['input'])

                if 'EOF' in input:
                    input = input + 'EOF\n'

                yield '(echo "export PREFIX=$1"; (echo "' + base64.b64encode(input) + '" | base64 -D -i - -o -)) > data; (cat data | /usr/bin/env -i /usr/local/bin/dash -s) || exit 1'
            except Exception as e:
                y.xprint_red('------------------------------------------\n', cmd, e)

    return '\n\n'.join(iter_cmd()) + '\n'

@y.defer_constructor
@y.singleton
def original_funcs():
    res = []

    y.gd_callback('orig functions')(res.append)

    return res


def fix_user_data(iter):
    for f in iter:
        f = y.deep_copy(f)

        ss = f.get('support', [])

        if ss and 'darwin' not in ss:
            continue

        yield f


@y.singleton
def iter_all_user_generators():
    res = []

    @y.gd_callback('new functions generator')
    def cb(data):
        res.extend(fix_user_data([data]))

    return res


@y.singleton
def build_env_channel():
    return y.GEN_DATA_LOOP.write_channel('build env', 'common')

        
@y.singleton
def send_all_plugins_to_queue():
    ch = y.GEN_DATA_LOOP.write_channel('new plugin', 'file_data')

    for el in y.file_data:
        if el['name'].startswith('pl/'):
            ch(y.deep_copy(el))

    #TODO
    #y.gen_all_texts()
    y.make_perm()

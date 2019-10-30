@y.cached()
def toybox0(info, deps, codec):
    name = 'toybox-' + info['info']['host']['arch']
    ver = '0.8.1'

    return y.to_v2({
        'code': 'mkdir -p $IDIR/bin && cd $IDIR/bin && $(FETCH_URL_FILE) && cp %s toybox && chmod +x toybox' % name,
        'src': 'http://www.landley.net/toybox/downloads/binaries/' + ver + '/' + name,
        'version': ver,
        'deps': deps,
        'codec': codec,
    }, info)


y.register_func_generator({
    'support': ['linux'],
    'tier': -1,
    'kind': ['core', 'dev', 'tool'],
    'template': """
@y.options({options})
def {name}{num}(info):
    return toybox0(info, {deps}, '{codec}')
""",
})

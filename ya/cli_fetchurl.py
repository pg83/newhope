@y.main_entry_point
async def cli_cmd_fetch(args):
    if len(args) > 1:
        url = args[0]
        path = args[1]
        root = y.os.path.dirname(path)
        name = y.os.path.basename(path)
    else:
        url = args[0]
        root = './'
        name = y.os.path.basename(url)

    y.fetch_http(root, url, name=name, untar=False)

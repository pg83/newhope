@y.main_entry_point
async def cli_db_set(args):
    assert len(args) == 2

    with y.open_pdb() as db:
        db.kv[args[0]] = args[1]


@y.main_entry_point
async def cli_db_get(arg):
    assert len(arg) == 1

    with y.open_pdb() as db:
        print(db.kv.get(arg[0], '{br}no such key{}'))


@y.main_entry_point
async def cli_db_dump(args):
    with y.open_pdb() as db:
        print(y.json.dumps(db.db, indent=4, sort_keys=True))

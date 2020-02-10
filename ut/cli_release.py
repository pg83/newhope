@y.verbose_entry_point
def cli_cmd_release(args):
   data = {'file_data': y.globals.file_data, 'script_path': y.globals.script_path, 'compile_cache': y.globals.cache}
   data = y.marshal.dumps(data)
   data = y.lzma.compress(data)
   data = y.base64.b64encode(data)

   code = 'import marshal; import lzma; import base64; fd = marshal.loads(lzma.decompress(base64.b64decode("{data}"))); file_data = fd["file_data"];'
   code = code.replace('{data}', data.decode('utf-8'))

   for x in y.globals.file_data:
      if x['path'].endswith('cli'):
         break

   print(x['data'].replace('#REPLACEME', code))

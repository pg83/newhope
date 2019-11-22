@y.main_entry_point
def cli_release(args):
   data = {'file_data': y.file_data, 'data': y.stagea.__ytext__}
   data = y.marshal.dumps(data)
   data = y.zlib.compress(data)
   data = y.base64.b64encode(data)

   code = 'import marshal; import zlib; import base64; fd = marshal.loads(zlib.decompress(base64.b64decode("{data}"))); file_data = fd["file_data"]; data = fd["data"]'
   code = code.replace('{data}', data)

   for x in y.file_data:
      if x['path'] == 'cli':
         break

   print x['data'].replace('#REPLACEME', code)

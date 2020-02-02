import marshal
import time
import urllib.request as urllib2


while True:
    data = marshal.loads(urllib2.urlopen('http://138.68.80.104:81/worker').read())

    if 'state' in data:
        time.sleep(0.1)
        print(data)
    else:
        urllib2.urlopen('http://138.68.80.104:81/' + data['id'], data=b'qqqqq').read()

import marshal
import time
import urllib.request as urllib2


def step():
    data = marshal.loads(urllib2.urlopen('http://138.68.80.104:81/worker').read())

    if 'state' in data:
        time.sleep(0.2)
    else:
        print(data)

        with open('/media/storage/pkg_repo/' + data['req'], 'rb') as f:
            dt = f.read()

        print(len(dt))
    
        urllib2.urlopen('http://138.68.80.104:81/' + data['id'], data=dt).read()


while True:
    try:
        step()
    except Exception as e:
        print(e)
        time.sleep(0.2)

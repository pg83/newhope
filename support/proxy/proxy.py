from bottle import route, run, post, request, Bottle

import queue
import json
import random
import collections
import marshal
import threading


app1 = Bottle()
app2 = Bottle()


def gen_id():
    return str(int(random.random() * 100000000000000000))


requests = collections.deque()
in_proc = {}


@app1.route('/worker')
def worker():
    resp = {}

    try:
        req, qq, my_id = requests.popleft()
    except IndexError:
        resp = {'state': 'no work'}

    if not resp:
        in_proc[my_id] = qq
        resp = {'req': req, 'id': my_id}

    return marshal.dumps(resp)


@app2.route('/')
def main():
    return 'fetch for packages'


@app2.route('/<path>')
def fetch(path):
    qq = queue.Queue()
    my_id = gen_id()
    requests.append((path, qq, my_id))

    return qq.get()


@app1.post('/<my_id>')
def on_ready(my_id):
    qq = in_proc.pop(my_id)
    qq.put(request.body.read())


f1 = lambda: run(app2, host='0.0.0.0', port=80, debug=True)
f2 = lambda: run(app1, host='0.0.0.0', port=81, debug=True)


threading.Thread(target=f1).start()
threading.Thread(target=f2).start()

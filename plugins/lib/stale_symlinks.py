#!/bin/upm python

import os
import sys
import time


for prefix in ('/etc/runit', '/etc/profile.d'):
    for x in os.listdir(prefix):
        p = os.path.join(prefix, x)

        if os.path.islink(p):
            where = p + '/' + os.readlink(p)

            if not os.path.exists(where):
                os.unlink(p)


time.sleep(5)

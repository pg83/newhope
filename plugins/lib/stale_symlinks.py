#!/bin/upm python

import os
import sys
import time


for prefix in ('/etc/runit', '/etc/profile.d'):
    for x in os.listdir(prefix):
        p = os.path.join(prefix, x)

        if os.path.islink(p):
            l = os.readlink(p)
    
            if os.path.isabs(l):
                where = l
            else:
                where = prefix + '/' + l

            if not os.path.exists(where):
                os.unlink(p)


time.sleep(5)

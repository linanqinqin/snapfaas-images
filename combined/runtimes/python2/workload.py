#!/usr/bin/env python2

import sys
import imp
import struct
import json
from subprocess import call, Popen
import multiprocessing as mp
import time

with open('/dev/ttyS1', 'r') as tty, open('/dev/ttyS1', 'w') as out:
    call(['outl', '123', '0x3f0'], executable="/usr/bin/outl")

    #call(["mount", "-r", "/dev/vdb", "/srv"], executable="/bin/mount")

    sys.path.append('/srv/package')
    app = imp.load_source('app', '/srv/workload')

    # signal firerunner we are ready
    #call(['outl', '126', '0x3f0'], executable="/usr/bin/outl")
    #call(['outl', '126', '0x3f0'], executable="/usr/bin/outl")

    # for function diff snapshot
    for i in range(1, mp.cpu_count()):
        Popen('taskset -c %d outl 124 0x3f0'%(i), shell=True)
    call('taskset -c 0 outl 124 0x3f0', shell=True)

    call(['outl', '126', '0x3f0'], executable="/usr/bin/outl")
    while True:
        request = json.loads(tty.readline())
        #t0 = time.clock()

        response = app.handle(request)
        #t1 = time.clock()
        #response['runtime'] = (t1-t0) * 1000

        responseJson = json.dumps(response)

        out.write(struct.pack(">I", len(responseJson)))
        out.write(bytes(responseJson))
        out.flush()


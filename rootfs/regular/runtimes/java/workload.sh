#!/usr/bin/env bash

/usr/bin/setup-eth0.sh
/usr/bin/ioctl

java -cp "/bin/RuntimeWorkload.jar:/srv/libworkload.jar" RuntimeWorkload

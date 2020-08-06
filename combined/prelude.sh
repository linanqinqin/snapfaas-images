apk add openrc util-linux

cp /common/outl /usr/bin/outl
cp /common/setup-eth0.sh /usr/bin/setup-eth0.sh
cp /common/ioctl /usr/bin/ioctl

## Create start script for that mounts the appfs and invokes whatever binary is in /srv/workload
printf '#!/bin/sh\n
exec /bin/runtime-workload\n' > /bin/workload
chmod +x /bin/workload

## Have the start script invoked by openrc/init
printf '#!/sbin/openrc-run\n
command="/bin/workload"\n' > /etc/init.d/serverless-workload
chmod +x /etc/init.d/serverless-workload
rc-update add serverless-workload default

## Add /dev and /proc file systems to openrc's boot
rc-update add devfs boot
rc-update add procfs boot

#!/usr/bin/env python3

import sys
import importlib.util
import importlib.machinery
import os
import struct
import json
from subprocess import run, Popen
import time
import socket

# vsock to communicate with the host
VSOCKPORT = 1234
sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
hostaddr = (socket.VMADDR_CID_HOST, VSOCKPORT)

importlib.machinery.SOURCE_SUFFIXES.append('')
spec = importlib.util.spec_from_file_location("app", "/srv/workload")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

sock.connect(hostaddr)
while True:
    data = sock.recv(4, socket.MSG_WAITALL)
    res = struct.unpack(">I", data)
    requestJson = sock.recv(res[0], socket.MSG_WAITALL).decode("utf-8")
    request = json.loads(requestJson)

    response = app.handle(request)

    responseJson = json.dumps(response)
    sock.sendall(struct.pack(">I", len(responseJson)))
    sock.sendall(bytes(responseJson, "utf-8"))

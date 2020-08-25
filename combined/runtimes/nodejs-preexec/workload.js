const vsock = require("vsock");
const { execSync, exec } = require("child_process");
const cpu_count = require("os").cpus().length;

(async function() {
  module.paths.push("/srv/node_modules");
  const app = require("/srv/workload");
  
  await app.handle({});

  for (var i = 1; i < cpu_count; i++) {
      exec(`taskset -c ${i} outl 124 0x3f0`);
  }
  execSync('taskset -c 0 outl 124 0x3f0')
  
  const sock_conn = vsock.connect(2, 1234);

  while (true) {
    const req = await vsock.readRequest(sock_conn);

    const hrstart = process.hrtime();
    const resp = await app.handle(req);
    const hrend = process.hrtime(hrstart)
    resp.runtime_sec = hrend[0];
    resp.runtime_ms = hrend[1] / 1000000;
    await vsock.writeResponse(sock_conn, resp);
  }
})();

import sys
import os

import rpyc
from rpyc.utils.zerodeploy import DeployedServer as _DeployedServer
from rpyc.lib.compat import BYTES_LITERAL
from rpyc.utils.zerodeploy import  SERVER_SCRIPT
import socket

from plumbum import SshMachine
from plumbum import local, ProcessExecutionError, CommandNotFound
from plumbum.path import copy

# PATCH
class RedPitayaDeployedServer(_DeployedServer):
    def __init__(self, remote_machine):
        self.remote_machine = remote_machine
        
        rpyc_root = local.path(rpyc.__file__).up()
        self._tmpdir_ctx = remote_machine.tempdir()
        tmp = self._tmpdir_ctx.__enter__()
        self.tmp = tmp
        copy(rpyc_root, tmp / "rpyc")
        
        self.copy_other_files(tmp)
        script = (tmp / "deployed-rpyc.py")
        server_class = "rpyc.utils.server.ThreadedServer"
        modname, clsname = server_class.rsplit(".", 1)
        script.write(SERVER_SCRIPT.replace("$MODULE$", modname).replace("$SERVER$", clsname).replace("$EXTRA_SETUP$", self.extra_setup))
        cmd = remote_machine['/opt/usr/bin/python']
        self.proc = cmd.popen(script, new_session = True)
        line = ""
        try:
            line = self.proc.stdout.readline()
            self.remote_port = int(line.strip())
        except Exception:
            try:
                self.proc.terminate()
            except Exception:
                pass
            stdout, stderr = self.proc.communicate()
            raise ProcessExecutionError(self.proc.argv, self.proc.returncode, BYTES_LITERAL(line) + stdout, stderr)
        
        if hasattr(remote_machine, "connect_sock"):
            # Paramiko: use connect_sock() instead of tunnels
            self.local_port = None
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("localhost", 0))
            self.local_port = s.getsockname()[1]
            s.close()
            self.tun = remote_machine.tunnel(self.local_port, self.remote_port)

    def copy_other_files(self, tmp):
        pyredpitaya_root = local.path(__file__).up().up()
        copy(pyredpitaya_root/'monitor/libmonitor.so', tmp / 'libmonitor.so')
        copy(pyredpitaya_root/'PyRedPitayaTest.py', tmp / 'PyRedPitayaTest.py')
        copy(pyredpitaya_root/'PyRedPitaya', tmp / 'PyRedPitaya')

    def load_hdl(self, bitfile):
        print bitfile
        name = os.path.basename(bitfile)
        copy(local.path(bitfile), self.remote_machine.path('/tmp')/ name)
        load = ( self.remote_machine['/bin/cat']['/tmp/{name}'.format(name=name)] > '/dev/xdevcfg')
        print load
        self.remote_machine.popen(str(load)).wait()


    extra_setup = """
import PyRedPitayaTest
PyRedPitayaTest.libmonitor_file = './libmonitor.so'
    """


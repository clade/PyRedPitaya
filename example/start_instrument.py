#!/usr/bin/python

import os
on_board = 'armv7l' in os.uname()[-1]


import argparse
parser = argparse.ArgumentParser()

if on_board:
    from PyRedPitaya.board import RedPitaya
    redpitaya = RedPitaya()
else:
    from plumbum import SshMachine
    from PyRedPitaya.pc import RedPitaya
    from PyRedPitaya.server import RedPitayaDeployedServer
    parser.add_argument("--hostname", default='192.168.1.100')
    parser.add_argument("--user", default='root')
    parser.add_argument("--password", default='root')
    args = parser.parse_args()
    mach = SshMachine(args.hostname, user=args.user, password=args.password)
    server = RedPitayaDeployedServer(mach)
    conn = server.classic_connect()
    redpitaya = RedPitaya(conn)

header = """IPython shell for interacting with the board

Use for exemple redpitaya.ams.temp
"""

try:
    import IPython as ipython
except ImportError:
    import ipython
ipython.embed(header=header)

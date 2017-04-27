#!/usr/bin/env python

import sys
import os
import argparse

from config import MACHINES

def list_machines():
    print("Available machines:")
    if len(MACHINES) == 0:
        print("None")
    else:
        for k in MACHINES:
            print("  - " + k)

parser = argparse.ArgumentParser(description="Connect !")
parser.add_argument("machine", help="machine to connect to")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
else:
    args = parser.parse_args()
    machine = args.machine

    if machine == "list":
        list_machines()
        sys.exit(0);

    if machine in MACHINES:
        machine_conf = MACHINES[machine]
        command = "ssh {user}@{ip} -p {port} -i {identity}".format(
            user=machine_conf["user"],
            ip=machine_conf["ip"],
            port=machine_conf["port"],
            identity=machine_conf["identity"]
        )

        os.system(command)
        print("All done !")
    else:
        print("Machine `{0}` is unknown".format(machine))
        sys.exit(1)

#!/usr/bin/env python

"""pSSH tool."""

import sys
import os
import argparse

from config import MACHINES


def list_machines():
    """List machines."""
    print("Available machines:")
    if len(MACHINES) == 0:
        print("None")
    else:
        for k in MACHINES:
            print("  - " + k)


def main():
    """Main."""
    parser = argparse.ArgumentParser(description="pssh")

    subps = parser.add_subparsers(dest="command", metavar="")
    subps.add_parser("list", help="list machines")

    connect = subps.add_parser("connect", help="connect to a machine")
    connect.add_argument("machine", help="machine to connect to")
    connect.add_argument("-t", "--tmux", action="store_true", help="start tmux")
    connect.add_argument("-u", "--user", help="specify user")

    push = subps.add_parser("push", help="push to a machine")
    push.add_argument("machine", help="machine to connect to")
    push.add_argument("source", help="source")
    push.add_argument("dest", help="dest")

    pull = subps.add_parser("pull", help="pull from a machine")
    pull.add_argument("machine", help="machine to connect to")
    pull.add_argument("source", help="source")
    pull.add_argument("dest", help="dest")

    show = subps.add_parser("show", help="show a machine conf")
    show.add_argument("machine", help="machine name")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    else:
        args = parser.parse_args()

        if args.command == "list":
            list_machines()
            sys.exit(0)

        machine = args.machine
        if machine not in MACHINES:
            print("Machine `{0}` does not exist".format(machine))
            sys.exit(1)

        machine_conf = MACHINES[machine]

        if args.command == "connect":
            user = args.user if args.user else machine_conf["user"]
            command = "ssh {user}@{ip} -p {port} -i {identity}".format(
                user=user,
                ip=machine_conf["ip"],
                port=machine_conf["port"],
                identity=machine_conf["identity"]
            )

            if args.tmux:
                command += " -t 'tmux attach || tmux new'"
            os.system(command)

        elif args.command == "show":
            import pprint
            pprint.pprint(machine_conf)

        elif args.command == "push":
            command = "scp -i {identity} -P {port} {s_path} {user}@{ip}:{d_path}".format(
                user=machine_conf["user"],
                ip=machine_conf["ip"],
                port=machine_conf["port"],
                s_path=args.source,
                d_path=args.dest,
                identity=machine_conf["identity"]
            )
            os.system(command)

        elif args.command == "pull":
            command = "scp -i {identity} -P {port} {user}@{ip}:{s_path} {d_path}".format(
                user=machine_conf["user"],
                ip=machine_conf["ip"],
                port=machine_conf["port"],
                s_path=args.source,
                d_path=args.dest,
                identity=machine_conf["identity"]
            )
            os.system(command)


if __name__ == "__main__":
    main()

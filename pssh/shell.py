"""pssh shell."""

import argparse
import sys
import os

from pssh.version import __version__
from pssh.wrapper import list_machines, get_machine_configuration


def entry_point():
    """Entry point."""
    parser = argparse.ArgumentParser(description="pssh v.{0}".format(__version__))
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument("-f", "--file", nargs="?", help="configuration file", default="config.yml")

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

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    call_handle_fn(parser.parse_args())


def call_handle_fn(args):
    """
    Call handle function.

    :param args     Argument (Namespace)
    """
    command_name = args.command
    try:
        handle_fn = globals()["_handle_{0}".format(command_name)]
        handle_fn(args)
    except KeyError:
        raise RuntimeError("Unsupported command {0}".format(command_name))


def _handle_connect(args):
    machine_conf = get_machine_configuration(args.file, args.machine)
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


def _handle_push(args):
    machine_conf = get_machine_configuration(args.file, args.machine)

    command = "scp -i {identity} -P {port} {s_path} {user}@{ip}:{d_path}".format(
        user=machine_conf["user"],
        ip=machine_conf["ip"],
        port=machine_conf["port"],
        s_path=args.source,
        d_path=args.dest,
        identity=machine_conf["identity"]
    )
    os.system(command)


def _handle_pull(args):
    machine_conf = get_machine_configuration(args.file, args.machine)

    command = "scp -i {identity} -P {port} {user}@{ip}:{s_path} {d_path}".format(
        user=machine_conf["user"],
        ip=machine_conf["ip"],
        port=machine_conf["port"],
        s_path=args.source,
        d_path=args.dest,
        identity=machine_conf["identity"]
    )
    os.system(command)


def _handle_show(args):
    configuration = get_machine_configuration(args.file, args.machine)
    print("Configuration for `{0}`:".format(args.machine))
    print("  IP: {0}".format(configuration.get("ip", "None")))
    print("  Port: {0}".format(configuration.get("port", "None")))
    print("  User: {0}".format(configuration.get("user", "None")))
    print("  Identity: {0}".format(configuration.get("identity", "None")))


def _handle_list(args):
    machines = list_machines(args.file)
    for machine in machines:
        print("> {0}".format(machine))

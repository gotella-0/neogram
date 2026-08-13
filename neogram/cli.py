#!/usr/bin/python3

#########################################################
# Copyright © 2022 Nikita Smirnov. All rights reserved. #
#########################################################

import argparse
import sys

from .imports import create_project, run_project, remove_project, Color


def build_parser():
    parser = argparse.ArgumentParser(
        prog="neogram",
        description="Low-code config-driven Telegram bot framework",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("create", help="Create a new bot project").add_argument("name_project")

    subparsers.add_parser("run", help="Run a bot project").add_argument("name_project")

    subparsers.add_parser("remove", help="Remove a bot project").add_argument("name_project")

    return parser


def check_cmd_args():
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    name_project = args.name_project

    if args.command == "create":
        print(f"{Color.Yellow}[*]{Color.END} Start Creating project...")
        create_project(name_project)
    elif args.command == "run":
        print(f"{Color.Yellow}[*]{Color.END} Running project...")
        run_project(name_project)
    elif args.command == "remove":
        print(f"{Color.Yellow}[*]{Color.END} Preparing to remove a project...")
        remove_project(name_project)
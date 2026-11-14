#!/usr/bin/env python3
# Gufw - https://costales.github.io/projects/gufw/
# Copyright (C) 2008-2025 Marcos Alvarez Costales https://costales.github.io
#
# Gufw is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Gufw is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gufw; if not, see http://www.gnu.org/licenses for more
# information.

import os
import sys
import argparse
import configparser
from gufw.model.frontend import Frontend

def _get_parser():
    parser = argparse.ArgumentParser(
        prog="gufw",
        description="Run without arguments to launch GUI, or use arguments to manage via CLI."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--list", action="store_true", help="List all available Gufw profiles")
    group.add_argument("-s", "--status", action="store_true", help="Show active profile, policies, and rules")
    group.add_argument("-p", "--profile", metavar="NAME", help="Switch to and apply a Gufw profile")
    group.add_argument("-r", "--reload", action="store_true", help="Re-apply the currently active profile")
    return parser

def print_help():
    _get_parser().print_help()

def _apply_profile(fw, target):
    profile_path = f"/etc/gufw/{target}.profile"
    if target not in fw.get_all_profiles():
        sys.exit(f"Error: File '{profile_path}' not found.")

    cfg = configparser.ConfigParser()
    cfg.read(profile_path)
    basic = cfg["fwBasic"]

    fw.set_profile(target)

    if "incoming" in basic:
        fw.set_policy("incoming", basic["incoming"])
    if "outgoing" in basic:
        fw.set_policy("outgoing", basic["outgoing"])
    if "routed" in basic and basic["routed"] != "disabled":
        fw.set_policy("routed", basic["routed"])
    if "status" in basic:
        fw.set_status(basic["status"] == "enabled")

def run_cli():
    parser = _get_parser()
    args = parser.parse_args()

    if os.geteuid() != 0:
        sys.exit("Error: CLI operations require root privileges (use sudo).")

    fw = Frontend()

    if args.list:
        current = fw.get_profile()
        for p in fw.get_all_profiles():
            marker = "*" if p == current else " "
            print(f" {marker} {p}")

    elif args.status:
        print(f"Active Profile:   {fw.get_profile()}")
        print(f"Firewall Status:  {'Enabled' if fw.get_status() else 'Disabled'}")
        print(f"Incoming Policy:  {fw.get_policy('incoming').capitalize()}")
        print(f"Outgoing Policy:  {fw.get_policy('outgoing').capitalize()}")
        print(f"Routed Policy:    {fw.get_policy('routed').capitalize()}")
        if fw.get_rules() == []:
            print(f"\nActive Rules:  None\n")
        else:
            print(f"\nActive Rules:\n")
            for idx, rule in enumerate(fw.get_rules(), start=1):
                print(f"  [{idx}] {rule}\n")

    elif args.profile:
        _apply_profile(fw, args.profile)
        print(f"Switched to profile '{args.profile}' and updated UFW.")

    elif args.reload:
        current = fw.get_profile()
        _apply_profile(fw, current)
        print(f"Reloaded profile '{current}' into UFW.")

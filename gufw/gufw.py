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

import sys


if __name__ == '__main__':
    # Intercept CLI flags before importing GTK/GUI modules
    if len(sys.argv) > 1 and any(arg.startswith('-') for arg in sys.argv[1:]):
        from gufw.cli import run_cli
        run_cli()
        sys.exit(0)


    # Check if a graphical display (X11 or Wayland) is available before starting the UI
    import gi
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gdk

    if Gdk.Display.get_default() is None:
        print("\nError: No graphical display detected (X11 or Wayland).\n", file=sys.stderr)
        from gufw.cli import print_help
        print_help()
        sys.exit(1)


    # Otherwise, start the GTK GUI normally
    from gufw.controller import Controller
    from gufw.instance   import Instance
    from gufw.view.gufw  import Gufw


    app_instance = Instance()
    controler = Controller()
    gufw = Gufw(controler.get_frontend())
    app_instance.exit_app()

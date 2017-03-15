#!/usr/bin/env python3
#
# Copyright (c) 2017 Aboud Zakaria (https://github.com/aboudzakaria/stickies)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# Authored by: Aboud Zakaria <aboud.zakaria@gmail.com>
#
# main application
#

import gi, sys, StickyManager
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import signal


class StickyApplication(Gtk.Application):
	
	def __init__(self):
		Gtk.Application.__init__(self)


	def do_activate(self):
		# restore saved stickies and show them
		StickyManager.restore_stickies(self)
		for st in StickyManager.stickylist:
			st.connect("delete-event", self.window_close)
			st.btnNew.connect("clicked", self.window_new)
			st.show_all()

	
	def do_startup(self):
		Gtk.Application.do_startup(self)


	def window_close(self, sticky, event):
		StickyManager.close_sticky(sticky)
		if len(StickyManager.stickylist) == 0:
			self.quit() # quit app when all stickies are closed


	def window_new(self, button):
		st = StickyManager.create_sticky(self)
		st.connect("delete-event", self.window_close)
		st.btnNew.connect("clicked", self.window_new)
		st.show_all()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = StickyApplication()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)

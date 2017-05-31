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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

import sys, signal, StickyManager

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

		# periodically autosave all stickies
		GLib.timeout_add_seconds(10, self.autosaver);

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

	def autosaver(self):
		for st in StickyManager.stickylist:
			if (st.modified):
				StickyManager.save_sticky(st)
				st.modified = False
		return True

	def exit_gracefully(self):
		for st in StickyManager.stickylist:
			StickyManager.close_sticky(st)
		self.quit()


# handle singals gracefully
def SignalHandler(app):
	def signal_action(signal):
		if signal is 1: print("Caught signal SIGHUP(1)")
		elif signal is 2: print("Caught signal SIGINT(2)")
		elif signal is 15: print("Caught signal SIGTERM(15)")
		app.exit_gracefully()

	def handler(*args):
		# Activate GLib signal handler
		signal_action(args[0])

	def idle_handler(*args):
		# Activate python signal handler
		GLib.idle_add(signal_action, priority=GLib.PRIORITY_HIGH)

	def install_glib_handler(sig):
		unix_signal_add = None
		if hasattr(GLib, "unix_signal_add"):
			unix_signal_add = GLib.unix_signal_add
		elif hasattr(GLib, "unix_signal_add_full"):
			unix_signal_add = GLib.unix_signal_add_full
		if unix_signal_add:
			# Register GLib signal handler
			unix_signal_add(GLib.PRIORITY_HIGH, sig, handler, sig)
		else:
			print("WARNING: Can't install GLib signal handler, too old gi.")

	SIGS = [getattr(signal, s, None) for s in "SIGINT SIGTERM SIGHUP".split()]
	for sig in filter(None, SIGS):
		# Register Python signal handler
		signal.signal(sig, idle_handler)
		GLib.idle_add(install_glib_handler, sig, priority=GLib.PRIORITY_HIGH)


if __name__ == "__main__":
	app = StickyApplication()
	SignalHandler(app)
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)


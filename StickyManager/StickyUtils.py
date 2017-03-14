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
# StickyUtils management utilities
#

from .StickyWindow import StickyWindow
from .StickyDTO import StickyDTO

from uuid import uuid4
import os, pickle


# a list of StickyWindow
stickylist = []

#define stickies home directory
sticky_home = os.path.join(os.path.expanduser("~"), ".stickies")
if not os.path.exists(sticky_home):
	os.makedirs(sticky_home)


''' create a new sticky. '''
def create_sticky(app):
	sticky = StickyWindow(app, genid())
	stickylist.append(sticky)
	return sticky


''' save a filled sticky, remove an empty sticky. '''
def close_sticky(sticky):
	dto = sticky.toDTO()
	name = dto.id + ".pkl"
	path = os.path.join(sticky_home, name)
	stickylist.remove(sticky)
	if (dto.text != ""):
		f = open(path, "wb")
		pickle.dump(dto, f)
	elif os.path.isfile(path):
		os.remove(path)


''' restore saved stickies. '''
def restore_stickies(app):
	for name in os.listdir(sticky_home):
		path = os.path.join(sticky_home, name)
		if os.path.isfile(path):
			if path.endswith(".pkl"):
				try:
					f = open(path, "rb")
					dto = pickle.load(f)
					sticky = StickyWindow.fromDTO(dto, app)
					stickylist.append(sticky)
					sticky.move(dto.x, dto.y) # force moving!
					sticky.move(dto.x, dto.y) # force moving again!
				except(Exception) as ex:
					pass # ignore and continue loop
	if (len(stickylist) == 0): # no saved stickies?
		create_sticky(app) # create a new one


''' generate an identifier. '''
def genid():
	return str(uuid4())[:8]
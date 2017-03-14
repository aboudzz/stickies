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
# StickyDTO class
#

''' a small class that holds the data to be pickled. '''
class StickyDTO:

	def __init__(self, id, x, y, w, h, text):
		# identifier
		self.id = id
		# position attrs
		self.x, self.y = x, y
		# size attrs
		self.w, self.h = w, h
		# text
		self.text = text
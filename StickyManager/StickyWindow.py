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
# StickyWindow class
#

from .StickyDTO import StickyDTO

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango

''' the main sticky note window. '''
class StickyWindow(Gtk.Window):

	def __init__(self, app, id, x=0, y=0, w=400, h=400, text=""):
		Gtk.Window.__init__(self, application=app)
		
		# header
		lblNew = Gtk.Label()
		lblNew.set_markup("\u2795") # + sign
		self.btnNew = Gtk.ToolButton()
		self.btnNew.set_tooltip_text("new sticky")
		self.btnNew.set_label_widget(lblNew)
		lblRemove = Gtk.Label()
		lblRemove.set_markup("\u2718") # x sign
		self.btnRemove = Gtk.ToolButton()
		self.btnRemove.set_tooltip_text("remove sticky")
		self.btnRemove.set_label_widget(lblRemove)
		self.btnRemove.connect("clicked", self.remove_clicked)
		self.headerbar = Gtk.HeaderBar()
		self.headerbar.pack_start(self.btnRemove)
		self.headerbar.pack_end(self.btnNew)
		self.set_titlebar(self.headerbar)

		# content
		self.txtBuffer = Gtk.TextBuffer()
		self.txtBuffer.set_text(text)
		self.txtView = Gtk.TextView(buffer = self.txtBuffer)
		self.txtView.set_wrap_mode(Gtk.WrapMode.WORD) # wrap text on width
		self.txtView.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 0.6, 0.7)) # light yellow
		self.txtView.override_background_color(Gtk.StateFlags.SELECTED, Gdk.RGBA(0.5, 0.5, 0.5, 0.7)) # dark gray
		self.txtView.modify_font(Pango.FontDescription("Comic Sans MS 14"))
		self.add(self.txtView)
		self.txtBuffer.connect("changed", self.text_changed)
		self.text_changed(self.txtBuffer) # sets the window title

		self.id = id
		if x == 0 | y == 0:
			self.set_position(Gtk.WindowPosition.MOUSE) # default on mouse position
		else:
			self.move(x, y)

		self.resize(w, h)


	''' text buffer changed event handler. '''
	def text_changed(self, buffer):
		text = self.get_text();
		title = text.split('\n', 1)[0] # take first line
		if len(title) > 17:
			title = title[:15] + "..." # take 15 chars
		if title == "":
			self.set_title("Sticky")
		else:
			self.set_title(title)


	''' get the whole text from buffer. '''
	def get_text(self):
		startiter = self.txtBuffer.get_start_iter()
		enditer = self.txtBuffer.get_end_iter()
		return self.txtBuffer.get_text(startiter, enditer, include_hidden_chars = True)


	''' remove button clicked event handler. '''
	def remove_clicked(self, button):
		if self.get_text() != "":
			# prompt for deleting
			dialog = ConfirmDialog(self, "Are you sure you want to delete sticky?")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				self.txtBuffer.set_text("") # act like remove on close
				dialog.close()
				self.close()
			elif response == Gtk.ResponseType.CANCEL:
				dialog.close()
		else:
			self.close()


	''' convert to DTO object. '''
	def toDTO(self):
		dto = StickyDTO(id = self.id,
						x = self.get_position()[0],
						y = self.get_position()[1],
						w = self.get_size()[0],
						h = self.get_size()[1],
						text = self.get_text())
		return dto


	''' creates a stickyWindow from DTO object. '''
	@staticmethod
	def fromDTO(dto, app):
		return StickyWindow(app, dto.id,
							x = dto.x, y = dto.y,
							w = dto.w, h = dto.h,
							text = dto.text)




''' Yes/No confirmation Dialog. '''
class ConfirmDialog(Gtk.Dialog):
	
	def __init__(self, parent, message=""):
		Gtk.Dialog.__init__(self, "Confirmation", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_resizable(False)
		self.get_content_area().add(Gtk.Label(message))
		self.show_all()

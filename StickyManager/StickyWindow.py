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
		rgbaColor = Gdk.RGBA(1.0, 1.0, 0.6, 0.7) # light yellow
		self.id = id

		# header
		self.lblTitle = Gtk.Label()
		self.lblTitle.set_text("Sticky")
		self.lblTitle.modify_font(Pango.FontDescription("Open Sans Bold 10"))
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

		# content
		self.txtBuffer = Gtk.TextBuffer()
		self.txtBuffer.set_text(text)
		self.txtView = Gtk.TextView(buffer = self.txtBuffer)
		self.txtView.set_wrap_mode(Gtk.WrapMode.WORD) # wrap text on width
		self.txtView.set_border_width(10) # apply some hardcoded padding
		self.txtView.override_background_color(Gtk.StateFlags.NORMAL, rgbaColor)
		self.txtView.override_background_color(Gtk.StateFlags.SELECTED, Gdk.RGBA(0.5, 0.5, 0.5, 0.7)) # dark gray
		self.txtView.modify_font(Pango.FontDescription("Open Sans 14"))
		self.txtBuffer.connect("changed", self.text_changed)
		self.text_changed(self.txtBuffer) # sets the window title

		# layout
		hbox = Gtk.HBox()
		hbox.set_size_request(-1, 33)
		hbox.modify_bg(Gtk.StateFlags.NORMAL, rgbaColor.to_color())
		hbox.pack_start(self.btnRemove, False, False, 0)
		hbox.pack_start(self.lblTitle, True, True, 0)
		hbox.pack_end(self.btnNew, False, False, 0)
		ebox = Gtk.EventBox()
		ebox.add(self.txtView)
		ebox.modify_bg(Gtk.StateFlags.NORMAL, rgbaColor.to_color())
		vbox = Gtk.VBox()
		vbox.pack_start(hbox, False, False, 0)
		vbox.pack_end(ebox, True, True, 0)
		junkiebox = Gtk.Box()

		self.add(vbox)
		self.set_titlebar(junkiebox) # hiding titlebar hack
		self.set_focus_child(self.txtView)
		self.resize(w, h)
		self.set_position(Gtk.WindowPosition.MOUSE) # default on mouse position
		if (x, y) != (0, 0): 
			self.move(x, y)
		else: 
			# fix position
			posx = self.get_position()[0];
			posy = self.get_position()[1];
			self.move(posx, posy + 200);

		# sticky dragging event signals
		self.pressed = False
		self.connect("button-press-event", self.button_pressed)
		self.connect("button-release-event", self.button_released)
		self.connect("motion-notify-event", self.motion_notified)


	''' mouse button clicking event handler. '''
	def button_pressed(self, ev, dat):
		if (dat.x > 40 and dat.y > 40): # not in resizing position
			if dat.button == 1: # mouse primary
				self.pressed = True
				# record clicking position
				self.x_pressed = dat.x
				self.y_pressed = dat.y


	''' mouse button releasing event handler. '''
	def button_released(self, ev, dat):
		if dat.button == 1: # mouse primary
			self.pressed = False


	''' mouse movement event handler '''
	def motion_notified(self, ev, dat):
		if (self.pressed):
			self.move(dat.x_root - self.x_pressed,
			 		  dat.y_root - self.y_pressed)


	''' text buffer changed event handler. '''
	def text_changed(self, buffer):
		text = self.get_text();
		title = text.split('\n', 1)[0] # take first line
		if len(title) > 17:
			title = title[:15] + "..." # take 15 chars
		if title == "":
			self.set_title("Sticky")
			self.lblTitle.set_text("Sticky")
		else:
			self.set_title(title)
			self.lblTitle.set_text(title)


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

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
# Authored by: Mirko Brombin <brombinmirko@gmail.com>
#
# setup script
#

import glob, os 
from distutils.core import setup

inst_path = '/usr/share/com.github.aboudzakaria.stickies'

install_data = [('/usr/share/metainfo', ['data/com.github.aboudzakaria.stickies.appdata.xml']),
                ('/usr/share/applications', ['data/com.github.aboudzakaria.stickies.desktop']),
                ('/usr/share/icons/hicolor/128x128/apps',['data/com.github.aboudzakaria.stickies.png']),
                (inst_path+'/stickies/StickyManager',['stickies/StickyManager/StickyDTO.py']),
                (inst_path+'/stickies/StickyManager',['stickies/StickyManager/StickyUtils.py']),
                (inst_path+'/stickies/StickyManager',['stickies/StickyManager/StickyWindow.py']),
                (inst_path+'/stickies/StickyManager',['stickies/StickyManager/__init__.py']),
                (inst_path+'/stickies',['stickies/main.py']),
                (inst_path+'/stickies',['stickies/__init__.py']),]

setup(  name='stickies',
        version='0.1.6',
        author='Aboud Zakaria',
        description='Neat sticky notes app for elementary OS',
        url='https://github.com/aboudzakaria/stickies',
        license='GNU GPL2',
        scripts=['com.github.aboudzakaria.stickies'],
        packages=['stickies'],
        data_files=install_data)

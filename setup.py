#!/usr/bin/python3

import glob, os 
from distutils.core import setup

inst_path = '/usr/share/com.github.aboudzakaria.stickies/stickies'

install_data = [('/usr/share/metainfo', ['data/com.github.aboudzakaria.stickies.appdata.xml']),
                ('/usr/share/applications', ['data/com.github.aboudzakaria.stickies.desktop']),
                ('/usr/share/icons/hicolor/128x128/apps',['data/com.github.aboudzakaria.stickies.png']),
                (inst_path+'/StickyManager',['stickies/StickyManager/StickyDTO.py']),
                (inst_path+'/StickyManager',['stickies/StickyManager/StickyUtils.py']),
                (inst_path+'/StickyManager',['stickies/StickyManager/StickyWindow.py']),
                (inst_path+'/StickyManager',['stickies/StickyManager/__init__.py']),
                (inst_path,['stickies/main.py']),
                (inst_path,['stickies/__init__.py']),]

setup(  name='Stickies',
        version='0.0.3',
        author='Aboud Zakaria',
        description='Neat sticky notes app',
        url='https://github.com/aboudzakaria/stickies',
        license='GNU GPL3',
        scripts=['com.github.aboudzakaria.stickies'],
        packages=['stickies'],
        data_files=install_data)

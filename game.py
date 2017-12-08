#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file is part of Place Pictures.
    Place Pictures is a program that allows you to play with any of your pictures.
    Copyright (C) 2017 František Brožka
    email: sentientfanda@gmail.com
    website: https://github.com/existenceexists/place_pictures

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame

import gui
import maps
import mouse
import pictures


class Game:
  
  def __init__(self):
    self.screen=pygame.display.set_mode((1000,800))
    self.screen_rect=self.screen.get_rect()
    pygame.key.set_repeat(500,500)
    self.map=maps.Map(self)
    self.map.open_image("""images/landscape/teapot-dome-sky-em-from-the-boundary-trail-pasayten-wilderness.jpg""")
    self.gui = gui.Gui(self)
    self.pictures=pictures.Pictures(self)
    self.mouse=mouse.Mouse()
    pygame.display.flip()
    
  def run(self):
    self.running=True
    while self.running is True:
      event=pygame.event.wait()
      do_drawing=False
      if self.mouse.update(event):
        do_drawing=True
      if self.gui.update(event):
        do_drawing=True
      if self.pictures.update(event):
        do_drawing=True
      if self.map.update(event):
        do_drawing=True
      if do_drawing:
        self.map.draw()
        self.pictures.draw()
        self.gui.draw()
        self.mouse.draw()
        pygame.display.flip()
    
  def exit(self):
    self.running=False
      

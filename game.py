#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2017 František Brožka <sentientfanda@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import argparse
import pygame

import gui
import maps
import mouse
import pictures
import savegame


class Game:
  
  def __init__(self):
    args=self.parse_command_line_arguments()
    self.screen=pygame.display.set_mode((args.width,args.height))
    self.screen_rect=self.screen.get_rect()
    pygame.display.set_caption("Place Pictures")
    pygame.key.set_repeat(100,100)
    self.map=maps.Map(self)
    self.map.create_map(2000,2000,0,0,0)
    self.gui = gui.Gui(self)
    self.pictures=pictures.Pictures(self)
    self.mouse=mouse.Mouse()
    self.savegame=savegame.Savegame(self)
    pygame.display.flip()
    
  def parse_command_line_arguments(self):
    parser=argparse.ArgumentParser(description='Place Pictures is a program that allows you to play with any of your pictures.')
    parser.add_argument('-w','--width',dest='width',nargs='?',type=int,default=1000,help='Width of window displayed.')
    parser.add_argument('-e','--height',dest='height',nargs='?',type=int,default=700,help='Height of window displayed.')
    return parser.parse_args()
  
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
      

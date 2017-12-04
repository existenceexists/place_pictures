#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

import gui
import maps
import mouse
import pictures


class Game:
  
  def __init__(self):
    self.screen = pygame.display.set_mode((1000,800))
    self.screen_rect=self.screen.get_rect()
    pygame.key.set_repeat(500,500)
    self.map=maps.Map(self)
    self.map.open_image("""images/background/teapot-dome-sky-em-from-the-boundary-trail-pasayten-wilderness.jpg""")
    self.gui = gui.Gui(self)
    self.pictures=pictures.Pictures(self)
    self.mouse=mouse.Mouse()
    self.clock = pygame.time.Clock()
    pygame.display.flip()
    
  def exit(self):
    self.running=False
    
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
      

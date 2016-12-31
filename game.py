# -*- coding: utf-8 -*-

import pygame

import gui
import maps


class Game:
  
  def __init__(self):

    self.screen = pygame.display.set_mode((1000,800))
    self.screen_rect=self.screen.get_rect()
    pygame.display.flip()
    
    self.map=maps.Map(self)
    self.map.open_image("""/home/kdokoli/fanda/wallpapers/teapot-dome-sky-em-from-the-boundary-trail-pasayten-wilderness.jpg""")
    self.gui = gui.Gui(self)
    pygame.display.flip()

  def run(self):
    
    self.running=True
    
    while self.running is True:
      
      if self.map.moving is True:
        events=pygame.event.get()
        if events:
          for event in events:
            self.map.update(event)
            self.gui.update(event)
        else:
          self.map.update(None)
      else:
        ev = pygame.event.wait()
        self.map.update(ev)
        self.gui.update(ev)
      
      pygame.display.flip()
      

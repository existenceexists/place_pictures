# -*- coding: utf-8 -*-

import pygame

import sgc

import gui
import maps
import mouse
import pictures


class Game:
  
  def __init__(self):

    self.screen = sgc.surface.Screen((1000,800))
    self.screen_rect=self.screen.get_rect()
    pygame.display.flip()
    
    self.map=maps.Map(self)
    self.map.open_image("""images/background/teapot-dome-sky-em-from-the-boundary-trail-pasayten-wilderness.jpg""")
    self.gui = gui.Gui(self)
    self.pictures=pictures.Pictures(self)
    self.mouse=mouse.Mouse()
    self.clock = pygame.time.Clock()
    pygame.display.flip()

  def run(self):
    
    self.running=True
    
    while self.running is True:
      time=self.clock.tick(30)
      
      if self.map.moving is True:
        events=pygame.event.get()
        if events:
          for event in events:
            self.mouse.update(event)
            self.gui.update(event)
            self.pictures.update(event)
            self.map.update(event)
        else:
          self.map.update(None)
      else:
        ev = pygame.event.wait()
        self.mouse.update(ev)
        self.gui.update(ev)
        self.pictures.update(ev)
        self.map.update(ev)
      
      sgc.update(time)
      pygame.display.flip()
      

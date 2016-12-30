# -*- coding: utf-8 -*-

import pygame

import gui


class Game:
  
  def __init__(self):

    self.screen = pygame.display.set_mode((1000,800))
    pygame.display.flip()
    
    self.gui = gui.Gui(self)
    pygame.display.flip()

  def run(self):
    
    self.running=True
    
    while self.running is True:
      
      ev = pygame.event.wait()
      
      self.gui.update(ev)
      
      if not self.running:
        break
      
      pygame.display.flip()
      

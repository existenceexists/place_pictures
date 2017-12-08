# -*- coding: utf-8 -*-

import pygame


class Mouse(pygame.sprite.Sprite):
  
  def __init__(self):
    self.image=pygame.Surface((1,1))
    self.rect=self.image.get_rect()
    
  def update(self,event):
    if event.type==pygame.MOUSEMOTION or event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.MOUSEBUTTONUP:
      self.rect.topleft=event.pos
    
  def draw(self):
    pass

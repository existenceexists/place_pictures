# -*- coding: utf-8 -*-

import pygame


class Label(pygame.sprite.Sprite):
  
  def __init__(self,text,color,background_color=None,font=None):
    
    self.screen=pygame.display.get_surface()
    if font is None:
      font=pygame.font.Font(None, 24)
    self.font=font
    if background_color is None:
      self.image=font.render(text,True,pygame.Color(*color))
    else:
      self.image=font.render(text,True,pygame.Color(*color),pygame.Color(*background_color))
    self.rect=self.image.get_rect()
    self.update()
    
  def set_topleft_position(self, position):
    self.rect.topleft=position
    self.update()
    
  def set_topright_position(self, position):
    self.rect.topright=position
    self.update()
    
  def update(self, *event):
    self.screen.blit(self.image,self.rect.topleft)
    

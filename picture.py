# -*- coding: utf-8 -*-

import pygame


class Picture(pygame.sprite.Sprite):
  
  def __init__(self,path):
    pygame.sprite.Sprite.__init__(self)
    self.path=path
    self.image=pygame.image.load(path)
    self.image=self.image.convert()
    self.rect=self.image.get_rect()
    self.is_highlighted=False
    self.is_selected=False
    self.image_original=self.image
    self.image_highlighted=pygame.Surface((self.rect.width+2,self.rect.height+2))
    pygame.draw.rect(self.image_highlighted,pygame.Color(255,255,0),pygame.Rect((1,1),(self.rect.width+1,self.rect.height+1)),1)
    self.image_selected=pygame.Surface((self.rect.width+2,self.rect.height+2))
    pygame.draw.rect(self.image_selected,pygame.Color(255,0,255),pygame.Rect((1,1),(self.rect.width+1,self.rect.height+1)),1)
    self.image_highlighted_and_selected=pygame.Surface((self.rect.width+4,self.rect.height+4))
    pygame.draw.rect(self.image_highlighted_and_selected,pygame.Color(255,0,255),pygame.Rect((2,2),(self.rect.width+1,self.rect.height+1)),1)
    pygame.draw.rect(self.image_highlighted_and_selected,pygame.Color(255,255,0),pygame.Rect((1,1),(self.rect.width+2,self.rect.height+2)),1)
    
  def update(self,position=None,movement=None):
    if movement:
      pos=(self.rect.center[0]+movement[0],self.rect.center[1]+movement[1])
      self.rect.center=position
      self.image.get_rect().center=position
    if position:
      self.rect.center=position
      self.image.get_rect().center=position
  
  def set_layer(self,layer):
    self._layer=layer
    
  def select(self):
    self.is_selected=True
    self.image=self.image_selected
    if self.is_highlighted:
      self.image=self.image_highlighted_and_selected
    pos=self.rect.center
    self.image.get_rect().center=pos
  
  def unselect(self):
    self.is_selected=False
    self.image=self.image_original
    if self.is_highlighted:
      self.image=self.image_highlighted
    pos=self.rect.center
    self.image.get_rect().center=pos
    
  def highlight(self):
    self.is_highlighted=True
    self.image=self.image_highlighted
    if self.is_selected:
      self.image=self.image_highlighted_and_selected
    pos=self.rect.center
    self.image.get_rect().center=pos
  
  def unhighlight(self):
    self.is_higlight=False
    self.image=self.image_original
    if self.is_selected:
      self.image=self.image_selected
    pos=self.rect.center
    self.image.get_rect().center=pos
    
  def set_image_original(self):
    self.image=self.image_original

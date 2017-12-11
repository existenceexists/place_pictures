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


class Picture(pygame.sprite.Sprite):
  
  def __init__(self,path,layer,scale,position):
    pygame.sprite.Sprite.__init__(self)
    self.path=path
    self.set_layer(layer)
    image_unscaled=pygame.image.load(path).convert_alpha()
    image_unscaled_rect=image_unscaled.get_rect()
    scale=float(scale)/100.0# convert from percent
    width=int(round(image_unscaled_rect.width*scale))
    height=int(round(image_unscaled_rect.height*scale))
    self.image_normal=pygame.transform.scale(image_unscaled,(width,height))
    self.rect_normal=self.image_normal.get_rect()
    self.image_highlighted=pygame.Surface((self.rect_normal.width+2,self.rect_normal.height+2)).convert_alpha()
    self.rect_highlighted=self.image_highlighted.get_rect()
    self.image_highlighted.fill(pygame.Color(0,0,0,0))
    pygame.draw.rect(self.image_highlighted,pygame.Color(255,255,255,255),self.rect_highlighted,1)
    self.image_highlighted.blit(self.image_normal,(1,1))
    self.image_selected=pygame.Surface((self.rect_normal.width+2,self.rect_normal.height+2)).convert_alpha()
    self.rect_selected=self.image_selected.get_rect()
    self.image_selected.fill(pygame.Color(0,0,0,0))
    pygame.draw.rect(self.image_selected,pygame.Color(255,255,0,255),self.rect_selected,1)
    self.image_selected.blit(self.image_normal,(1,1))
    self.image_highlighted_and_selected=pygame.Surface((self.rect_normal.width+4,self.rect_normal.height+4)).convert_alpha()
    self.rect_highlighted_and_selected=self.image_highlighted_and_selected.get_rect()
    self.image_highlighted_and_selected.fill(pygame.Color(0,0,0,0))
    pygame.draw.rect(self.image_highlighted_and_selected,pygame.Color(255,255,255,255),self.rect_highlighted_and_selected,1)
    pygame.draw.rect(self.image_highlighted_and_selected,pygame.Color(255,255,0,255),pygame.Rect(1,1,self.rect_highlighted_and_selected.width-2,self.rect_highlighted_and_selected.height-2),1)
    self.image_highlighted_and_selected.blit(self.image_normal,(2,2))
    self.image=self.image_normal
    self.rect=self.rect_normal
    self.is_highlighted=False
    self.is_selected=False
    self.go_to(position)
    
  def update(self,event):
    pass
  
  def draw(self,surface):
    surface.blit(self.image,self.rect)
  
  def set_layer(self,layer):
    self._layer=layer
  
  def go_to(self,position):
    self.rect.center=position
  
  def move_by(self,movement_x,movement_y):
    self.rect.center=(self.rect.center[0]+movement_x,self.rect.center[1]+movement_y)
    
  def select(self):
    self.is_selected=True
    pos=self.rect.center
    self.image=self.image_selected
    self.rect=self.rect_selected
    if self.is_highlighted:
      self.image=self.image_highlighted_and_selected
      self.rect=self.rect_highlighted_and_selected
    self.rect.center=pos
  
  def unselect(self):
    self.is_selected=False
    pos=self.rect.center
    self.image=self.image_normal
    self.rect=self.rect_normal
    if self.is_highlighted:
      self.image=self.image_highlighted
      self.rect=self.rect_highlighted
    self.rect.center=pos
    
  def highlight(self):
    self.is_highlighted=True
    pos=self.rect.center
    self.image=self.image_highlighted
    self.rect=self.rect_highlighted
    if self.is_selected:
      self.image=self.image_highlighted_and_selected
      self.rect=self.rect_highlighted_and_selected
    self.rect.center=pos
  
  def unhighlight(self):
    self.is_highlighted=False
    pos=self.rect.center
    self.image=self.image_normal
    self.rect=self.rect_normal
    if self.is_selected:
      self.image=self.image_selected
      self.rect=self.rect_selected
    self.rect.center=pos

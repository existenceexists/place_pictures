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

import pygame
import ntpath


class Picture(pygame.sprite.Sprite):
  
  def __init__(self,path,scale,center_x,center_y):
    pygame.sprite.Sprite.__init__(self)
    self.path=path
    self.filename=self.path_leaf(path)
    self.is_highlighted=False
    self.is_selected=False
    self.scale_image(scale)
    self.rect.center=(center_x,center_y)
    
  def update(self,event):
    pass
  
  def draw(self,surface):
    surface.blit(self.image,self.rect)
  
  def move_by(self,movement_x,movement_y):
    self.rect.center=(self.rect.center[0]+movement_x,self.rect.center[1]+movement_y)
  
  def update_image(self):
    position=False
    if hasattr(self,"rect"):
      position=self.rect.center
    self.image=self.image_normal
    self.rect=self.rect_normal
    if self.is_highlighted and self.is_selected:
      image_highlighted_and_selected=pygame.Surface((self.rect_normal.width+4,self.rect_normal.height+4)).convert_alpha()
      rect_highlighted_and_selected=image_highlighted_and_selected.get_rect()
      image_highlighted_and_selected.fill(pygame.Color(0,0,0,0))
      pygame.draw.rect(image_highlighted_and_selected,pygame.Color(255,255,255,255),rect_highlighted_and_selected,1)
      pygame.draw.rect(image_highlighted_and_selected,pygame.Color(255,255,0,255),pygame.Rect(1,1,rect_highlighted_and_selected.width-2,rect_highlighted_and_selected.height-2),1)
      image_highlighted_and_selected.blit(self.image_normal,(2,2))
      self.image=image_highlighted_and_selected
      self.rect=rect_highlighted_and_selected
    elif self.is_highlighted:
      image_highlighted=pygame.Surface((self.rect_normal.width+2,self.rect_normal.height+2)).convert_alpha()
      rect_highlighted=image_highlighted.get_rect()
      image_highlighted.fill(pygame.Color(0,0,0,0))
      pygame.draw.rect(image_highlighted,pygame.Color(255,255,255,255),rect_highlighted,1)
      image_highlighted.blit(self.image_normal,(1,1))
      self.image=image_highlighted
      self.rect=rect_highlighted
    elif self.is_selected:
      image_selected=pygame.Surface((self.rect_normal.width+2,self.rect_normal.height+2)).convert_alpha()
      rect_selected=image_selected.get_rect()
      image_selected.fill(pygame.Color(0,0,0,0))
      pygame.draw.rect(image_selected,pygame.Color(255,255,0,255),rect_selected,1)
      image_selected.blit(self.image_normal,(1,1))
      self.image=image_selected
      self.rect=rect_selected
    if not position is False:
      self.rect.center=position
  
  def select(self):
    self.is_selected=True
    self.update_image()
  
  def unselect(self):
    self.is_selected=False
    self.update_image()
    
  def highlight(self):
    self.is_highlighted=True
    self.update_image()
  
  def unhighlight(self):
    self.is_highlighted=False
    self.update_image()
  
  def scale_image(self,scale):
    self.scale=float(scale)
    image_unscaled=pygame.image.load(self.path).convert_alpha()
    image_unscaled_rect=image_unscaled.get_rect()
    width=int(round(image_unscaled_rect.width*self.scale))
    height=int(round(image_unscaled_rect.height*self.scale))
    self.image_normal=pygame.transform.scale(image_unscaled,(width,height))
    self.rect_normal=self.image_normal.get_rect()
    self.update_image()
    
  def path_leaf(self,path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

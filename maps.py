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


class Map:
  
  def __init__(self,game):
    self.game=game
    self.moving=False
    self.movement_step=10
    self.movement=[0,0]
    menu_bar_height=19
    top=menu_bar_height+1
    self.display_area_rect=pygame.Rect(0,top,self.game.screen_rect.width,self.game.screen_rect.height-top)
    self.display_area=self.game.screen.subsurface(self.display_area_rect)
    self.display_area_rect_top_zero=self.display_area.get_rect().copy()
    self.display_area_rect_top_zero.top=0
    self.path=None
    self.background_color=None
    self.is_background_filled_with_color=False
    self.is_background_from_file=False
    self.scale=1.0
    self.image=None
    self.rect=None
    
  def update(self,event):
    return_value=False
    self.moving=False
    self.movement=[0,0]
    rect_left=self.rect.left
    rect_top=self.rect.top
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_DOWN:
        self.set_moving([self.movement[0],-self.movement_step])
      elif event.key==pygame.K_UP:
        self.set_moving([self.movement[0],self.movement_step])
      elif event.key==pygame.K_RIGHT:
        self.set_moving([-self.movement_step,self.movement[1]])
      elif event.key==pygame.K_LEFT:
        self.set_moving([self.movement_step,self.movement[1]])
    elif event.type==pygame.KEYUP:
      if event.key==pygame.K_DOWN or event.key==pygame.K_UP:
        self.set_moving([self.movement[0],0])
      elif event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
        self.set_moving([0,self.movement[1]])
    if self.moving:
      self.rect.topleft=(self.rect.left+self.movement[0],self.rect.top+self.movement[1])
      if self.rect.left>0:
        self.rect.left=0
      if self.rect.right<self.display_area_rect_top_zero.right:
        self.rect.right=self.display_area_rect_top_zero.right
      if self.rect.top>0:
        self.rect.top=0
      if self.rect.bottom<self.display_area_rect_top_zero.bottom:
        self.rect.bottom=self.display_area_rect_top_zero.bottom
    movement_x=self.rect.left-rect_left
    movement_y=self.rect.top-rect_top
    if movement_x!=0 or movement_y!=0:
      return_value=True
      self.game.pictures.move_all_pictures_by(movement_x,movement_y)
    return return_value
    
  def draw(self):
    self.display_area.blit(self.image,self.rect.topleft)
    
  def set_moving(self,movement):
    self.movement=movement
    if movement==[0,0]:
      self.moving=False
    else:
      self.moving=True
    
  def open_image(self,path,scale):
    image_unscaled=pygame.image.load(path).convert_alpha()
    image_unscaled_rect=image_unscaled.get_rect()
    self.scale=float(scale)
    width=int(round(image_unscaled_rect.width*self.scale))
    height=int(round(image_unscaled_rect.height*self.scale))
    image=pygame.transform.scale(image_unscaled,(width,height))
    self.set_background_image(image)
    self.path=path
    self.is_background_filled_with_color=False
    self.is_background_from_file=True
  
  def create_map(self,width,height,rgb_red,rgb_green,rgb_blue):
    image=pygame.Surface((width,height)).convert_alpha()
    image.fill(pygame.Color(rgb_red,rgb_green,rgb_blue))
    self.set_background_image(image)
    self.background_color=(rgb_red,rgb_green,rgb_blue)
    self.scale=1.0
    self.is_background_filled_with_color=True
    self.is_background_from_file=False
  
  def set_background_image(self,image):
    rect=image.get_rect()
    width=rect.width
    height=rect.height
    if not self.rect is None:
      # If map image already existed, 
      # position screen relative to map image 
      # similarly or same as the old relative position to old map image.
      position_x=int((float(self.rect.left)*width)/self.rect.width)
      position_y=int((float(self.rect.top)*height)/self.rect.height)
    else:
      # Position the screen to the center of map image.
      position_x=int((self.display_area_rect.width-width)/2.0)
      position_y=int((self.display_area_rect.height-height)/2.0)
    if self.display_area_rect.width>width:
      width=self.display_area_rect.width
      position_x=0
    if self.display_area_rect.height>height:
      height=self.display_area_rect.height
      position_y=0
    rect.center=(int(width/2),int(height/2))
    self.image=pygame.Surface((width,height)).convert_alpha()
    self.rect=self.image.get_rect()
    self.image.fill(pygame.Color(0,0,0,255))
    self.image.blit(image,rect)
    self.rect.left=position_x
    self.rect.top=position_y
    self.draw()

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

import mouse
import picture


class Pictures:
  """Handles pictures that are placed on the background map image."""
  def __init__(self,game):
    self.game=game
    self.do_not_interact_with_pictures=False
    self.pictures_all=pygame.sprite.LayeredUpdates()
    self.pictures_to_display=pygame.sprite.LayeredUpdates()
    self.pictures_selected=pygame.sprite.LayeredUpdates()
    self.picture_highlighted=pygame.sprite.GroupSingle()
  
  def update(self,event):
    return_value=False
    if self.do_not_interact_with_pictures:
      return return_value
    if event.type==pygame.MOUSEMOTION:
      pictures_list=pygame.sprite.spritecollide(self.game.mouse,self.pictures_to_display,False)
      if pictures_list:
        if self.picture_highlighted.sprite:
          if pictures_list[-1]!=self.picture_highlighted.sprite:
            self.picture_highlighted.sprite.unhighlight()
            pictures_list[-1].highlight()
            self.picture_highlighted.empty()
            self.picture_highlighted.add(pictures_list[-1])
            return_value=True
        else:
            pictures_list[-1].highlight()
            self.picture_highlighted.add(pictures_list[-1])
            return_value=True
      elif self.picture_highlighted.sprite:
            self.picture_highlighted.sprite.unhighlight()
            self.picture_highlighted.empty()
            return_value=True
    elif event.type==pygame.MOUSEBUTTONUP:
      pictures_list=pygame.sprite.spritecollide(self.game.mouse,self.pictures_to_display,False)
      if pictures_list:
        if pictures_list!=self.pictures_selected.sprites():
          for picture in self.pictures_selected:
            picture.unselect()
          pictures_list[-1].select()
          self.pictures_selected.empty()
          self.pictures_selected.add(pictures_list[-1])
          return_value=True
      elif self.pictures_selected.sprites():
        self.selected_pictures_go_to(event.pos)
        pictures_list=pygame.sprite.spritecollide(self.game.mouse,self.pictures_to_display,False)
        return_value=True
        if pictures_list:
          if self.picture_highlighted.sprite:
            if pictures_list[-1]!=self.picture_highlighted.sprite:
              self.picture_highlighted.sprite.unhighlight()
              pictures_list[-1].highlight()
              self.picture_highlighted.empty()
              self.picture_highlighted.add(pictures_list[-1])
              return_value=True
          else:
              pictures_list[-1].highlight()
              self.picture_highlighted.add(pictures_list[-1])
              return_value=True
    return return_value
    
  def draw(self):
    for picture in self.pictures_to_display:
      picture.draw(self.game.screen)
    
  def move_all_pictures_by(self,movement_x,movement_y):
    for picture in self.pictures_all:
       picture.move_by(movement_x,movement_y)
  
  def open_picture_file(self,path,layer,zoom):
    pic=picture.Picture(path,layer,zoom,(self.game.screen_rect.width/2,self.game.screen_rect.height/2))
    self.pictures_all.add(pic)
    self.pictures_to_display.add(pic)
    
  def selected_pictures_go_to(self,position):
    if self.pictures_selected.sprites():
      left=self.game.screen_rect.width
      right=0
      top=self.game.screen_rect.height
      bottom=0
      for pic in self.pictures_selected.sprites():
        left=min(left,pic.rect.left)
        right=max(right,pic.rect.right)
        top=min(top,pic.rect.top)
        bottom=max(bottom,pic.rect.bottom)
      center=(int(left+((right-left)/2.0)),int(top+((bottom-top)/2.0)))
      for pic in self.pictures_selected.sprites():
        pic.rect.center=(position[0]+(center[0]-pic.rect.center[0]),position[1]+(center[1]-pic.rect.center[1]))
    
  def get_number_of_layers(self):
    return len(self.pictures_all.layers())

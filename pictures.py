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
      self.do_not_interact_with_pictures=False
      return False
    if hasattr(event,"pos"):
      event_dict=dict(event.dict)
      pos=list(event_dict["pos"])
      pos[1]=pos[1]-self.game.map.display_area_rect.top
      event_dict["pos"]=pos
      event=pygame.event.Event(event.type,event_dict)
      self.game.mouse.update(event)
    if event.type==pygame.MOUSEMOTION:
      pictures_list=pygame.sprite.spritecollide(self.game.mouse,self.pictures_to_display,False)
      if pictures_list:
        if self.picture_highlighted.sprite:
          if pictures_list[-1]!=self.picture_highlighted.sprite:
            self.picture_highlighted.sprite.unhighlight()
            pictures_list[-1].highlight()
            self.picture_highlighted.empty()
            self.picture_highlighted.add(pictures_list[-1])
            self.game.gui.set_label_highlighted()
            return_value=True
        else:
            pictures_list[-1].highlight()
            self.picture_highlighted.add(pictures_list[-1])
            self.game.gui.set_label_highlighted()
            return_value=True
      elif self.picture_highlighted.sprite:
            self.picture_highlighted.sprite.unhighlight()
            self.picture_highlighted.empty()
            self.game.gui.set_label_highlighted()
            return_value=True
    elif event.type==pygame.MOUSEBUTTONUP:
      pictures_list=pygame.sprite.spritecollide(self.game.mouse,self.pictures_to_display,False)
      if pictures_list:
        if pictures_list!=self.pictures_selected.sprites():
          for picture in self.pictures_selected.sprites():
            picture.unselect()
          pictures_list[-1].select()
          self.pictures_selected.empty()
          self.pictures_selected.add(pictures_list[-1])
          self.game.gui.set_label_selected()
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
              self.game.gui.set_label_highlighted()
              return_value=True
          else:
              pictures_list[-1].highlight()
              self.picture_highlighted.add(pictures_list[-1])
              self.game.gui.set_label_highlighted()
              return_value=True
    return return_value
    
  def draw(self):
    for picture in self.pictures_to_display:
      picture.draw(self.game.map.display_area)
    
  def move_all_pictures_by(self,movement_x,movement_y):
    for picture in self.pictures_all:
       picture.move_by(movement_x,movement_y)
  
  def open_picture_file(self,path,layer,scale,center_x,center_y,select=False,display=True):
    pic=picture.Picture(path,layer,scale,center_x,center_y)
    self.pictures_all.add(pic)
    if select:
      pic.select()
      self.pictures_selected.add(pic)
    if display:
      self.pictures_to_display.add(pic)
    
  def selected_pictures_go_to(self,position):
    if self.pictures_selected.sprites():
      left=self.game.map.display_area_rect.width
      right=0
      top=self.game.map.display_area_rect.height
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
  
  def get_number_of_selected_pictures(self):
    return len(self.pictures_selected.sprites())
  
  def scale_selected_pictures(self,scale):
    for picture in self.pictures_selected.sprites():
      picture.scale_images(scale)
    self.game.gui.set_label_selected()
    self.game.gui.set_label_highlighted()
    
  def copy_selected_pictures(self):
    if self.pictures_selected.sprites():
      left=self.game.map.display_area_rect.width
      right=0
      top=self.game.map.display_area_rect.height
      bottom=0
      for pic in self.pictures_selected.sprites():
        left=min(left,pic.rect.left)
        right=max(right,pic.rect.right)
        top=min(top,pic.rect.top)
        bottom=max(bottom,pic.rect.bottom)
      center=(int(left+((right-left)/2.0)),int(top+((bottom-top)/2.0)))
      for pic in self.pictures_selected.sprites():
        self.open_picture_file(pic.path,pic.get_layer(),pic.scale,self.game.map.display_area_rect.center[0]-(center[0]-pic.rect.center[0]),self.game.map.display_area_rect.center[1]-(center[1]-pic.rect.center[1]))
  
  def move_selected_to_new_layer(self,layer_number):
    layer_number+=1
    for layer in reversed(self.pictures_all.layers()):
      if layer>=layer_number:
        new_layer=layer+1
        for picture in self.pictures_all.get_sprites_from_layer(layer):
          self.pictures_all.change_layer(picture,new_layer)
          if picture in self.pictures_to_display.sprites():
            self.pictures_to_display.change_layer(picture,new_layer)
    for picture in self.pictures_selected.sprites():
      self.pictures_all.change_layer(picture,layer_number)
      if picture in self.pictures_to_display.sprites():
        self.pictures_to_display.change_layer(picture,layer_number)
    self.game.gui.set_label_selected()
    self.game.gui.set_label_highlighted()

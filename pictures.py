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
    self.is_multiple_selection_on=False
    self.is_selecting_on=True
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
      if pictures_list and self.is_selecting_on:
        if not pictures_list[-1] in self.pictures_selected.sprites():
          if not self.is_multiple_selection_on:
            for picture in self.pictures_selected.sprites():
              picture.unselect()
            self.pictures_selected.empty()
          pictures_list[-1].select()
          self.pictures_selected.add(pictures_list[-1])
          self.game.gui.set_label_selected()
          return_value=True
        else:
          pictures_list[-1].unselect()
          self.pictures_selected.remove(pictures_list[-1])
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
        pic.rect.center=(position[0]-(center[0]-pic.rect.center[0]),position[1]-(center[1]-pic.rect.center[1]))
    
  def get_number_of_layers(self):
    return len(self.pictures_all.layers())
  
  def get_number_of_selected_pictures(self):
    return len(self.pictures_selected.sprites())
  
  def turn_on_multiple_selection(self):
    self.is_multiple_selection_on=True
  
  def turn_off_multiple_selection(self):
    self.is_multiple_selection_on=False
  
  def turn_on_selecting(self):
    self.is_selecting_on=True
  
  def turn_off_selecting(self):
    self.is_selecting_on=False

  def deselect_selected(self):
    for picture in self.pictures_selected.sprites():
      picture.unselect()
    self.pictures_selected.empty()
    self.game.gui.set_label_selected()
  
  def select_same_file(self):
    path=self.pictures_selected.sprites()[-1].path
    for picture in self.pictures_to_display.sprites():
      if picture.path==path:
        picture.select()
        self.pictures_selected.add(picture)
    self.game.gui.set_label_selected()
  
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
        self.open_picture_file(pic.path,self.pictures_all.get_layer_of_sprite(pic),pic.scale,self.game.map.display_area_rect.center[0]-(center[0]-pic.rect.center[0]),self.game.map.display_area_rect.center[1]-(center[1]-pic.rect.center[1]))
  
  def remove_empty_layers(self):
    nonempty_layers=[]
    for layer in self.pictures_all.layers():
      if len(self.pictures_all.get_sprites_from_layer(layer))>0:
        nonempty_layers.append(layer)
    if (len(nonempty_layers)-1)==self.pictures_all.get_top_layer():
      return
    l=0
    for layer in nonempty_layers:
      if layer>l:
        self.pictures_all.switch_layer(layer,l)
        self.pictures_to_display.switch_layer(layer,l)
        self.pictures_selected.switch_layer(layer,l)
      l+=1
    pictures_all=pygame.sprite.LayeredUpdates()
    pictures_all.add(self.pictures_all.sprites())
    self.pictures_all=pictures_all
    pictures_to_display=pygame.sprite.LayeredUpdates()
    pictures_to_display.add(self.pictures_to_display.sprites())
    self.pictures_to_display=pictures_to_display
    pictures_selected=pygame.sprite.LayeredUpdates()
    pictures_selected.add(self.pictures_selected.sprites())
    self.pictures_selected=pictures_selected
  
  def move_selected_to_new_layer(self,after_layer_number):
    new_layer=after_layer_number+1
    for layer in reversed(self.pictures_all.layers()):
      if layer>=new_layer:
        layer_move=layer+1
        for picture in self.pictures_all.get_sprites_from_layer(layer):
          picture.set_layer(layer_move)
          self.pictures_all.change_layer(picture,layer_move)
          if picture in self.pictures_to_display.sprites():
            self.pictures_to_display.change_layer(picture,layer_move)
          if picture in self.pictures_selected.sprites():
            self.pictures_selected.change_layer(picture,layer_move)
    for picture in self.pictures_selected.sprites():
      picture.set_layer(new_layer)
      self.pictures_all.change_layer(picture,new_layer)
      if picture in self.pictures_to_display.sprites():
        self.pictures_to_display.change_layer(picture,new_layer)
      if picture in self.pictures_selected.sprites():
        self.pictures_selected.change_layer(picture,new_layer)
    self.remove_empty_layers()
    self.game.gui.set_label_selected()
    self.game.gui.set_label_highlighted()
  
  def move_selected_to_layer(self,layer_number):
    for picture in self.pictures_selected.sprites():
      picture.set_layer(layer_number)
      self.pictures_all.change_layer(picture,layer_number)
      self.pictures_to_display.change_layer(picture,layer_number)
      self.pictures_selected.change_layer(picture,layer_number)
    self.remove_empty_layers()
    self.game.gui.set_label_selected()
    self.game.gui.set_label_highlighted()

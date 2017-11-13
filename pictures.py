# -*- coding: utf-8 -*-

import pygame

import mouse
import picture


class Pictures:
  """Handles pictures that are placed on the background map image."""
  
  def __init__(self,game):
    self.game=game
    self.left_control_key_pressed=False
    self.mouse=mouse.Mouse()
    self.all_pictures=pygame.sprite.LayeredUpdates()
    self.pictures_displayed=pygame.sprite.LayeredUpdates()
    self.pictures_selected=pygame.sprite.LayeredUpdates()
    self.picture_under_mouse_pointer=pygame.sprite.GroupSingle()
    
  def open_file(self,path,layer):
    pic=picture.Picture(path)
    pic.set_layer(layer)
    self.all_pictures.add(pic)
  
  def update(self,event):
    #movement=[0,0]
    if event is None and self.game.map.moving:
      self.all_pictures.update(movement=self.game.map.movement)
      return
    elif event.type==pygame.MOUSEMOTION:
      self.check_mouse_pointer_collision()
    elif event.type==pygame.MOUSEBUTTONUP:
      self.check_on_mousebuttonup(event.pos)
    elif event.type==pygame.KEYDOWN:
      if event.key==pygame.K_LCTRL:
        self.left_control_key_pressed=True
    elif event.type==pygame.KEYUP:
      if event.key==pygame.K_LCTRL:
        self.left_control_key_pressed=False
    
  def check_mouse_pointer_collision(self):
    if self.game.gui.interaction_with_widgets_registered:
      pass
    else:
      pictures=pygame.sprite.spritecollide(self.mouse,self.pictures_displayed,False)
      if pictures:
        if not self.picture_under_mouse_pointer.sprite or self.picture_under_mouse_pointer.sprite and self.picture_under_mouse_pointer.sprite and pictures[-1]!=self.picture_under_mouse_pointer.sprite:
          self.highlight_another_picture(pictures[-1])
      else:
        pass
    
  def check_on_mousebuttonup(self,position):
    if self.game.gui.interaction_with_widgets_registered:
      pass
    else:
      pictures=pygame.sprite.spritecollide(self.mouse,self.pictures_displayed,False)
      if pictures:
        if pictures[-1] in self.pictures_selected.sprites():
          self.pictures_selected.remove(pictures[-1])
        else:
          self.pictures_selected.add(pictures[-1])
      else:
        self.move_selected_pictures(position)
    
  def move_selected_pictures(self,position):
    if self.pictures_selected.sprites():
      left=0
      right=0
      top=0
      bottom=0
      for pic in self.pictures_selected.sprites():
        left=min(left,pic.rect.left)
        right=max(right,pic.rect.right)
        top=min(top,pic.rect.top)
        bottom=max(bottom,pic.rect.bottom)
      center=(int((left+(right-left)/2.0)),int(top+((bottom-top)/2.0)))
      for pic in self.pictures_selected.sprites():
        pic.rect.center=(position[0]+(center[0]-pic.rect.center[0]),position[1]+(center[1]-pic.rect.center[1]))
    
  def highlight_another_picture(self,picture):
    if self.picture_under_mouse_pointer.sprite:
      self.picture_under_mouse_pointer.sprite.unhighlight()
    self.picture_under_mouse_pointer.add(picture)
    self.picture_under_mouse_pointer.sprite.higlight()
    
  def get_number_of_layers(self):
    return len(self.all_pictures.layers())

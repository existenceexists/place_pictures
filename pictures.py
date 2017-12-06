# -*- coding: utf-8 -*-

import pygame

import mouse
import picture


class Pictures:
  """Handles pictures that are placed on the background map image."""
  def __init__(self,game):
    self.game=game
    self.do_not_interact_with_pictures=False
    self.mouse=mouse.Mouse()
    self.all_pictures=pygame.sprite.LayeredUpdates()
    self.pictures_to_display=pygame.sprite.LayeredUpdates()
    self.pictures_selected=pygame.sprite.LayeredUpdates()
    self.picture_under_mouse_pointer=pygame.sprite.GroupSingle()
  
  def update(self,event):
    return_value=None
    if (event.type==pygame.KEYDOWN or event.type==pygame.KEYUP) and self.game.map.moving:
      #self.all_pictures.update(movement=self.game.map.movement)
      for picture in self.all_pictures:
        picture.update(movement=self.game.map.movement)
      return_value=True
    elif event.type==pygame.MOUSEMOTION:
      if self.check_mouse_motion_collision():
        return_value=True
    elif event.type==pygame.MOUSEBUTTONUP:
      if self.check_on_mousebuttonup(event.pos):
        return_value=True
    return return_value
    
  def draw(self):
    self.pictures_to_display.draw(self.game.screen)
    
  def open_picture_file(self,path,layer,zoom):
    pic=picture.Picture(path)
    pic.set_layer(layer)
    self.all_pictures.add(pic)
    
  def check_mouse_motion_collision(self):
    return_value=None
    if self.do_not_interact_with_pictures:
      pass
    else:
      pictures=pygame.sprite.spritecollide(self.mouse,self.pictures_to_display,False)
      if pictures:
        return_value=True
        if not self.picture_under_mouse_pointer.sprite or self.picture_under_mouse_pointer.sprite and self.picture_under_mouse_pointer.sprite and pictures[-1]!=self.picture_under_mouse_pointer.sprite:
          self.highlight_another_picture(pictures[-1])
      else:
        pass
    
  def check_on_mousebuttonup(self,position):
    return_value=None
    if self.do_not_interact_with_pictures:
      pass
    else:
      pictures=pygame.sprite.spritecollide(self.mouse,self.pictures_to_display,False)
      if pictures:
        return_value=True
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

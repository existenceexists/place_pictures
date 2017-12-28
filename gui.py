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

import os
import pygame

import FunnyGUI
import FunnyMenuSystem
import FunnyPathGetter


class Gui:
  
  def __init__(self,game):
    
    self.game=game
    self.container_widgets_FunnyGUI=[]
    #self.widgets_MenuSystem_to_draw_basic=[]
    self.widgets_MenuSystem_to_draw=[]
    self.FunnyGUI_dialogs_stealing_focus=[]
    self.window_background_color=(0,0,0,200)
    self.window_message_background_color=(100,0,0,200)
    self.font_size_buttons_ok_cancel=20
    self.text_line_height=30
    self.text_paragraphs_distance_height=50
    self.savegame_filename_user_part_max_length=30
    self.create_gui()
    self.force_everything_to_draw=True

  def create_gui(self):
    # based on exemple.py in MenuSystem package, the comments are in French
    
    #~ le module doit être initialisé après la vidéo
    FunnyMenuSystem.MenuSystem.init()
    
    #~ change la couleur du fond
    FunnyMenuSystem.MenuSystem.BGCOLOR = pygame.Color(200,200,200,80)
    FunnyMenuSystem.MenuSystem.FGCOLOR = pygame.Color(200,200,200,255)
    FunnyMenuSystem.MenuSystem.BGHIGHTLIGHT = pygame.Color(0,0,0,180)
    FunnyMenuSystem.MenuSystem.BORDER_HL = pygame.Color(200,200,200,180)
    
    #~ création des menus
    self.menu_game = FunnyMenuSystem.MenuSystem.Menu('game', ('info','turn on info','turn off info','save','load','new','export as image','exit'))
    self.menu_picture = FunnyMenuSystem.MenuSystem.Menu('picture', ('open file',))
    self.menu_map = FunnyMenuSystem.MenuSystem.Menu('map',('open file','create','scale with pictures ','scale without pictures'))
    self.menu_select = FunnyMenuSystem.MenuSystem.Menu('select',('start multi selection','end multi selection','disable selecting','enable selecting','within layers','turn off within layers','same file and scale','same file','layers','all on screen','all','by name'))
    self.menu_selection = FunnyMenuSystem.MenuSystem.Menu('selection', ('info','scale','copy','move to layer','give a name','deselect','delete'))
    self.menu_layer = FunnyMenuSystem.MenuSystem.Menu('layers', ('info','new','move','join','display'))
    
    #~ création de la barre
    self.menu_bar=FunnyMenuSystem.MenuSystem.MenuBar()
    self.menu_bar.set((self.menu_game,self.menu_picture,self.menu_map,self.menu_select,self.menu_selection,self.menu_layer))
    
    self.label_selected=FunnyGUI.label.Label(text="selected: 0")
    self.label_selected.rect.center=(int(self.game.map.display_area_rect.width/2.0),int(self.game.map.display_area_rect.height-40))
    self.container_widgets_FunnyGUI.append(self.label_selected)
    self.label_highlighted=FunnyGUI.label.Label(text="highlighted: 0")
    self.label_highlighted.rect.center=(int(self.game.map.display_area_rect.width/2.0),int(self.game.map.display_area_rect.height-80))
    self.container_widgets_FunnyGUI.append(self.label_highlighted)
    
  def update(self, event):
    return_value=False
    self.game.pictures.do_not_interact_with_pictures=False
    if self.is_mouse_pointer_over_gui_widget():
      self.game.pictures.do_not_interact_with_pictures=True
    if self.FunnyGUI_dialogs_stealing_focus:
      if self.FunnyGUI_dialogs_stealing_focus[-1].update(event):
        return_value=True
      return return_value
    rect_list=self.menu_bar.update(event)
    if rect_list:
      # Menu bar changed it's image because user interacted with it.
      return_value=True
      self.widgets_MenuSystem_to_draw=[]
      for rect in rect_list:
        self.widgets_MenuSystem_to_draw.append([self.game.screen.subsurface(rect).copy(),rect])
      if self.menu_bar.choice:
        if self.menu_bar.choice_index==(0,1):
          self.turn_on_info_bar()
        elif self.menu_bar.choice_index==(0,2):
          self.turn_off_info_bar()
        elif self.menu_bar.choice_index==(0,3):
          self.show_dialog_save_game()
        elif self.menu_bar.choice_index==(0,4):
          self.show_dialog_load_game()
        elif self.menu_bar.choice_index==(0,7):
          self.game.exit()
        elif self.menu_bar.choice_index==(1,0):
          self.show_dialog_open_picture_file()
        elif self.menu_bar.choice_index==(2,0):
          self.show_dialog_open_map_file()
        elif self.menu_bar.choice_index==(2,1):
          self.show_dialog_create_map()
        elif self.menu_bar.choice_index==(3,0):
          self.turn_on_multiple_selection()
        elif self.menu_bar.choice_index==(3,1):
          self.turn_off_multiple_selection()
        elif self.menu_bar.choice_index==(3,2):
          self.turn_off_selecting()
        elif self.menu_bar.choice_index==(3,3):
          self.turn_on_selecting()
        elif self.menu_bar.choice_index==(3,4):
          self.show_dialog_select_within_layers()
        elif self.menu_bar.choice_index==(3,5):
          self.turn_off_within_layers()
        elif self.menu_bar.choice_index==(3,6):
          self.select_same_file_and_scale()
        elif self.menu_bar.choice_index==(3,7):
          self.select_same_file()
        elif self.menu_bar.choice_index==(4,1):
          self.show_dialog_scale_selection()
        elif self.menu_bar.choice_index==(4,2):
          self.show_dialog_copy_selection()
        elif self.menu_bar.choice_index==(4,3):
          self.show_dialog_move_selection_to_layer()
        elif self.menu_bar.choice_index==(4,5):
          self.deselect_selected()
        elif self.menu_bar.choice_index==(4,6):
          self.delete_selected()
        elif self.menu_bar.choice_index==(5,1):
          self.show_dialog_new_layer()
        elif self.menu_bar.choice_index==(5,2):
          self.show_dialog_move_layers()
    for widget in self.container_widgets_FunnyGUI:
      if widget.update(event):
        return_value=True
    if self.force_everything_to_draw:
        return_value=True
        self.force_everything_to_draw=False
    return return_value
  
  def draw(self):
    for widget_and_rect in self.widgets_MenuSystem_to_draw:
      self.game.screen.blit(widget_and_rect[0],widget_and_rect[1])
    for widget in self.container_widgets_FunnyGUI:
      widget.draw(self.game.screen)
  
  def is_mouse_pointer_over_gui_widget(self):
    if self.menu_bar.rect.collidepoint(self.game.mouse.rect.center):
      return True
    for surface_and_rect in self.widgets_MenuSystem_to_draw:
      if surface_and_rect[1].collidepoint(self.game.mouse.rect.center):
        return True
    for widget in self.container_widgets_FunnyGUI:
      if widget.rect.collidepoint(self.game.mouse.rect.center):
        return True
    return False
    
  def is_float(self,text):
    try:
      float(text)
    except:
      return False
    else:
      return True
    
  def is_integer(self,text):
    try:
      int(text)
    except:
      return False
    else:
      return True
  
  def make_list_of_layers(self,layers):
    layers_list=[]
    layers=layers.split(",")
    for la in layers:
      l=la.split("-")
      if len(l)==1:
        assert(self.is_integer(l[0]))
        layers_list.append(int(l[0]))
      elif len(l)==2:
        assert(self.is_integer(l[0]))
        assert(self.is_integer(l[1]))
        l=[int(l[0]),int(l[1])]
        assert(l[0]<(l[1]-1))
        layers_list.extend(range(l[0],(l[1]+1)))
      else:
        raise AssertionError
    # Sort the list
    layers_list=sorted(layers_list)
    # Check if list is unique:
    l_list=[]
    for l in layers_list:
      if l in l_list:
        raise AssertionError
      l_list.append(l)
    return layers_list
  
  def add_window(self,window):
    self.container_widgets_FunnyGUI.append(window)
    self.FunnyGUI_dialogs_stealing_focus.append(window)
    self.force_everything_to_draw=True
    self.game.map.do_not_interact_with_map=True
  
  def remove_window(self,window):
    self.container_widgets_FunnyGUI.remove(window)
    self.FunnyGUI_dialogs_stealing_focus.remove(window)
    self.force_everything_to_draw=True
    if len(self.FunnyGUI_dialogs_stealing_focus)==0:
      self.game.map.do_not_interact_with_map=False
    
  def turn_on_info_bar(self):
    if not self.label_selected in self.container_widgets_FunnyGUI:
      self.container_widgets_FunnyGUI.append(self.label_selected)
      self.set_label_selected()
      self.force_everything_to_draw=True
    if not self.label_highlighted in self.container_widgets_FunnyGUI:
      self.container_widgets_FunnyGUI.append(self.label_highlighted)
      self.set_label_highlighted()
      self.force_everything_to_draw=True
    
  def turn_off_info_bar(self):
    if self.label_selected in self.container_widgets_FunnyGUI:
      self.container_widgets_FunnyGUI.remove(self.label_selected)
      self.force_everything_to_draw=True
    if self.label_highlighted in self.container_widgets_FunnyGUI:
      self.container_widgets_FunnyGUI.remove(self.label_highlighted)
      self.force_everything_to_draw=True
  
  def set_label_selected(self):
    text=""
    pictures_selected=self.game.pictures.pictures_selected.sprites()
    count=len(pictures_selected)
    if count==0:
      text="selected: none"
    elif count==1:
      text="selected: 1: {0} , scale: {1}% , layer: {2}".format(pictures_selected[-1].filename,pictures_selected[-1].scale*100.0,self.game.pictures.pictures_all.get_layer_of_sprite(pictures_selected[-1]))
    elif count>1:
      layers_list=[]
      for picture in pictures_selected:
        l=self.game.pictures.pictures_all.get_layer_of_sprite(picture)
        if not l in layers_list:
          layers_list.append(l)
      text="selected: {0} , layers: {1}".format(count,repr(layers_list))
    self.label_selected.SetText(text)
    self.label_selected.rect.center=(int(self.game.map.display_area_rect.width/2.0),int(self.game.map.display_area_rect.height-40))
  
  def set_label_highlighted(self):
    text=""
    if self.game.pictures.picture_highlighted.sprite:
      text="highlighted: {0} , scale: {1}% , layer: {2}".format(self.game.pictures.picture_highlighted.sprite.filename,self.game.pictures.picture_highlighted.sprite.scale*100.0,self.game.pictures.pictures_all.get_layer_of_sprite(self.game.pictures.picture_highlighted.sprite))
    else:
      text="highlighted: none"
    self.label_highlighted.SetText(text)
    self.label_highlighted.rect.center=(int(self.game.map.display_area_rect.width/2.0),int(self.game.map.display_area_rect.height-80))
    
  def display_message_window(self,text_list):
    width=0
    position_x=50
    position_y=50
    widgets=[]
    for text in text_list:
      widgets.append(FunnyGUI.label.Label(text=text))
      widgets[-1].rect.topleft=(position_x,position_y)
      width=max(width,widgets[-1].rect.width)
      position_y+=self.text_line_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.remove_window,normalColor=(255,255,255,255),highlightedColor=(255,255,0,255)))
    position_y+=10
    width=width+(2*50)
    widgets[-1].rect.midtop=(width/2,position_y)
    height=position_y+self.text_paragraphs_distance_height
    if width>self.game.map.display_area_rect.width:
      width=self.game.map.display_area_rect.width
    if height>self.game.map.display_area_rect.height:
      height=self.game.map.display_area_rect.height
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_message_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    self.add_window(window)
    
  def display_dialog_yes_or_no(self,text_list,on_ok_callback):
    width=0
    position_x=50
    position_y=50
    widgets=[]
    for text in text_list:
      widgets.append(FunnyGUI.label.Label(text=text))
      widgets[-1].rect.topleft=(position_x,position_y)
      width=max(width,widgets[-1].rect.width)
      position_y+=self.text_line_height
    position_y+=10
    widgets.append(FunnyGUI.button.Button(text="Yes",onClickCallback=on_ok_callback,normalColor=(255,255,255,255),highlightedColor=(255,255,0,255)))
    widgets.append(FunnyGUI.button.Button(text="No",onClickCallback=self.remove_window,normalColor=(255,255,255,255),highlightedColor=(255,255,0,255)))
    width=max(width,widgets[-1].rect.width+40+widgets[-2].rect.width)
    width=width+(2*50)
    widgets[-2].rect.topright=(int((width/2)-20),position_y)
    widgets[-1].rect.topleft=(int((width/2)+20),position_y)
    height=position_y+50
    if width>self.game.map.display_area_rect.width:
      width=self.game.map.display_area_rect.width
    if height>self.game.map.display_area_rect.height:
      height=self.game.map.display_area_rect.height
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_message_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-2].callbackArgs=(window,)
    widgets[-1].callbackArgs=(window,)
    self.add_window(window)
  
  def show_dialog_open_picture_file(self):
    path_to_picture_to_open=FunnyPathGetter.PathGetter.get(mode=1,caption="Open picture file")
    try:
      path_to_picture_to_open=path_to_picture_to_open.decode("utf-8")
    except AttributeError:
      pass
    if not path_to_picture_to_open:
      return
    self.create_dialog_open_picture_file(os.path.relpath(path_to_picture_to_open))
  
  def create_dialog_open_picture_file(self,path_to_picture_to_open):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Open and show picture file."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter scale percent."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Picture will be scaled"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""to the given percent size of the original picture file."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer or decimal number between 0 and infinity."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_scale=FunnyGUI.inputbox.InputBox()
    input_box_scale.SetText("100")
    widgets.append(input_box_scale)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter layer number."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Picture will be moved into layer with the given number."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    top_layer=self.game.pictures.pictures_all.get_top_layer()
    if top_layer==0:
      widgets.append(FunnyGUI.label.Label(text="""Currently the number can be only number 0 ."""))
    else:
      widgets.append(FunnyGUI.label.Label(text="""The number can be an integer number in range 0 and {0} .""".format(str(top_layer))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_layer=FunnyGUI.inputbox.InputBox()
    input_box_layer.SetText(str(top_layer))
    widgets.append(input_box_layer)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_open_picture_file,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_scale,input_box_layer,path_to_picture_to_open)
    self.add_window(window)
    
  def confirm_dialog_open_picture_file(self,window,input_box_scale,input_box_layer,path_to_picture_to_open):
    scale=input_box_scale.GetText()
    try:
      assert(self.is_float(scale))
      scale=float(scale)
      assert(scale>=0)
    except AssertionError:
      self.display_message_window(["You have not filled scale number field correctly."])
      return
    layer=input_box_layer.GetText()
    try:
      assert(self.is_integer(layer))
      layer=int(layer)
      assert(layer>=0)
      assert(layer<=self.game.pictures.pictures_all.get_top_layer())
    except AssertionError:
      self.display_message_window(["You have not filled layer number field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.open_picture_file(path_to_picture_to_open,layer,scale/100.0,self.game.map.display_area_rect_top_zero.center[0],self.game.map.display_area_rect_top_zero.center[1])
    
  def show_dialog_open_map_file(self):
    path_to_picture_to_open=FunnyPathGetter.PathGetter.get(mode=1,caption="Open background image file")
    try:
      path_to_picture_to_open=path_to_picture_to_open.decode("utf-8")
    except AttributeError:
      pass
    if not path_to_picture_to_open:
      return
    self.create_dialog_open_map_file(os.path.relpath(path_to_picture_to_open))
  
  def create_dialog_open_map_file(self,path_to_picture_to_open):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Open and show background picture file."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter scale percent."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Picture will be scaled"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""to the given percent size of the original picture file."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer or decimal number between 0 and infinity."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_scale=FunnyGUI.inputbox.InputBox()
    input_box_scale.SetText("100")
    widgets.append(input_box_scale)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_open_map_file,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_scale,path_to_picture_to_open)
    self.add_window(window)
    
  def confirm_dialog_open_map_file(self,window,input_box_scale,path_to_picture_to_open):
    scale=input_box_scale.GetText()
    try:
      assert(self.is_float(scale))
      scale=float(scale)
      assert(scale>=0)
    except AssertionError:
      self.display_message_window(["You have not filled scale number field correctly."])
      return
    self.remove_window(window)
    self.game.map.open_image(path_to_picture_to_open,scale/100.0)
  
  def show_dialog_create_map(self):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Create background image filled with solid color."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter size of the background image:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Size of the current background image is: width: {0} , height: {1}""".format(str(self.game.map.rect.width),str(self.game.map.rect.height))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""width:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_width=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_width)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""height:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_height=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_height)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter RGB color value the image will be filled with:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Values can be integer numbers between 0 and 255."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Red:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_rgb_red=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_rgb_red)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Green:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_rgb_green=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_rgb_green)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Blue:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_rgb_blue=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_rgb_blue)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y+=self.text_line_height
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_create_map,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_width,input_box_height,input_box_rgb_red,input_box_rgb_green,input_box_rgb_blue)
    self.add_window(window)
  
  def confirm_dialog_create_map(self,window,input_box_width,input_box_height,input_box_rgb_red,input_box_rgb_green,input_box_rgb_blue):
    width=input_box_width.GetText()
    try:
      assert(self.is_integer(width))
      width=int(width)
      assert(width>=0)
    except AssertionError:
      self.display_message_window(["You have not filled width number field correctly."])
      return
    height=input_box_height.GetText()
    try:
      assert(self.is_integer(height))
      height=int(height)
      assert(height>=0)
    except AssertionError:
      self.display_message_window(["You have not filled height number field correctly."])
      return
    rgb_red=input_box_rgb_red.GetText()
    try:
      assert(self.is_integer(rgb_red))
      rgb_red=int(rgb_red)
      assert(rgb_red>=0)
      assert(rgb_red<=255)
    except AssertionError:
      self.display_message_window(["You have not filled RGB color Red number field correctly."])
      return
    rgb_green=input_box_rgb_green.GetText()
    try:
      assert(self.is_integer(rgb_green))
      rgb_green=int(rgb_green)
      assert(rgb_green>=0)
      assert(rgb_green<=255)
    except AssertionError:
      self.display_message_window(["You have not filled RGB color Green number field correctly."])
      return
    rgb_blue=input_box_rgb_blue.GetText()
    try:
      assert(self.is_integer(rgb_blue))
      rgb_blue=int(rgb_blue)
      assert(rgb_blue>=0)
      assert(rgb_blue<=255)
    except AssertionError:
      self.display_message_window(["You have not filled RGB color Blue number field correctly."])
      return
    self.remove_window(window)
    self.game.map.create_map(width,height,rgb_red,rgb_green,rgb_blue)
    
  def show_dialog_scale_selection(self):
    number_of_selected_pictures=self.game.pictures.get_number_of_selected_pictures()
    if number_of_selected_pictures==0:
      self.display_message_window(["No pictures selected."])
      return
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Scale pictures"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""The number of selected pictures is: {0}""".format(str(number_of_selected_pictures))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter scale percent."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Selected pictures will be scaled"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""to the given percent size of the original picture files."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer or decimal number between 0 and infinity."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_scale=FunnyGUI.inputbox.InputBox()
    input_box_scale.SetText("100")
    widgets.append(input_box_scale)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_scale_selection,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_scale)
    self.add_window(window)
    
  def confirm_dialog_scale_selection(self,window,input_box_scale):
    scale=input_box_scale.GetText()
    try:
      assert(self.is_float(scale))
      scale=float(scale)
      assert(scale>=0)
    except AssertionError:
      self.display_message_window(["You have not filled scale number field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.scale_selected_pictures(scale/100.0)
  
  def show_dialog_save_game(self):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Save game"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter part of filename."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Savegame will be named this way:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""savegame.[timestamp].[your_part].save"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Where you can specify [your_part] by filling the following field."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""[your_part] can be text of maximum {0} characters.""".format(str(self.savegame_filename_user_part_max_length))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""[your_part] is optional. You can leave this empty."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_filename_part=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_filename_part)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_save_game,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_filename_part)
    self.add_window(window)
    
  def confirm_dialog_save_game(self,window,input_box_filename_part):
    filename_user_part=input_box_filename_part.GetText()
    try:
      assert(len(filename_user_part)<=self.savegame_filename_user_part_max_length)
    except AssertionError:
      self.display_message_window(["Enter text of length equal or less than {0} characters.".format(str(self.savegame_filename_user_part_max_length))])
      return
    self.remove_window(window)
    self.game.savegame.save(filename_user_part)
    
  def show_dialog_load_game(self):
    path=FunnyPathGetter.PathGetter.get(path=self.game.savegame.savegames_directory_path_absolute,mode=1,caption="Open savegame file")
    try:
      path=path.decode("utf-8")
    except AttributeError:
      pass
    if not path:
      return
    self.create_dialog_load_game(os.path.relpath(path))
  
  def create_dialog_load_game(self,path):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Load game"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Saved game from the selected file will be loaded."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Do you want to proceed?"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_load_game,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,path)
    self.add_window(window)
    
  def confirm_dialog_load_game(self,window,path):
    self.remove_window(window)
    self.game.savegame.load(path)
    
  def show_dialog_copy_selection(self):
    number_of_selected_pictures=self.game.pictures.get_number_of_selected_pictures()
    beginning=""
    if number_of_selected_pictures==0:
      self.display_message_window(["No pictures selected."])
      return
    elif number_of_selected_pictures==1:
      beginning="1 picture"
    else:
      beginning="{0} pictures".format(number_of_selected_pictures)
    self.display_dialog_yes_or_no(["{0} will be copied.".format(beginning),"Do you want to proceed?"],self.confirm_dialog_copy_selection)
    
  def confirm_dialog_copy_selection(self,window):
    self.remove_window(window)
    self.game.pictures.copy_selected_pictures()
  
  def show_dialog_new_layer(self):
    number_of_selected_pictures=self.game.pictures.get_number_of_selected_pictures()
    if number_of_selected_pictures==0:
      self.display_message_window(["No pictures selected."])
      return
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""New layer"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Move {0} selected pictures into new layer.""".format(str(number_of_selected_pictures))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Specify a layer after that the new layer will be inserted:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""E.g. if you give number 2, the new layer will have number 3."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""If you give -1, the new layer will be the first layer, i.e. number 0."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""You can give an integer number in range -1 and {0}""".format(str(self.game.pictures.pictures_all.get_top_layer()))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_layer_number=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_layer_number)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_new_layer,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_layer_number)
    self.add_window(window)
    
  def confirm_dialog_new_layer(self,window,input_box_layer_number):
    layer_number=input_box_layer_number.GetText()
    try:
      assert(self.is_integer(layer_number))
      layer_number=int(layer_number)
      assert(layer_number>=-1)
      assert(layer_number<=self.game.pictures.pictures_all.get_top_layer())
    except AssertionError:
      self.display_message_window(["You have not filled the layer number field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.move_selected_to_new_layer(layer_number)
  
  def show_dialog_move_selection_to_layer(self):
    number_of_selected_pictures=self.game.pictures.get_number_of_selected_pictures()
    if number_of_selected_pictures==0:
      self.display_message_window(["No pictures selected."])
      return
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Move selected pictures to layer"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Move {0} selected pictures into existing layer.""".format(str(number_of_selected_pictures))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Specify a layer to move the selected pictures to:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""You can give an integer number in range 0 and {0}""".format(str(self.game.pictures.pictures_all.get_top_layer()))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_layer_number=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_layer_number)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_move_selection_to_layer,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_layer_number)
    self.add_window(window)
    
  def confirm_dialog_move_selection_to_layer(self,window,input_box_layer_number):
    layer_number=input_box_layer_number.GetText()
    try:
      assert(self.is_integer(layer_number))
      layer_number=int(layer_number)
      assert(layer_number>=0)
      assert(layer_number<=self.game.pictures.pictures_all.get_top_layer())
    except AssertionError:
      self.display_message_window(["You have not filled the layer number field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.move_selected_to_layer(layer_number)
  
  def turn_on_multiple_selection(self):
    self.game.pictures.turn_on_multiple_selection()
  
  def turn_off_multiple_selection(self):
    self.game.pictures.turn_off_multiple_selection()
  
  def turn_on_selecting(self):
    self.game.pictures.turn_on_selecting()
  
  def turn_off_selecting(self):
    self.game.pictures.turn_off_selecting()
  
  def deselect_selected(self):
    self.game.pictures.deselect_selected()
  
  def select_same_file(self):
    if self.game.pictures.get_number_of_selected_pictures()==0:
      self.display_message_window(["No picture selected."])
      return
    paths=[]
    for picture in self.game.pictures.pictures_selected.sprites():
      if picture.path not in paths:
        paths.append(picture.path)
    if len(paths)>1:
      self.display_message_window(["Invalid selection to achieve this task.","Only pictures sharing common image file should be selected.","Try to deselect selected pictures and select only one picture."])
      return
    self.game.pictures.select_same_file()
  
  def select_same_file_and_scale(self):
    if self.game.pictures.get_number_of_selected_pictures()==0:
      self.display_message_window(["No picture selected."])
      return
    paths=[]
    scalings=[]
    for picture in self.game.pictures.pictures_selected.sprites():
      if picture.path not in paths:
        paths.append(picture.path)
      if picture.scale not in scalings:
        scalings.append(picture.scale)
    if len(paths)>1:
      self.display_message_window(["Invalid selection to achieve this task.","Only pictures sharing common image file should be already selected.","Try to deselect selected pictures and select only one picture and try again."])
      return
    if len(scalings)>1:
      self.display_message_window(["Invalid selection to achieve this task.","Only pictures sharing common scale should be already selected.","Try to deselect selected pictures and select only one picture and try again."])
      return
    self.game.pictures.select_same_file_and_scale()
  
  def delete_selected(self):
    number_of_selected_pictures=self.game.pictures.get_number_of_selected_pictures()
    if number_of_selected_pictures==0:
      self.display_message_window(["No picture selected."])
      return
    self.display_dialog_yes_or_no(["Delete selected pictures?","{0} pictures will be deleted.".format(number_of_selected_pictures),"Do you want to proceed?"],self.confirm_dialog_delete_selected)
  
  def confirm_dialog_delete_selected(self,window):
    self.remove_window(window)
    self.game.pictures.delete_selected()
  
  def show_dialog_select_within_layers(self):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Select only within given layers"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Limit selectable and highlightable pictures to pictures within specified layers."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Specify layers to that selecting will be limited:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""You can give comma separated integer numbers or ranges in range 0 and {0}""".format(str(self.game.pictures.pictures_all.get_top_layer()))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Example: 1,3-5,7"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_layers=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_layers)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_select_within_layers,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_layers)
    self.add_window(window)
    
  def confirm_dialog_select_within_layers(self,window,input_box_layers):
    layers=input_box_layers.GetText()
    try:
      layers=self.make_list_of_layers(layers)
      assert(layers[-1]<=self.game.pictures.pictures_all.get_top_layer())
    except AssertionError:
      self.display_message_window(["You have not filled the layers list and ranges of layers field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.set_selecting_within_layers(layers)
  
  def turn_off_within_layers(self):
    self.game.pictures.unset_selecting_within_layers()
  
  def show_dialog_move_layers(self):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Move layers"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Move one or more layers to position after a specified layer."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Specify layers to move:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""You can give comma separated integer numbers or ranges in range 0 and {0}""".format(str(self.game.pictures.pictures_all.get_top_layer()))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Example: 1,3-5,7"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_layers_to_move=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_layers_to_move)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Specify layer after that layers to be moved will be inserted:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""You can give integer number in range -1 and {0}""".format(str(self.game.pictures.pictures_all.get_top_layer()))))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_line_height
    input_box_where_to_be_moved=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_where_to_be_moved)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y+=self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_move_layers,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topright=((width/2)-20,position_y)
    widgets.append(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.remove_window,fontSize=self.font_size_buttons_ok_cancel))
    widgets[-1].rect.topleft=((width/2)+20,position_y)
    height=position_y+70
    window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=self.window_background_color)
    window.rect.center=(self.game.map.display_area_rect.center[0],self.game.map.display_area_rect.center[1])
    for widget in widgets:
      window.add(widget)
    widgets[-1].callbackArgs=(window,)
    widgets[-2].callbackArgs=(window,input_box_layers_to_move,input_box_where_to_be_moved)
    self.add_window(window)
    
  def confirm_dialog_move_layers(self,window,input_box_layers_to_move,input_box_where_to_be_moved):
    layers_to_move=input_box_layers_to_move.GetText()
    try:
      layers_to_move=self.make_list_of_layers(layers_to_move)
      assert(layers_to_move[-1]>=0)
      assert(layers_to_move[-1]<=self.game.pictures.pictures_all.get_top_layer())
    except AssertionError:
      self.display_message_window(["You have not filled the layers to move list and ranges of layers to move field correctly."])
      return
    where_to_be_moved=input_box_where_to_be_moved.GetText()
    try:
      assert(self.is_integer(where_to_be_moved))
      where_to_be_moved=int(where_to_be_moved)
      assert(where_to_be_moved>=-1)
      assert(where_to_be_moved<=self.game.pictures.pictures_all.get_top_layer())
    except AssertionError:
      self.display_message_window(["You have not filled the where to move field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.move_layers(layers_to_move,where_to_be_moved)

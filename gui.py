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
    self.create_gui()
    self.force_everything_to_draw=False

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
    self.menu_select = FunnyMenuSystem.MenuSystem.Menu('select',('start multi selection','end multi selection','disable selecting','enable selecting','within layers','same file and scale','same file','layers','all on screen','all','by name'))
    self.menu_selection = FunnyMenuSystem.MenuSystem.Menu('selection', ('info','scale','copy','move to layer','give a name','deselect','delete'))
    self.menu_layer = FunnyMenuSystem.MenuSystem.Menu('layers', ('info','new','move','join','display'))
    self.menu_map = FunnyMenuSystem.MenuSystem.Menu('map',('scale with pictures ','scale without pictures','open file','create'))
    
    #~ création de la barre
    self.menu_bar=FunnyMenuSystem.MenuSystem.MenuBar()
    self.menu_bar.set((self.menu_game,self.menu_picture,self.menu_select,self.menu_selection,self.menu_layer,self.menu_map))
    #menu_bar_rect=self.menu_bar.set((self.menu_game,self.menu_picture,self.menu_select,self.menu_selection,self.menu_layer,self.menu_map))
    #self.widgets_MenuSystem_to_draw_basic.append([self.game.screen.subsurface(menu_bar_rect).copy(),menu_bar_rect])
    #self.widgets_MenuSystem_to_draw.append([self.game.screen.subsurface(menu_bar_rect).copy(),menu_bar_rect])
    
    #self.label_selected_pictures_count=label.Label('pictures:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_pictures_count.set_topright_position((990,60))
    #self.widgets_container.append(self.label_selected_pictures_count)
    #self.label_selected_picture_types_count=label.Label('types:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_picture_types_count.set_topright_position((990,90))
    #self.widgets_container.append(self.label_selected_picture_types_count)
    
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
        if self.menu_bar.choice_index==(0,7):
          self.game.exit()
        elif self.menu_bar.choice_index==(1,0):
          self.show_dialog_open_picture_file()
        elif self.menu_bar.choice_index==(3,1):
          self.show_dialog_scale_selection()
        elif self.menu_bar.choice_index==(5,2):
          self.show_dialog_open_map_file()
        elif self.menu_bar.choice_index==(5,3):
          self.show_dialog_create_map()
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
  
  def add_window(self,window):
    self.container_widgets_FunnyGUI.append(window)
    self.FunnyGUI_dialogs_stealing_focus.append(window)
    self.force_everything_to_draw=True
  
  def remove_window(self,window):
    self.container_widgets_FunnyGUI.remove(window)
    self.FunnyGUI_dialogs_stealing_focus.remove(window)
    self.force_everything_to_draw=True
    
  def display_message_window(self,text_list):
    width=0
    position_x=50
    position_y=50
    widgets=[]
    for text in text_list:
      widgets.append(FunnyGUI.label.Label(text=text))
      widgets[-1].rect.topleft=(position_x,position_y)
      width=max(width,widgets[-1].rect.width)
      position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.button.Button(text="OK",onClickCallback=self.remove_window,normalColor=(255,255,255,255),highlightedColor=(255,255,0,255)))
    position_y=position_y+10
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
    
  def show_dialog_open_picture_file(self):
    path_to_picture_to_open=FunnyPathGetter.PathGetter.get()
    if not path_to_picture_to_open:
      return
    self.create_dialog_open_picture_file(path_to_picture_to_open)
  
  def create_dialog_open_picture_file(self,path_to_picture_to_open):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Open and show picture file."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter scale percent."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The size of the new picture will be scaled"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""to the given percent size of the original picture."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer or floating point number between 0 and infinity."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    input_box_scale=FunnyGUI.inputbox.InputBox()
    input_box_scale.SetText("100")
    widgets.append(input_box_scale)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter layer number."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The new picture will be moved into the layer."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    top_layer=self.game.pictures.get_number_of_layers()
    if top_layer==0:
      top_layer=1
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer number between 1 and """+str(top_layer)+""" ."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    input_box_layer=FunnyGUI.inputbox.InputBox()
    input_box_layer.SetText("1")
    widgets.append(input_box_layer)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
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
      assert(layer>=1)
      number_of_layers=self.game.pictures.get_number_of_layers()
      if number_of_layers>0:
        assert(layer<=self.game.pictures.get_number_of_layers())
    except AssertionError:
      self.display_message_window(["You have not filled layer number field correctly."])
      return
    self.remove_window(window)
    self.game.pictures.open_picture_file(path_to_picture_to_open,layer,scale)
    
  def show_dialog_open_map_file(self):
    path_to_picture_to_open=FunnyPathGetter.PathGetter.get()
    if not path_to_picture_to_open:
      return
    self.create_dialog_open_map_file(path_to_picture_to_open)
  
  def create_dialog_open_map_file(self,path_to_picture_to_open):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Open and show background picture file."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter scale percent."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The size of the new picture will be scaled"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""to the given percent size of the original picture."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer or floating point number between 0 and infinity."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    input_box_scale=FunnyGUI.inputbox.InputBox()
    input_box_scale.SetText("100")
    widgets.append(input_box_scale)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
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
    self.game.map.open_image(path_to_picture_to_open,scale)
  
  def show_dialog_create_map(self):
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Create background image filled with solid color."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter size of the background image:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Size of the current background image is: width: """+str(self.game.map.rect.width)+""", height: """+str(self.game.map.rect.height)))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""width:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_width=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_width)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""height:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_height=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_height)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter RGB color value the image will be filled with:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Values can be integer numbers between 0 and 255."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Red:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_rgb_red=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_rgb_red)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Green:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_rgb_green=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_rgb_green)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""Blue:"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    input_box_rgb_blue=FunnyGUI.inputbox.InputBox()
    widgets.append(input_box_rgb_blue)
    widgets[-1].rect.topleft=(position_x+60,position_y)
    position_y=position_y+self.text_line_height
    position_y=position_y+self.text_paragraphs_distance_height
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
    width=580
    position_x=50
    position_y=50
    widgets=[]
    widgets.append(FunnyGUI.label.Label(text="""Scale picture"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
    widgets.append(FunnyGUI.label.Label(text="""Enter scale percent."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The size of picture files of selected pictures will be scaled"""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""to the given percent size of the original picture files."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    widgets.append(FunnyGUI.label.Label(text="""The number can be an integer or floating point number between 0 and infinity."""))
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_line_height
    input_box_scale=FunnyGUI.inputbox.InputBox()
    input_box_scale.SetText("100")
    widgets.append(input_box_scale)
    widgets[-1].rect.topleft=(position_x,position_y)
    position_y=position_y+self.text_paragraphs_distance_height
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
    self.game.pictures.scale_selected_pictures(scale)

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

import MenuSystem
import PathGetter
import FunnyGUI


class Gui:
  
  def __init__(self,game):
    
    self.game=game
    self.container_widgets_FunnyGUI=[]
    self.widgets_MenuSystem_to_draw_basic=[]
    self.widgets_MenuSystem_to_draw=[]
    self.FunnyGUI_dialogs_stealing_focus=[]
    self.create_gui()
    self.path_picture_to_open=None
    self.force_everything_to_draw=False

  def create_gui(self):
    # based on exemple.py in MenuSystem package, the comments are in French
    
    #~ le module doit être initialisé après la vidéo
    MenuSystem.MenuSystem.init()
    
    #~ change la couleur du fond
    MenuSystem.MenuSystem.BGCOLOR = pygame.Color(200,200,200,80)
    MenuSystem.MenuSystem.FGCOLOR = pygame.Color(200,200,200,255)
    MenuSystem.MenuSystem.BGHIGHTLIGHT = pygame.Color(0,0,0,180)
    MenuSystem.MenuSystem.BORDER_HL = pygame.Color(200,200,200,180)
    
    #~ création des menus
    self.menu_game = MenuSystem.MenuSystem.Menu('game', ('save','load','new','export as image','exit'))
    self.menu_picture = MenuSystem.MenuSystem.Menu('picture', ('open file',))
    self.menu_select = MenuSystem.MenuSystem.Menu('select',('same file and zoom','same file','layers','all on screen','all','by name'))
    self.menu_selection = MenuSystem.MenuSystem.Menu('selection', ('zoom','copy','move to layer','give a name','deselect','delete'))
    self.menu_layer = MenuSystem.MenuSystem.Menu('layer', ('new layer','show list','move','join layers','display'))
    self.menu_map = MenuSystem.MenuSystem.Menu('map',('zoom with pictures ','zoom without pictures','open file','create'))
    
    #~ création de la barre
    self.menu_bar=MenuSystem.MenuSystem.MenuBar()
    menu_bar_rect=self.menu_bar.set((self.menu_game,self.menu_picture,self.menu_select,self.menu_selection,self.menu_layer,self.menu_map))
    self.widgets_MenuSystem_to_draw_basic.append([self.game.screen.subsurface(menu_bar_rect).copy(),menu_bar_rect])
    self.widgets_MenuSystem_to_draw=list(self.widgets_MenuSystem_to_draw_basic)
    
    #self.label_selected_pictures_count=label.Label('pictures:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_pictures_count.set_topright_position((990,60))
    #self.widgets_container.append(self.label_selected_pictures_count)
    #self.label_selected_picture_types_count=label.Label('types:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_picture_types_count.set_topright_position((990,90))
    #self.widgets_container.append(self.label_selected_picture_types_count)
    
  def update(self, event):
    return_value=False
    self.game.pictures.do_not_interact_with_pictures=False
    if self.FunnyGUI_dialogs_stealing_focus:
      self.game.pictures.do_not_interact_with_pictures=True
      if self.FunnyGUI_dialogs_stealing_focus[-1].update(event):
        return_value=True
      return return_value
    rect_list=self.menu_bar.update(event)
    if rect_list:
      # Menu bar changed it's image because user interacted with it.
      return_value=True
      self.game.pictures.do_not_interact_with_pictures=True
      self.widgets_MenuSystem_to_draw=list(self.widgets_MenuSystem_to_draw_basic)
      for rect in rect_list:
        self.widgets_MenuSystem_to_draw.append([self.game.screen.subsurface(rect).copy(),rect])
      if self.menu_bar.choice:
        if self.menu_bar.choice_index==(0,4):
          self.game.exit()
        elif self.menu_bar.choice_index==(1,0):
          self.show_dialog_open_picture_file()
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
    
  def show_dialog_open_picture_file(self):
    self.path_to_picture_to_open=PathGetter.PathGetter.get()
    if not self.path_to_picture_to_open:
      return
    self.create_dialog_open_picture_file()
  
  def create_dialog_open_picture_file(self):
    self.window_dialog_open_picture_file=FunnyGUI.window.Window(width=530,height=480,backgroundColor=(0,0,0,200))
    self.window_dialog_open_picture_file.rect.center=(self.game.screen_rect.width/2,self.game.screen_rect.height/2)
    self.container_widgets_FunnyGUI.append(self.window_dialog_open_picture_file)
    self.FunnyGUI_dialogs_stealing_focus.append(self.window_dialog_open_picture_file)
    position_x=50
    position_y=50
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""Open and show picture file."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+50
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""Enter zoom percent."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The size of the new picture will be scaled"""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""to the given percent size of the original picture."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The number can be an integer or float number between 0 and infinity."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    self.input_box_zoom=FunnyGUI.inputbox.InputBox()
    self.input_box_zoom.SetText("100")
    self.window_dialog_open_picture_file.add(self.input_box_zoom)
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+50
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""Enter layer number."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The new picture will be moved into the layer."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    top_layer=self.game.pictures.get_number_of_layers()
    if top_layer==0:
      top_layer=1
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The number can be an integer number between 1 and """+str(top_layer)+""" ."""))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+30
    self.input_box_layer=FunnyGUI.inputbox.InputBox()
    self.input_box_layer.SetText("1")
    self.window_dialog_open_picture_file.add(self.input_box_layer)
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x,position_y)
    position_y=position_y+50
    self.window_dialog_open_picture_file.add(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_open_picture_file))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x+100,position_y)
    self.window_dialog_open_picture_file.add(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.cancel_dialog_open_picture_file))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x+150,position_y)
    
  def confirm_dialog_open_picture_file(self):
    zoom=self.input_box_zoom.GetText()
    try:
      assert(self.is_float(zoom))
      zoom=float(zoom)
      assert(zoom>=0)
    except AssertionError:
      self.display_message_window(["You have not filled zoom number field correctly."])
      return
    layer=self.input_box_layer.GetText()
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
    self.container_widgets_FunnyGUI.remove(self.window_dialog_open_picture_file)
    self.FunnyGUI_dialogs_stealing_focus.remove(self.window_dialog_open_picture_file)
    self.force_everything_to_draw=True
    self.game.pictures.open_picture_file(self.path_to_picture_to_open,layer,zoom)
    
  def cancel_dialog_open_picture_file(self):
    self.container_widgets_FunnyGUI.remove(self.window_dialog_open_picture_file)
    self.FunnyGUI_dialogs_stealing_focus.remove(self.window_dialog_open_picture_file)
    self.force_everything_to_draw=True
    
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
  
  def display_message_window(self,text_list):
    height=50
    width=0
    for text in text_list:
      height=height+30
      width=max(width,pygame.font.Font(pygame.font.match_font("freesans,sansserif,microsoftsansserif,arial,dejavusans,verdana,timesnewroman,helvetica"),14).size(text)[0])
    height=height+50
    width=width+(2*50)
    if width>self.game.screen_rect.width:
      width=self.game.screen_rect.widt
    if height>self.game.screen_rect.height:
      height=self.game.screen_rect.height
    self.message_window=FunnyGUI.window.Window(width=width,height=height,backgroundColor=(100,0,0,200))
    self.message_window.rect.center=(self.game.screen_rect.width/2,self.game.screen_rect.height/2)
    self.container_widgets_FunnyGUI.append(self.message_window)
    self.FunnyGUI_dialogs_stealing_focus.append(self.message_window)
    position_x=50
    position_y=50
    for text in text_list:
      self.message_window.add(FunnyGUI.label.Label(text=text))
      self.message_window.widgets[-1].rect.move_ip(position_x,position_y)
      position_y=position_y+30
    self.message_window.add(FunnyGUI.button.Button(text="OK",onClickCallback=self.dismiss_message_window,normalColor=(255,255,255,255),highlightedColor=(255,255,0,255)))
    self.message_window.widgets[-1].rect.center=(width/2,position_y+10)
  
  def dismiss_message_window(self):
    self.container_widgets_FunnyGUI.remove(self.message_window)
    self.FunnyGUI_dialogs_stealing_focus.remove(self.message_window)
    self.force_everything_to_draw=True

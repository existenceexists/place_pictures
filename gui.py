# -*- coding: utf-8 -*-

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
    self.menu_game = MenuSystem.MenuSystem.Menu('game', ('save','load','new','exit'))
    self.menu_map = MenuSystem.MenuSystem.Menu('map',('zoom with pictures ','zoom without pictures','open file','create','export with pictures as one image'))
    self.menu_layer = MenuSystem.MenuSystem.Menu('layer', ('show list','new','move','join layers','delete empty layers'))
    self.menu_picture = MenuSystem.MenuSystem.Menu('picture', ('open file',))
    self.menu_selection = MenuSystem.MenuSystem.Menu('selection', ('zoom','move to layer','give a name'))
    self.menu_select = MenuSystem.MenuSystem.Menu('select',('same file and zoom','same file','layers','all on screen','all'))
    
    #~ création de la barre
    self.menu_bar=MenuSystem.MenuSystem.MenuBar()
    menu_bar_rect=self.menu_bar.set((self.menu_game,self.menu_map,self.menu_layer,self.menu_picture,self.menu_selection,self.menu_select))
    self.widgets_MenuSystem_to_draw_basic.append([self.game.screen.subsurface(menu_bar_rect).copy(),menu_bar_rect])
    self.widgets_MenuSystem_to_draw=list(self.widgets_MenuSystem_to_draw_basic)
    
    #self.label_selected_pictures_count=label.Label('pictures:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_pictures_count.set_topright_position((990,60))
    #self.widgets_container.append(self.label_selected_pictures_count)
    #self.label_selected_picture_types_count=label.Label('types:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_picture_types_count.set_topright_position((990,90))
    #self.widgets_container.append(self.label_selected_picture_types_count)
    
  def create_dialog_open_picture_file(self):
    self.window_dialog_open_picture_file=FunnyGUI.window.Window()
    self.window_dialog_open_picture_file.rect.center=(self.game.screen_rect.width/2,self.game.screen_rect.height/2)
    self.container_widgets_FunnyGUI.append(self.window_dialog_open_picture_file)
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""Open and show picture file."""))
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""Enter zoom percent."""))
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The size of the new picture will be scaled"""))
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""to the given percent size of the original picture."""))
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The number can be an integer or float number between 0 and infinity."""))
    self.input_box_zoom=FunnyGUI.inputbox.InputBox()
    self.input_box_zoom.SetText("100")
    self.window_dialog_open_picture_file.add(self.input_box_zoom)
    top_layer=self.game.pictures.get_number_of_layers()
    if top_layer==0:
      top_layer=1
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""Enter layer number."""))
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The new picture will be moved into the layer."""))
    self.window_dialog_open_picture_file.add(FunnyGUI.label.Label(text="""The number can be an integer number between 1 and """+str(top_layer)+""" ."""))
    self.input_box_layer=FunnyGUI.inputbox.InputBox()
    self.input_box_layer.SetText("1")
    self.window_dialog_open_picture_file.add(self.input_box_layer)
    position_x=50
    position_y=50
    for widget in self.window_dialog_open_picture_file.widgets:
      widget.rect.move_ip(position_x,position_y)
      position_y=position_y+30
    self.window_dialog_open_picture_file.add(FunnyGUI.button.Button(text="OK",onClickCallback=self.confirm_dialog_open_picture_file))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x+100,position_y+30)
    self.window_dialog_open_picture_file.add(FunnyGUI.button.Button(text="Cancel",onClickCallback=self.cancel_dialog_open_picture_file))
    self.window_dialog_open_picture_file.widgets[-1].rect.move_ip(position_x+150,position_y+30)
    
  def update(self, event):
    return_value=False
    self.game.pictures.do_not_interact_with_pictures=False
    rect_list=self.menu_bar.update(event)
    if rect_list:
      # Menu bar changed it's image because user interacted with it.
      return_value=True
      self.game.pictures.do_not_interact_with_pictures=True
      self.widgets_MenuSystem_to_draw=list(self.widgets_MenuSystem_to_draw_basic)
      for rect in rect_list:
        self.widgets_MenuSystem_to_draw.append([self.game.screen.subsurface(rect).copy(),rect])
      if self.menu_bar.choice:
        if self.menu_bar.choice_index==(0,3):
          self.game.exit()
        elif self.menu_bar.choice_index==(3,0):
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
  
  def confirm_dialog_open_picture_file(self):
    zoom=self.input_box_zoom.GetText()
    try:
      assert(self.is_float(zoom))
      zoom=float(zoom)
      assert(zoom>=0)
    except AssertionError:
      self.show_dialog_wrong_zoom()
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
      self.show_dialog_wrong_layer()
      return
    self.container_widgets_FunnyGUI.remove(self.window_dialog_open_picture_file)
    self.force_everything_to_draw=True
    self.game.pictures.open_picture_file(self.path_to_picture_to_open,layer,zoom)
    
  def cancel_dialog_open_picture_file(self):
    self.container_widgets_FunnyGUI.remove(self.window_dialog_open_picture_file)
    self.force_everything_to_draw=True
    
  def show_dialog_open_picture_file(self):
    self.sgc_dialog_window_shown=True
    self.path_to_picture_to_open=PathGetter.PathGetter.get()
    if not self.path_to_picture_to_open:
      return
    self.create_dialog_open_picture_file()
    
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

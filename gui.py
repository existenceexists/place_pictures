# -*- coding: utf-8 -*-

import pygame

import MenuSystem
import PathGetter

import label


class Gui:
  
  def __init__(self,game):
    
    self.game=game
    self.widgets_container=[]
    self.create_gui()
    self.path_picture_to_open=None
    self.interaction_with_widgets_registered=False

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
    self.bar = MenuSystem.MenuSystem.MenuBar()
    self.widgets_container.append(self.bar)
    self.bar.set((self.menu_game,self.menu_map,self.menu_layer,self.menu_picture,self.menu_selection,self.menu_select))
    
    self.label_selected_pictures_count=label.Label('pictures:  0',(200,200,200,255),(80,80,80,80))
    self.label_selected_pictures_count.set_topright_position((990,60))
    self.widgets_container.append(self.label_selected_pictures_count)
    self.label_selected_picture_types_count=label.Label('types:  0',(200,200,200,255),(80,80,80,80))
    self.label_selected_picture_types_count.set_topright_position((990,90))
    self.widgets_container.append(self.label_selected_picture_types_count)
    
    # We add 4 spaces at the end of the string 'No picture selected' because there is a bug in MenuSystem software that cuts 2 ending letters of the string.
    self.menu_file_and_zoom=MenuSystem.MenuSystem.Menu('No picture selected    ',())
    self.label_file_and_zoom=MenuSystem.MenuSystem.MenuChoice()
    self.label_file_and_zoom.set(self.menu_file_and_zoom,(500,50),w=100)
    self.widgets_container.append(self.label_file_and_zoom)
    
    self.menu_choice_layers=MenuSystem.MenuSystem.MenuChoice()
    self.menu_choice_layers.set(MenuSystem.MenuSystem.Menu(' ',(' ',)),(500,450),w=100)
    self.menu_choice_layers.undraw()
    self.button_layer_confirm=MenuSystem.MenuSystem.Button('OK',100,30)
    self.button_layer_confirm.topleft=(500,500)
    self.button_layer_confirm.set()
    self.game.screen.blit(self.button_layer_confirm._bg,self.button_layer_confirm)
    
  def update(self, event):
    
    self.interaction_with_widgets_registered=False
    ret=[]
    for widget in self.widgets_container:
      ret=widget.update(event)
      
      if ret:
        self.interaction_with_widgets_registered=True
        
        if widget==self.bar:
          if self.bar.choice:
            if self.bar.choice_index==(0,3):
              self.game.running=False
            
            elif self.bar.choice_index==(3,0):
              self.open_picture_file()
            
        elif widget==self.button_layer_confirm:
          if widget.clicked:
            self.widgets_container.remove(self.menu_choice_layers)
            self.widgets_container.remove(self.button_layer_confirm)
            self.menu_choice_layers.undraw()
            self.game.screen.blit(self.button_layer_confirm._bg,self.button_layer_confirm)
            self.game.pictures.open_file(self.path_picture_to_open,self.menu_choice_layers.choice_label)
    
    return ret
    
  def draw(self):
    
    for widget in self.widgets_container:
      if isinstance(widget,MenuSystem.MenuSystem.Button):
        widget._bg=self.game.screen.subsurface(widget).copy()
      else:
        widget.bg=self.game.screen.subsurface(widget.rect).copy()
      widget.draw()
  
  def open_picture_file(self):
    
    self.path_picture_to_open=PathGetter.PathGetter.get()
    layer=0
    if self.game.pictures.pictures_selected.sprites():
      layer=self.game.pictures.all_pictures.get_layer_of_sprite(self.game.pictures.pictures_selected.sprites()[-1])
    self.menu_choice_layers.set(MenuSystem.MenuSystem.Menu(layer,self.game.pictures.all_pictures.layers()),(500,450),w=100)
    self.widgets_container.append(self.menu_choice_layers)
    self.widgets_container.append(self.button_layer_confirm)
    self.button_layer_confirm.set()

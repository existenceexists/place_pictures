# -*- coding: utf-8 -*-

import pygame

import MenuSystem

import label


class Gui:
  
  def __init__(self,game):
    
    self.game=game
    self.widgets_container=[]
    self.create_gui()

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
    self.menu_picture = MenuSystem.MenuSystem.Menu('picture', ('open file','zoom','move to layer'))
    self.menu_layer = MenuSystem.MenuSystem.Menu('layer', ('show list','new','move','join','delete empty'))
    self.menu_select = MenuSystem.MenuSystem.Menu('select',('same file and zoom','same file','all on screen','all'))
    self.menu_map = MenuSystem.MenuSystem.Menu('map',('zoom with pictures ','zoom without pictures','open file'))
    
    #~ création de la barre
    self.bar = MenuSystem.MenuSystem.MenuBar()
    self.widgets_container.append(self.bar)
    self.bar.set((self.menu_game,self.menu_map,self.menu_layer,self.menu_picture,self.menu_select))
    
    self.label_selected_pictures_count=label.Label('pictures:  0',(200,200,200,255),(80,80,80,80))
    self.label_selected_pictures_count.set_topright_position((990,60))
    self.widgets_container.append(self.label_selected_pictures_count)
    self.label_selected_picture_types_count=label.Label('types:  0',(200,200,200,255),(80,80,80,80))
    self.label_selected_picture_types_count.set_topright_position((990,90))
    self.widgets_container.append(self.label_selected_picture_types_count)
    
    # We add 4 spaces at the end of the string 'No picture selected' because there is a bug in MenuSystem software that cuts 2 ending letters of the string.
    self.menu_file_and_zoom=MenuSystem.MenuSystem.Menu('No picture selected    ',())
    self.label_file_and_zoom=MenuSystem.MenuSystem.MenuChoice()
    self.widgets_container.append(self.label_file_and_zoom)
    self.label_file_and_zoom.set(self.menu_file_and_zoom,(460,30))
    
  def update(self, event):
    
    ret=[]
    for widget in self.widgets_container:
      ret=widget.update(event)
      
      if ret:
        
        if widget==self.bar:
          if self.bar.choice:
            if self.bar.choice_index==(0,3):
              self.game.running=False
    
    return ret
    

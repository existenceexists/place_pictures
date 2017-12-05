# -*- coding: utf-8 -*-

import pygame

import MenuSystem
import PathGetter
import FunnyGUI


class Gui:
  
  def __init__(self,game):
    
    self.game=game
    self.widgets_container=[]
    self.widgets_to_draw_basic=[]
    self.widgets_to_draw=[]
    self.create_gui()
    self.path_picture_to_open=None
    self.sgc_dialog_window_shown=False

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
    menu_bar_rect=self.bar.set((self.menu_game,self.menu_map,self.menu_layer,self.menu_picture,self.menu_selection,self.menu_select))
    self.widgets_to_draw_basic.append([self.game.screen.subsurface(menu_bar_rect).copy(),menu_bar_rect])
    self.widgets_to_draw=list(self.widgets_to_draw_basic)
    
    #self.label_selected_pictures_count=label.Label('pictures:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_pictures_count.set_topright_position((990,60))
    #self.widgets_container.append(self.label_selected_pictures_count)
    #self.label_selected_picture_types_count=label.Label('types:  0',(200,200,200,255),(80,80,80,80))
    #self.label_selected_picture_types_count.set_topright_position((990,90))
    #self.widgets_container.append(self.label_selected_picture_types_count)
    
  def create_dialog_open_picture_file(self):
    label_title = sgc.Label(text="""Open and show picture file.""",col=(150,150,150))
    label_title.pos=(0,0)
    label_zoom=sgc.Label(text="""Enter zoom percent. \nThe size of the new picture will be scaled \nto the given percent size of the original picture. \nThe number can be an integer or float number between 0 and infinity.""",col=(150,150,150))
    label_zoom.pos=(0,50)
    self.input_box_zoom = sgc.InputBox(label="zoom percent",default="100")
    self.input_box_zoom.pos = (0,140)
    self.input_box_zoom.text = "100"
    top_layer=self.game.pictures.get_number_of_layers()
    if top_layer==0:
      top_layer=1
    label_layer=sgc.Label(text="""Enter layer number. \nThe new picture will be moved into the layer. \nThe number can be an integer number between 1 and """+str(top_layer)+""" .""",col=(150,150,150))
    label_layer.pos=(0,190)
    self.input_box_layer = sgc.InputBox(label="layer number",default="1")
    self.input_box_layer.pos = (0,270)
    self.input_box_layer.text = "1"
    btn_ok = sgc.Button(label="OK", pos=(100,320))
    btn_ok.on_click = self.confirm_dialog_open_picture_file
    container_dialog_open_picture_file=sgc.Container(widgets=(label_title,label_zoom,self.input_box_zoom,label_layer,self.input_box_layer,btn_ok), border=10)
    # Display dialog window, on_click replaced through inheritance
    self.dialog_open_picture_file=sgc.Dialog(widget=container_dialog_open_picture_file,title="Open picture file")
    self.dialog_open_picture_file.rect.center = self.game.screen.rect.center
    self.sgc_dialog_window_shown
    
  def update(self, event):
    
    self.game.pictures.do_not_interact_with_pictures=False
    ret=[]
    for widget in self.widgets_container:
      ret=widget.update(event)
      #print ret
      if ret:
        self.game.pictures.do_not_interact_with_pictures=True
        if widget==self.bar:
          if self.bar.choice:
            if self.bar.choice_index==(0,3):
              self.game.exit()
            
            elif self.bar.choice_index==(3,0):
              self.show_dialog_open_picture_file()
    if ret:
      self.widgets_to_draw=list(self.widgets_to_draw_basic)
      for rect in ret:
        self.widgets_to_draw.append([self.game.screen.subsurface(rect).copy(), rect])
    return ret
  
  def draw(self):
    for widget_and_rect in self.widgets_to_draw:
      #print widget_and_rect
      self.game.screen.blit(widget_and_rect[0],widget_and_rect[1])
  
  def confirm_dialog_open_picture_file(self):
    zoom=self.input_box_zoom.text
    try:
      assert(self.is_float(zoom))
      zoom=float(zoom)
      assert(zoom>=0)
    except AssertionError:
      self.show_dialog_wrong_zoom()
      return
    layer=self.input_box_layer.text
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
    self.dialog_open_picture_file.remove()
    self.game.pictures.open_picture_file(self.path_to_picture_to_open,layer,zoom)
    
  def show_dialog_open_picture_file(self):
    self.sgc_dialog_window_shown=True
    self.path_to_picture_to_open=PathGetter.PathGetter.get()
    if not self.path_to_picture_to_open:
      return
    self.create_dialog_open_picture_file()
    self.dialog_open_picture_file.add()
    
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

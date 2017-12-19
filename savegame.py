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

import datetime
import os


class Savegame():
  
  def __init__(self,game):
    self.game=game
    self.directory_savegames="savegames"
    self.timestamp_format="%Y-%m-%d_%H-%M-%S_%Z"
    self.filename_template="savegame.{0}{1}.save"
    
  def save(self,filename_user_part):
    if len(filename_user_part)>0:
      filename_user_part=".{0}".format(filename_user_part)
    now=datetime.datetime.now().strftime(self.timestamp_format)
    filename=self.filename_template.format(now,filename_user_part)
    path=os.path.join(self.directory_savegames,filename)
    if os.path.exists(path):
      self.game.gui.display_message_window(["The file ",path,"already exists.","Give another filename."])
      return
    with open(path,'w') as f:
      line="# savegame file for application Place Pictures\n"
      f.write(line)
      line="# timestamp: {0}\n".format(now)
      f.write(line)
      if self.game.map.is_background_from_file:
        line="%map;%file;{0};{1};{2};{3};\n".format(self.game.map.path,self.game.map.scale,self.game.map.rect.topleft[0],self.game.map.rect.topleft[1])
        f.write(line)
      elif self.game.map.is_background_filled_with_color:
        line="%map;%color;{0};{1};{2};{3};{4};{5};\n".format("{0},{1},{2}".format(*self.game.map.background_color),self.game.map.scale,self.game.map.rect.width,self.game.map.rect.height,self.game.map.rect.topleft[0],self.game.map.rect.topleft[1])
        f.write(line)
      for picture in self.game.pictures.pictures_all.sprites():
        selected="n"
        if picture.is_selected:
          selected="s"
        line="%picture;{0};{1};{2};{3};{4};{5};\n".format(picture.path,picture.get_layer(),picture.scale,picture.rect.center[0]+self.game.map.rect.left,picture.rect.center[1]+self.game.map.rect.top,selected)
        f.write(line)
    
  def load(self,path):
    try:
      with open(path,'r') as f:
        lines_count=0
        self.game.pictures.pictures_all.empty()
        self.game.pictures.pictures_to_display.empty()
        self.game.pictures.pictures_selected.empty()
        self.game.pictures.picture_highlighted.empty()
        while True:
          lines_count+=1
          line=f.readline()
          if not line:
            break
          if line.startswith("#"):
            continue
          line=line.split(";")
          if line[0]=="%map":
            if line[1]=="%file":
              self.game.map.open_image(line[2],float(line[3]))
              self.game.map.rect.topleft=(int(line[4]),int(line[5]))
            elif line[1]=="%color":
              rgb=line[2].split(",")
              self.game.map.create_map(int(line[4]),int(line[5]),int(rgb[0]),int(rgb[1]),int(rgb[2]))
              self.game.map.rect.topleft=(int(line[6]),int(line[7]))
            else:
              self.game.gui.display_message_window(["An error occured when loading game.","File",path,"line {0}".format(lines_count)])
              return
          elif line[0]=="%picture":
            selected=False
            if line[6]=="s":
              selected=True
            self.game.pictures.open_picture_file(line[1],int(line[2]),float(line[3]),int(line[4])-self.game.map.rect.left,int(line[5])-self.game.map.rect.top,selected)
          else:
            self.game.gui.display_message_window(["An error occured when loading game.","File",path,"line {0}".format(lines_count)])
            return
    except IOError:
      self.game.gui.display_message_window(["The selected file could not been opened."])

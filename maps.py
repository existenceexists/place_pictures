# -*- coding: utf-8 -*-

import pygame


class Map:
  
  def __init__(self,game):
    
    self.game=game
    self.moving=False
    self.movement_step=10
    
  def open_image(self,path):
    
    self.path=path
    image=pygame.image.load(path)
    image.convert()
    rect=image.get_rect()
    width=max(self.game.screen_rect.width,rect.width)
    height=max(self.game.screen_rect.height,rect.height)
    self.image=pygame.Surface((width,height))
    self.image.convert()
    self.rect=self.image.get_rect()
    self.image.blit(image,(0,0))
    self.rect.left=int((self.game.screen_rect.width-self.rect.width)/2.0)
    self.rect.top=int((self.game.screen_rect.height-self.rect.height)/2.0)
    self.game.screen.blit(self.image,self.rect.topleft)
    
  def update(self,event):
    print('def update(self,event):')
    if event is None:
      pass
    elif event.type==pygame.KEYDOWN:
      print('if event.type==pygame.KEYDOWN:')
      if event.key==pygame.K_DOWN:
        print('if event.key==pygame.K_DOWN:')
        self.start_moving_down()
      elif event.key==pygame.K_UP:
        print('if event.key==pygame.K_UP:')
        self.start_moving_up()
      elif event.key==pygame.K_RIGHT:
        print('if event.key==pygame.K_RIGHT:')
        self.start_moving_right()
      elif event.key==pygame.K_LEFT:
        print('if event.key==pygame.K_LEFT:')
        self.start_moving_left()
    elif event.type==pygame.KEYUP:
      print('elif event.type==pygame.KEYUP:')
      if event.key==pygame.K_DOWN:
        print('if event.key==pygame.K_DOWN:')
        self.stop_moving_down()
      elif event.key==pygame.K_UP:
        print('if event.key==pygame.K_UP:')
        self.stop_moving_up()
      elif event.key==pygame.K_RIGHT:
        print('if event.key==pygame.K_RIGHT:')
        self.stop_moving_right()
      elif event.key==pygame.K_LEFT:
        print('if event.key==pygame.K_LEFT:')
        self.stop_moving_left()
    if self.moving:
      print('if self.moving:')
      self.rect.topleft=(self.rect.left+self.movement[0],self.rect.top+self.movement[1])
      if self.rect.left>0:
        self.rect.left=0
      elif self.rect.right<self.game.screen_rect.right:
        self.rect.right=self.game.screen_rect.right
      elif self.rect.top>0:
        self.rect.top=0
      elif self.rect.bottom<self.game.screen_rect.bottom:
        self.rect.bottom=self.game.screen_rect.bottom
      print(self.rect.topleft)
      self.game.screen.blit(self.image,self.rect.topleft)
      self.game.gui.draw()
      
  def start_moving_down(self):
    self.moving=True
    self.movement=[0,-self.movement_step]
    
  def start_moving_up(self):
    self.moving=True
    self.movement=[0,self.movement_step]
    
  def start_moving_right(self):
    self.moving=True
    self.movement=[-self.movement_step,0]
    
  def start_moving_left(self):
    self.moving=True
    self.movement=[self.movement_step,0]
    
  def stop_moving_down(self):
    self.moving=False
    self.movement=[0,0]
    
  def stop_moving_up(self):
    self.moving=False
    self.movement=[0,0]
    
  def stop_moving_right(self):
    self.moving=False
    self.movement=[0,0]
    
  def stop_moving_left(self):
    self.moving=False
    self.movement=[0,0]
    

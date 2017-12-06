# -*- coding: utf-8 -*-

import pygame


class Map:
  
  def __init__(self,game):
    self.game=game
    self.moving=False
    self.movement_step=10
    self.movement=[0,0]
    
  def update(self,event):
    return_value=False
    self.movement=[0,0]
    self.moving=False
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_DOWN:
        self.set_moving([self.movement[0],-self.movement_step])
      elif event.key==pygame.K_UP:
        self.set_moving([self.movement[0],self.movement_step])
      elif event.key==pygame.K_RIGHT:
        self.set_moving([-self.movement_step,self.movement[1]])
      elif event.key==pygame.K_LEFT:
        self.set_moving([self.movement_step,self.movement[1]])
    elif event.type==pygame.KEYUP:
      if event.key==pygame.K_DOWN or event.key==pygame.K_UP:
        self.set_moving([self.movement[0],0])
        return_value=True
      elif event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
        self.set_moving([0,self.movement[1]])
        return_value=True
    if self.moving:
      return_value=True
      self.rect.topleft=(self.rect.left+self.movement[0],self.rect.top+self.movement[1])
      if self.rect.left>0:
        self.rect.left=0
      if self.rect.right<self.game.screen_rect.right:
        self.rect.right=self.game.screen_rect.right
      if self.rect.top>0:
        self.rect.top=0
      if self.rect.bottom<self.game.screen_rect.bottom:
        self.rect.bottom=self.game.screen_rect.bottom
    return return_value
    
  def draw(self):
    self.game.screen.blit(self.image,self.rect.topleft)
    
  def set_moving(self, movement):
    self.movement=movement
    if movement==[0,0]:
      self.moving=False
    else:
      self.moving=True
    
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
    

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2017 František Brožka <sentientfanda@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import pygame


class Mouse(pygame.sprite.Sprite):
  
  def __init__(self):
    self.image=pygame.Surface((1,1))
    self.rect=self.image.get_rect()
    
  def update(self,event):
    if event.type==pygame.MOUSEMOTION or event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.MOUSEBUTTONUP:
      self.rect.topleft=event.pos
    
  def draw(self):
    pass

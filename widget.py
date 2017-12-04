#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame


class Widget(pygame.sprite.Sprite):
	def __init__(self, container=None):
		pygame.sprite.Sprite.__init__(self)

		self.container = container
		self.focused = 0
		self.highlighted = 0
		self.dirty = 1

 	def Destroy(self):
		self.container = None
		del self.container
		pygame.sprite.Sprite.kill(self)

	def SetFocus(self, val):
		self.focused = val
		self.SetDirty(1)

 	def SetHoverHighlight(self, value):
		self.highlighted = value
		self.SetDirty(1)

 	def OnGetFocus(self, event):
		self.SetFocus(1)

 	def OnLoseFocus(self, event):
		self.SetFocus(0)

 	def SetDirty(self, value):
		self.dirty = value
		if not self.container is None:
			self.container.SetDirty(value)

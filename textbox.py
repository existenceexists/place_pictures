

class TextBox(pygame.sprite.Sprite):
	def __init__(
			self,
			width=200,
			backspaceKeys=(pygame.K_BACKSPACE,), 
			fontFace=None, fontSize=14,
			borderLineColor=(0,0,100),
			backgroundColor=(0,0,0),
			borderLineWidth=4, 
			textNormalColor=(100,0,0), 
			textFocusedColor=(255,255,0), 
			textHighlightedColor=(255,0,0), 
			textPositionX=22):
		
		pygame.sprite.Sprite.__init__(self)
		self.focused = 0
		self.highlighted = 0
		self.dirty = 1
		self.backspaceKeys = list(backspaceKeys)
		
		self.textNormalColor = textNormalColor
		self.textFocusedColor = textFocusedColor
		self.textHighlightedColor = textHighlightedColor
		
		if (fontFace is None):
                        fontFilename = pygame.font.match_font("freesans,sansserif,microsoftsansserif,arial,dejavusans,verdana,timesnewroman,helvetica", bold=False)
                        if fontFilename is None:
				allAvailableFonts = pygame.font.get_fonts()
				fontFilename = pygame.font.match_font(allAvailableFonts[0])
			fontFace = fontFilename
		self.font = pygame.font.Font(fontFace, fontSize)
		linesize = self.font.get_linesize()
		
		self.rect = pygame.Rect((
			0, 0, width,
			#linesize + 2*f_config.TEXT_BOX_BORDER_LINE_WIDTH))
			linesize + borderLineWidth))
		boxImg = pygame.Surface(self.rect.size).convert_alpha()
		boxImg.fill(backgroundColor)
		#color = f_config.TEXT_BOX_LINE_COLOR
		"""
		rect = pygame.Rect((
			self.rect.left, self.rect.top,
			self.rect.width - f_config.TEXT_BOX_BORDER_LINE_WIDTH +3,
			self.rect.height - f_config.TEXT_BOX_BORDER_LINE_WIDTH +3))
		"""
		if (borderLineWidth > 0):
			pygame.draw.rect(boxImg, borderLineColor, self.rect, borderLineWidth)

		self.emptyImg = boxImg.convert_alpha()
		self.image = boxImg

		self.highlighted = 0
		self.text = ''
		#self.textPos = (22, 2)
		#self.textDefaultPosition = f_config.TEXT_BOX_TEXT_DEFAULT_POSITION
		self.textDefaultPosition = (
			textPositionX,
			#0 + borderLineWidth)
			#(self.rect.height - linesize)//2 + 3)
			(self.rect.height - linesize)//2)

	#----------------------------------------------------------------------
	def update(self, event):
		if not self.dirty:
			return

		text = self.text
		if self.focused:
			text += '|'
			color = self.textFocusedColor
		elif self.highlighted:
			color = self.textHighlightedColor
		else: 
			color = self.textNormalColor
		
		textPosition = list(self.textDefaultPosition)
		size = self.font.size(text)
		#if (size[0] > (self.rect.width - self.textDefaultPosition[0] - 20)):
		#if (size[0] > (self.rect.width - self.textDefaultPosition[0] - 22)):
		if (size[0] > (self.rect.width - 2*self.textDefaultPosition[0])):
			textPosition[0] = (
				(self.rect.width - self.textDefaultPosition[0]) - size[0])

		textImg = self.font.render(text, 1, color)
		self.image.blit(self.emptyImg, (0,0))
		#self.image.blit(textImg, self.textPos)
		self.image.blit(textImg, textPosition)

		self.dirty = 0

	#----------------------------------------------------------------------
	def Click(self):
		self.focused = 1
		self.SetDirty(1)
		if (not self.container is None):
			self.container.SetFocus(1)

	#----------------------------------------------------------------------
	def SetText(self, newText):
		self.text = newText
		self.SetDirty(1)
		"""
		if ((not self.container is None) and (not self.container.container is None)):
			print self.container, self.container.dirty
			self.container.container.dirty = 1
			print "self.container.dirty = 1"
		"""

	#----------------------------------------------------------------------
	def GetText(self):
		return self.text


	#----------------------------------------------------------------------
	def OnKeyPressed(self, event):
		if self.focused:
			if event.key in self.backspaceKeys:
				#strip of last character
				newText = self.text[:-1]
				self.SetText(newText)
				return True
			# add the unicode character to the text
			newText = self.text + event.unicode
			self.SetText(newText)
			return True

	#----------------------------------------------------------------------
	def OnMetaPressed(self, event):
		if self.focused and event.key in self.focusCycleKeys:
			#don't respond to the focus cycle keys
			return
		if self.focused and event.key in self.backspaceKeys:
			#strip of last character
			newText = self.text[:-1]
			self.SetText(newText)
			return True

	#----------------------------------------------------------------------
	def OnMouseClick(self, pos):
		if self.rect.collidepoint(pos):
			self.Click()
			#print "textBox.OnMouseClick-if collidepoint,", pos
			return True
		elif self.focused:
			self.SetFocus(0)
			#print "textBox.OnMouseClick-elif focused,", pos
			return True

	#----------------------------------------------------------------------
	def OnMouseMove(self, pos):
		if self.rect.collidepoint(pos):
			if not self.highlighted:
				self.SetHoverHighlight(1)
				return True
		elif self.highlighted:
			self.SetHoverHighlight(0)
			return True

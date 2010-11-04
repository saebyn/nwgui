
import pygame
from pygame.locals import *

import string

from nwgui.container import Container
from nwgui.image import Image
from nwgui.label import Label

class Text(Container):
    def __init__(self, text, width, height, game, background=(255, 255, 255), 
                       *args, **kwargs):
        kwargs['border'] = (1, (0, 0, 0))
        Container.__init__(self, width, height, game, *args, **kwargs)
        self.cursorPosition = 0
        self.text = ""

        self.textDisplayedBeginIndex = 0
        
        self.cursor = Image('textcursor', game)
        self.add(self.cursor)

        self.label = Label('', game, fontSize=30)
        self.add(self.label)

    @property
    def textDisplayedEndIndex(self):
        for index in xrange(len(self.text), self.textDisplayedBeginIndex + 1, -1):
            if self.label.font.size(self.text[self.textDisplayedBeginIndex:index])[0] < self.rect.width - 4:
                return index

        return self.textDisplayedBeginIndex + 1

    def setPosition(self, position):
        Container.setPosition(self, position)

        x, y = position

        self.cursor.setPosition(self._cursorPosition())

        self.label.setPosition((x + 3, y))
        self.label.rect.bottom = self.rect.bottom - 2

    def update(self, *args):
        Container.update(self, *args)
        self.cursor.setPosition(self._cursorPosition())
        self.label.setText(self._viewableText())
        self.label.changeLayer(self.layer + 1)
        self.cursor.changeLayer(self.layer + 2)

    def _viewableText(self):
        return self.text[self.textDisplayedBeginIndex:self.textDisplayedEndIndex]

    def _relativeCursorPosition(self):
        if self.cursorPosition < self.textDisplayedBeginIndex:
            self.textDisplayedBeginIndex = self.cursorPosition

        while self.textDisplayedEndIndex < self.cursorPosition:
            self.textDisplayedBeginIndex += 1

        return self.cursorPosition - self.textDisplayedBeginIndex

    def _cursorPosition(self):
        beforeCursorViewableText = self._viewableText()[:self._relativeCursorPosition()]

        return (self.label.font.size(beforeCursorViewableText)[0] + \
                self.rect.left,
                self.rect.top + 2)

    def moveCursorRight(self):
        if self.cursorPosition >= len(self.text):
            return

        self.cursorPosition += 1

        if self.cursor.rect.right > self.rect.right:
            self.cursor.rect.right = self.rect.right
        
    def moveCursorLeft(self):
        if self.cursorPosition == 0:
            return

        self.cursorPosition -= 1

        if self.cursor.rect.left < self.rect.left:
            self.cursor.rect.left = self.rect.left

    def deleteCharacter(self):
        # Can't delete anything if there's no text.
        if len(self.text) == 0:
            return

        self.text = self.text[:self.cursorPosition] + \
                    self.text[self.cursorPosition + 1:]
        self.cursor.setPosition(self._cursorPosition())

    def addCharacter(self, character):
        self.text += character
        self.moveCursorRight()

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.setActive()
            # TODO support mouse insert-cursor selection
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.moveCursorLeft()
            elif event.key == K_RIGHT:
                self.moveCursorRight()
            elif event.key == K_DELETE:
                self.deleteCharacter()
            elif event.key == K_BACKSPACE:
                self.moveCursorLeft()
                self.deleteCharacter()
            elif event.unicode in string.printable and event.unicode not in '\n\r\x0b\x0c':
                self.addCharacter(event.unicode)

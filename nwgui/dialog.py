
import pygame
from pygame.locals import *

from nwgui.widget import Widget
from nwgui.label import Label
from nwgui.button import SpriteButton


class Dialog(Widget):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255, 255, 255))

        # add ourselves
        self.root.add(self, 0, 0)
        self.rect.center = self.root.rect.center

        self.title = kwargs.pop('title', '')
        self._contents = None
        self._label = Label(self.title, root=self.root)
        self._label.setParent(self)
        self._label.setPosition((self.rect.left + 5,
                                 self.rect.top + 5))

        def closeCallback(*args):
            self.kill()

        self._closeButton = SpriteButton('x16', closeCallback, root=self.root)
        self._closeButton.setParent(self)
        buttonPosition = (self.rect.right - self._closeButton.rect.width - 5,
                          self.rect.top + 5)
        self._closeButton.setPosition(buttonPosition)

        self.moveToFront()

    def setPosition(self, position):
        pass

    def handleEvent(self, event):
        widgets = [self._closeButton, self._contents]
        # handle mouse events by deciding which widgets are in the clicked area
        for widget in widgets:
            if event.type in [MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP]:
                if widget.rect.collidepoint(pygame.mouse.get_pos()):
                    widget.handleEvent(event)
            else:
                widget.handleEvent(event)

    def moveToFront(self):
        super(Dialog, self).moveToFront()
        self._label.moveToFront()
        self._closeButton.moveToFront()
        if self._contents is not None:
            self._contents.moveToFront()

    def moveToBack(self):
        if self._contents is not None:
            self._contents.moveToBack()
        self._closeButton.moveToBack()
        self._label.moveToBack()
        super(Dialog, self).moveToBack()

    def kill(self):
        self._contents.kill()
        self._label.kill()
        self._closeButton.kill()
        super(Dialog, self).kill()

    def show(self):
        self._contents.show()
        self._label.show()
        self._closeButton.show()
        super(Dialog, self).show()
        self.moveToFront()

    def setContents(self, widget):
        self._contents = widget
        self._contents.setParent(self)
        self._contents.setPosition((self.rect.left + 5,
                                    self.rect.top + \
                                    max(self._label.rect.height,
                                        self._closeButton.rect.height) + 5))
        self._contents.updateLayer()

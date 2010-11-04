
import pygame

from nwgui.container import AbsoluteContainer

class GUI(AbsoluteContainer):
    def __init__(self, game):
        AbsoluteContainer.__init__(self, game.screen.get_width(),
                                         game.screen.get_height(),
                                         game)
        self.image = pygame.Surface((0,0))
        self.active = None
        self.names = {}

    def get(self, widgetName):
        return self.names[widgetName]

    def handleEvent(self, event):
        AbsoluteContainer.handleEvent(self, event)

    def updateLayers(self):
        for widget in self.widgets:
            widget.updateLayer()

    def setParent(self, parent):
        raise NotImplementedError

    def isActive(self):
        return self.active is not None

    def setActive(self, widget):
        if self.active is not None:
            self.active.setInactive()

        self.active = widget

    def setInactive(self, widget=None):
        if self.active == widget or widget is None:
            self.active = None

    def addSprite(self, sprite):
        self.game.addGUISprite(sprite)

    def setName(self, name, widget):
        self.names[name] = widget

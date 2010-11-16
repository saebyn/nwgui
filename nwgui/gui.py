
import pygame

from nwgui.container import AbsoluteContainer

class AbstractGUI(object):
    def __init__(self, game):
        raise NotImplementedError

    def getGameObject(self):
        raise NotImplementedError

    def get(self, widgetName):
        raise NotImplementedError

    def setName(self, name, widget):
        raise NotImplementedError

    def updateLayers(self):
        raise NotImplementedError

    def getLayer(self):
        raise NotImplementedError

    def addSprite(self, widget):
        raise NotImplementedError

    def setActive(self, widget):
        raise NotImplementedError

    def setInactive(self, widget):
        raise NotImplementedError

    def isControlledPosition(self, position):
        raise NotImplementedError

class GUI(AbsoluteContainer, AbstractGUI):
    def __init__(self, game):
        self._game = game
        AbsoluteContainer.__init__(self, game.screen.get_width(),
                                         game.screen.get_height(),
                                         self, root=self)
        self.image = pygame.Surface((0,0))
        self.active = None
        self.names = {}

    def getGameObject(self):
        return self._game

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
        self._game.addGUISprite(sprite)

    def setName(self, name, widget):
        self.names[name] = widget

    def isControlledPosition(self, position):
        for widget in self._game.guiSprites.sprites():
            if widget is self:
                continue

            if widget.rect.collidepoint(position):
                return True

        return False

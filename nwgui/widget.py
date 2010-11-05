
import pygame

from nwgui.renderers.basewidget import BaseWidget

def deferUntilParent(method):
    def inner(*args, **kwargs):
        self = args[0]
        if self.parent is not None:
            method(*args, **kwargs)
        else:
            def deferrable():
                method(*args, **kwargs)

            self._deferUntilParent.append(deferrable)

    return inner

class Widget(BaseWidget):
    def __init__(self, width, height, *args, **kwargs):
        BaseWidget.__init__(self, *args, **kwargs)

        self.rect = pygame.Rect((0,0), (width, height))

        self.sheet = self._renderer.getSpriteSource('gui')

        if kwargs.has_key('fontSize'):
            self.fontSize = kwargs['fontSize']
        else:
            self.fontSize = 16

        self.font = self._renderer.font(None, self.fontSize)
        self.layer = 0
        self._renderer.addSprite(self)

        self.parent = None
        self._deferUntilParent = []

    def setName(self, name, widget=None):
        if widget is None:
            widget = self
        
        self.root.setName(name, widget)

    def handleEvent(self, event):
        pass

    def changeLayer(self, layer):
        self._renderer.changeLayer(self, layer)

    def moveToFront(self):
        frontLayer = self._renderer.getTopLayer()
        self.changeLayer(frontLayer + 1)

    def moveToBack(self):
        backLayer = self._renderer.getBottomLayer()
        self.changeLayer(backLayer - 1)

    def getLayer(self):
        return self.layer

    @deferUntilParent
    def updateLayer(self):
        """
        Update the layer count of this widget. This is also when this widget is added as a
        sprite to the game. This should be called only by the GUI class.
        """
        self.layer = self.parent.getLayer() + 1
        if self.alive():
            self.changeLayer(self.layer)

    def setParent(self, parent):
        """
        Sets the parent widget of this widget. This is called by the parent
        widget's add() method.
        """
        self.parent = parent
        for lmda in self._deferUntilParent:
            lmda()

    @deferUntilParent
    def setActive(self, widget=None):
        if widget is None:
            widget = self

        self.parent.setActive(widget)

    @deferUntilParent
    def setInactive(self, widget=None):
        if widget is None:
            widget = self

        self.parent.setInactive(widget)

    def setPosition(self, position):
        """
        setPosition

        Sets the location of the widget (x and y are in pixels, where
        x, y = position).
        """
        self.rect.topleft = position

    def isVisible(self):
        return self.alive()

    def show(self):
        self.addSprite(self)

    def hide(self):
        self.kill()

    @deferUntilParent
    def addSprite(self, sprite):
        self.parent.addSprite(sprite)

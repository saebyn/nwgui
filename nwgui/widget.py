
import pygame

class Widget(pygame.sprite.Sprite):
    def __init__(self, width, height, game, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((0,0), (width, height))
        self.sheet = game.getSheet('gui')

        if kwargs.has_key('fontSize'):
            self.fontSize = kwargs['fontSize']
        else:
            self.fontSize = 16

        self.font = pygame.font.Font(None, self.fontSize)
        self.game = game
        self.layer = 0
        self.game.addGUISprite(self)

        self.parent = None
        self._deferUntilParent = []

    def setName(self, name, widget=None):
        if widget is None:
            widget = self
        
        if self.parent is not None:
            self.parent.setName(name, widget)
        else:
            self._deferUntilParent.append(lambda: self.parent.setName(name, widget))

    def handleEvent(self, event):
        pass

    def changeLayer(self, layer):
        self.game.guiSprites.change_layer(self, layer)

    def moveToFront(self):
        frontLayer = self.game.guiSprites.get_top_layer()
        self.game.guiSprites.change_layer(self, frontLayer + 1)

    def moveToBack(self):
        backLayer = self.game.guiSprites.get_bottom_layer()
        self.game.guiSprites.change_layer(self, backLayer - 1)

    def updateLayer(self):
        """
        Update the layer count of this widget. This is also when this widget is added as a
        sprite to the game. This should be called by the gui_factory...
        """
        self.layer = self.parent.layer + 1
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

    def setActive(self, widget=None):
        if widget is None:
            widget = self

        self.parent.setActive(widget)

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

    def addSprite(self, sprite):
        self.parent.addSprite(sprite)

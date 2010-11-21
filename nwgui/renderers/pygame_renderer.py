
import pygame

from nwgui.renderers.abstract_renderer import AbstractRenderer


class PyGameRenderer(AbstractRenderer):
    def __init__(self, game):
        self.game = game

    def getTopLayer(self):
        return self.game.guiSprites.get_top_layer()

    def getBottomLayer(self):
        return self.game.guiSprites.get_bottom_layer()

    def changeLayer(self, sprite, layer):
        self.game.guiSprites.change_layer(sprite, layer)

    def addSprite(self, sprite):
        self.game.addGUISprite(sprite)

    def getSpriteSource(self, name):
        return self.game.getSpriteSource(name)

    def font(self, fontName, fontSize):
        return pygame.font.Font(fontName, fontSize)

"""
BaseWidget

Mainly, this provides a way to do dependency injection on the GUI widgets
to allow us to unit test them. If we do eventually want to make this work
without pygame, we'll have to abstract over the pygame stuff here.
"""

import pygame

from nwgui.renderers.pygame_renderer import PyGameRenderer

class BaseWidget(pygame.sprite.Sprite):
    def __init__(self, root, renderer=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.root = root
        self.game = root.getGameObject()

        if renderer is None:
            self._renderer = PyGameRenderer(self.game)
        else:
            self._renderer = renderer

    def setRenderer(self, renderer):
        self._renderer = renderer

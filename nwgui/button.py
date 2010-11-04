
from pygame.locals import *

from nwgui.label import Label
from nwgui.widget import Widget

class BaseButton:
    def __init__(self, callback):
        self._callback = callback

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self._callback()
            self.setActive()
        elif event.type == KEYDOWN and event.key in [K_RETURN, K_SPACE]:
            self._callback()
            self.setActive()

class Button(BaseButton, Label):
    def __init__(self, text, callback, game, background=(100, 100, 100),
                       padding=(10, 10), *args, **kwargs):
        kwargs['background'] = background
        kwargs['padding'] = padding
        Label.__init__(self, text, game, *args, **kwargs)
        BaseButton.__init__(self, callback)


class ImageButton(Widget, BaseButton):
    def __init__(self, callback, game, *args, **kwargs):
        BaseButton.__init__(self, callback)


import pygame

from nwgui.widget import Widget


class Label(Widget):
    def __init__(self, text, color=(0, 0, 0), background=(255, 255, 255),
                       padding=(0, 0), width=None, height=None, **kwargs):
        Widget.__init__(self, 1, 1, **kwargs)

        self.color = color
        self.background = background
        self.text = text
        self.padding = padding
        self.width = width
        self.height = height
        self._render()
        self._dirty = False

    def setBackground(self, background):
        self.background = background
        self._dirty = True

    def setColor(self, color):
        self.color = color
        self._dirty = True

    def setText(self, text):
        self.text = text
        self._dirty = True

    def update(self, *args):
        Widget.update(self, *args)

        if self._dirty:
            self._render()
            self._dirty = False

    def _render(self):
        renderedText = self.font.render(self.text, 1,
                                        self.color, self.background)

        if self.width is None:
            width = renderedText.get_width()
        else:
            width = self.width

        if self.height is None:
            height = renderedText.get_height()
        else:
            height = self.height

        paddingX, paddingY = self.padding

        width += paddingX
        height += paddingY

        self.image = pygame.Surface((width, height))
        self.image.fill(self.background)

        # Position the source rectange in the center of the destination
        # rectangle. Find the top-left coordinates of the source rectangle
        # and use that as the destination of the blit, so that the text
        # will be centered on the background.
        dest = pygame.Rect(0, 0, width, height)
        src = pygame.Rect(0, 0,
                          renderedText.get_width(), renderedText.get_height())
        src.center = dest.center

        self.image.blit(renderedText, src)
        self.rect.size = self.image.get_size()

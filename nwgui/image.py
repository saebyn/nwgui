
import pygame

from nwgui.widget import Widget

class DirectImage(Widget):
    def __init__(self, image, width, height, game):
        Widget.__init__(self, width, height, game)

        if image is None:
            self.image = pygame.Surface((0, 0))
        else:
            self.setImage(image)

    def setImage(self, image):
        if image.get_width() < self.rect.width or \
           image.get_height() < self.rect.height:
            background = pygame.Surface(self.rect.size)
            background.fill((0, 0, 0))
            relrect = pygame.rect.Rect((0, 0), self.rect.size)
            imrect = image.get_rect()
            imrect.center = relrect.center
            background.blit(image, imrect)
            self.image = background
        else:
            self.image = image

class Image(Widget):
    def __init__(self, sheetName, game):
        self.image = game.getSheet('gui').get(sheetName)

        Widget.__init__(self, self.image.get_width(), self.image.get_height(),
                        game)

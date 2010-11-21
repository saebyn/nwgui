
import pygame

from nwgui.widget import Widget


class ProgressBar(Widget):
    PROGRESS_SPRITE = 'progress'

    def __init__(self, width, *args, **kwargs):
        root = kwargs.get('root')
        # _progress ranges from 0 to width
        self._progress = 0
        self._width = width

        # this is the number of pixels to adjust per progress % point
        self._progressPixelStep = width / 100.0

        self._baseImage = root.getGameObject() \
                              .getSpriteSource('gui') \
                              .get(self.PROGRESS_SPRITE)

        self._prepImage()

        Widget.__init__(self, width, self.image.get_height(),
                        *args, **kwargs)

    def _prepImage(self):
        # copy self._baseImage to self.image, until we get self._progress
        # pixels of image
        if not hasattr(self, 'image'):
            self.image = pygame.Surface((self._width,
                                         self._baseImage.get_height()))

        self.image.fill((0, 0, 0))

        x = 0
        while x < self._progress:
            nextWidth = min(self._progress - x, self._baseImage.get_width())
            self.image.blit(self._baseImage, (x, 0),
                            pygame.rect.Rect((0, 0),
                                             (nextWidth,
                                              self._baseImage.get_height())))
            x += nextWidth

    def setProgress(self, progress):
        self._progress = progress * self._progressPixelStep
        self._prepImage()

    def addProgress(self, progress):
        self._progress += progress * self._progressPixelStep
        self._prepImage()
